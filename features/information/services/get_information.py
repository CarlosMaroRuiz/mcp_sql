from core import MySQLConnector
import json

def get_all_tables_safe(db):
    """Versión segura de get_all_tables que maneja mayúsculas/minúsculas"""
    query = """
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = %s
    """
    result = db.execute_query(query, (db.config['database'],))
    if not result:
        return None
    
    tables = []
    for row in result:
        # Buscar la clave que coincida con 'table_name' sin importar mayúsculas/minúsculas
        key = next((k for k in row.keys() if k.lower() == 'table_name'), None)
        if key:
            tables.append(row[key])
    
    return tables

def get_table_schema_safe(db, table_name: str):
    """Versión segura de get_table_schema que maneja mayúsculas/minúsculas"""
    query = """
    SELECT column_name, data_type, is_nullable, column_default, column_key
    FROM information_schema.columns 
    WHERE table_schema = %s AND table_name = %s
    ORDER BY ordinal_position
    """
    result = db.execute_query(query, (db.config['database'], table_name))
    if not result:
        return None
    
    # Normalizar todas las claves a minúsculas
    normalized_result = []
    for row in result:
        normalized_row = {k.lower(): v for k, v in row.items()}
        normalized_result.append(normalized_row)
    
    return normalized_result

def get_foreign_keys_safe(db, table_name: str):
    """Obtiene claves foráneas con manejo seguro de claves"""
    query = """
    SELECT 
        COLUMN_NAME, 
        REFERENCED_TABLE_NAME, 
        REFERENCED_COLUMN_NAME,
        CONSTRAINT_NAME
    FROM 
        INFORMATION_SCHEMA.KEY_COLUMN_USAGE
    WHERE 
        TABLE_SCHEMA = %s 
        AND TABLE_NAME = %s
        AND REFERENCED_TABLE_NAME IS NOT NULL
    """
    result = db.execute_query(query, (db.config['database'], table_name))
    if not result:
        return []
    
    # Normalizar todas las claves a minúsculas
    normalized_result = []
    for row in result:
        normalized_row = {k.lower(): v for k, v in row.items()}
        normalized_result.append(normalized_row)
    
    return normalized_result

def get_information():
    """
    Obtiene información completa de la base de datos en formato JSON:
    - Número total de tablas
    - Nombres de todas las tablas
    - Claves primarias de cada tabla
    - Claves foráneas y sus relaciones
    
    Returns:
        str: Cadena JSON con toda la información de la base de datos
    """
    with MySQLConnector() as db:
        # 1. Obtener información general de la base de datos
        db_info = db.get_database_info()
        
        # 2. Obtener todas las tablas (usando versión segura)
        tables = get_all_tables_safe(db)
        if not tables:
            return json.dumps({"error": "No se encontraron tablas en la base de datos"})
            
        num_tables = len(tables)
        
        # 3. Obtener detalles de cada tabla
        db_structure = {}
        
        for table in tables:
            table_details = {
                "columns": [],
                "primary_keys": [],
                "foreign_keys": []
            }
            
            # Obtener esquema de la tabla (usando versión segura)
            schema = get_table_schema_safe(db, table)
            if schema:
                for col in schema:
                    col_info = {
                        "name": col['column_name'],
                        "type": col['data_type'],
                        "nullable": col['is_nullable'] == 'YES',
                        "default": col.get('column_default')
                    }
                    table_details["columns"].append(col_info)
                    
                    # Identificar clave primaria
                    if col.get('column_key') == 'PRI':
                        table_details["primary_keys"].append(col['column_name'])
            
            # Obtener claves foráneas (usando versión segura)
            foreign_keys = get_foreign_keys_safe(db, table)
            
            for fk in foreign_keys:
                fk_info = {
                    "column": fk['column_name'],
                    "references_table": fk['referenced_table_name'],
                    "references_column": fk['referenced_column_name'],
                    "constraint_name": fk['constraint_name']
                }
                table_details["foreign_keys"].append(fk_info)
            
            db_structure[table] = table_details
        
        # 4. Obtener relaciones entre tablas (mapa de relaciones)
        relationships = {}
        
        for table, details in db_structure.items():
            for fk in details['foreign_keys']:
                relation = f"{table}.{fk['column']} → {fk['references_table']}.{fk['references_column']}"
                relationships[relation] = {
                    "from_table": table,
                    "from_column": fk['column'],
                    "to_table": fk['references_table'],
                    "to_column": fk['references_column'],
                    "constraint": fk['constraint_name']
                }
        
        # 5. Obtener tabla con más relaciones
        table_relations = {}
        for rel in relationships.values():
            table_relations[rel['from_table']] = table_relations.get(rel['from_table'], 0) + 1
        
        most_related_table = None
        most_relations_count = 0
        if table_relations:
            most_related_table = max(table_relations, key=table_relations.get)
            most_relations_count = table_relations[most_related_table]
        
        # 6. Construir el resultado final
        result = {
            "database_info": db_info,
            "summary": {
                "num_tables": num_tables,
                "tables": tables,
                "num_relationships": len(relationships),
                "most_related_table": most_related_table,
                "most_relations_count": most_relations_count
            },
            "structure": db_structure,
            "relationships": relationships
        }
        
        # 7. Convertir a JSON y retornar
        return json.dumps(result, indent=2, default=str, ensure_ascii=False)
