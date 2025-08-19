from dotenv import load_dotenv
import os
import mysql.connector
from mysql.connector import Error
from typing import List, Dict, Any, Optional, Union
import json
from datetime import datetime

load_dotenv()

class MySQLConnector:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MySQLConnector, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        self.config = {
            "user": os.getenv("USER_BD"),
            "password": os.getenv("PASSWORD_BD"),
            "host": os.getenv("HOST_DB"),
            "database": os.getenv("DATABASE_MYSQL"),
        }
        self.conn = None
        self.cursor = None
        self._initialized = True
    
    def __enter__(self):
        """Context manager entrada"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager salida"""
        self.disconnect()
        return False  # No suprimir excepciones
    
    def connect(self):
        try:
            if not self.conn or not self.conn.is_connected():
                self.conn = mysql.connector.connect(**self.config)
                self.cursor = self.conn.cursor(dictionary=True)
                print("✅ Conexión establecida a MySQL")
            return True
        except Error as e:
            print(f"❌ Error de conexión: {e}")
            return False
    
    def disconnect(self):
        try:
            # Cerrar cursor si existe y es válido
            if hasattr(self, 'cursor') and self.cursor is not None:
                try:
                    if hasattr(self.cursor, 'close'):
                        self.cursor.close()
                except (ReferenceError, AttributeError):
                    pass  # El objeto ya fue destruido
                finally:
                    self.cursor = None
            
            # Cerrar conexión si existe y es válida
            if hasattr(self, 'conn') and self.conn is not None:
                try:
                    if hasattr(self.conn, 'is_connected') and self.conn.is_connected():
                        self.conn.close()
                        print("🔌 Conexión cerrada")
                except (ReferenceError, AttributeError):
                    pass  # El objeto ya fue destruido
                finally:
                    self.conn = None
                    
        except Exception:
            # Silenciar cualquier otro error de cierre
            pass
    
    def normalize_keys(self, data):
        """Normaliza las claves de un diccionario o lista de diccionarios a minúsculas"""
        if isinstance(data, dict):
            return {k.lower(): v for k, v in data.items()}
        elif isinstance(data, list):
            return [self.normalize_keys(item) for item in data]
        return data
    
    def execute_query(self, query, params=None):
        if not self.connect():
            return None
            
        try:
            self.cursor.execute(query, params or ())
            
            if query.strip().upper().startswith(('INSERT', 'UPDATE', 'DELETE')):
                self.conn.commit()
                return self.cursor.rowcount
            else:
                result = self.cursor.fetchall()
                # Normalizar claves a minúsculas
                return self.normalize_keys(result)
        except Error as e:
            print(f"❌ Error en consulta: {e}")
            self.conn.rollback()
            return None
    
    # ========== MÉTODOS CRUD ==========
    
    def insert(self, table: str, data: Dict[str, Any]) -> Optional[int]:
        """Inserta un registro en la tabla"""
        if not data:
            return None
            
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        result = self.execute_query(query, tuple(data.values()))
        return self.cursor.lastrowid if result else None
    
    def insert_many(self, table: str, data_list: List[Dict[str, Any]]) -> Optional[int]:
        """Inserta múltiples registros"""
        if not data_list:
            return None
            
        columns = ', '.join(data_list[0].keys())
        placeholders = ', '.join(['%s'] * len(data_list[0]))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        try:
            if not self.connect():
                return None
                
            values = [tuple(row.values()) for row in data_list]
            self.cursor.executemany(query, values)
            self.conn.commit()
            return self.cursor.rowcount
        except Error as e:
            print(f"❌ Error en inserción múltiple: {e}")
            self.conn.rollback()
            return None
    
    def select(self, table: str, conditions: str = "", params: tuple = (), 
               columns: str = "*", order_by: str = "", limit: int = None) -> Optional[List[Dict]]:
        """Selecciona registros de una tabla"""
        query = f"SELECT {columns} FROM {table}"
        
        if conditions:
            query += f" WHERE {conditions}"
        if order_by:
            query += f" ORDER BY {order_by}"
        if limit:
            query += f" LIMIT {limit}"
            
        return self.execute_query(query, params)
    
    def select_one(self, table: str, conditions: str = "", params: tuple = (), 
                   columns: str = "*") -> Optional[Dict]:
        """Selecciona un solo registro"""
        result = self.select(table, conditions, params, columns, limit=1)
        return result[0] if result else None
    
    def update(self, table: str, data: Dict[str, Any], conditions: str, params: tuple = ()) -> Optional[int]:
        """Actualiza registros en una tabla"""
        if not data:
            return None
            
        set_clause = ', '.join([f"{key} = %s" for key in data.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {conditions}"
        
        all_params = tuple(data.values()) + params
        return self.execute_query(query, all_params)
    
    def delete(self, table: str, conditions: str, params: tuple = ()) -> Optional[int]:
        """Elimina registros de una tabla"""
        query = f"DELETE FROM {table} WHERE {conditions}"
        return self.execute_query(query, params)
    
    def delete_safe(self, table: str, conditions: str, params: tuple = ()) -> Optional[int]:
        """Elimina registros con confirmación previa"""
        count_query = f"SELECT COUNT(*) as total FROM {table} WHERE {conditions}"
        result = self.execute_query(count_query, params)
        
        if result and result[0]['total'] > 0:
            total = result[0]['total']
            confirm = input(f"¿Estás seguro de eliminar {total} registros? (s/n): ").lower()
            
            if confirm == 's':
                return self.delete(table, conditions, params)
            else:
                print("Operación cancelada")
                return 0
        return 0
    
    # ========== MÉTODOS DE TRANSACCIONES ==========
    
    def begin_transaction(self):
        """Inicia una transacción"""
        if self.connect():
            self.conn.start_transaction()
            print("🔄 Transacción iniciada")
    
    def commit_transaction(self):
        """Confirma la transacción"""
        if self.conn:
            self.conn.commit()
            print("✅ Transacción confirmada")
    
    def rollback_transaction(self):
        """Revierte la transacción"""
        if self.conn:
            self.conn.rollback()
            print("↩️ Transacción revertida")
    
    # ========== MÉTODOS DE UTILIDAD ==========
    
    def table_exists(self, table_name: str) -> bool:
        """Verifica si una tabla existe"""
        query = """
        SELECT COUNT(*) as count 
        FROM information_schema.tables 
        WHERE table_schema = %s AND table_name = %s
        """
        result = self.execute_query(query, (self.config['database'], table_name))
        return result[0]['count'] > 0 if result else False
    
    def get_table_schema(self, table_name: str) -> Optional[List[Dict]]:
        """Obtiene el esquema de una tabla"""
        query = """
        SELECT column_name, data_type, is_nullable, column_default, column_key
        FROM information_schema.columns 
        WHERE table_schema = %s AND table_name = %s
        ORDER BY ordinal_position
        """
        return self.execute_query(query, (self.config['database'], table_name))
    
    def get_table_size(self, table_name: str) -> Optional[Dict]:
        """Obtiene información del tamaño de una tabla"""
        query = """
        SELECT 
            table_rows as rows,
            ROUND(((data_length + index_length) / 1024 / 1024), 2) as size_mb,
            ROUND((data_length / 1024 / 1024), 2) as data_mb,
            ROUND((index_length / 1024 / 1024), 2) as index_mb
        FROM information_schema.tables 
        WHERE table_schema = %s AND table_name = %s
        """
        result = self.execute_query(query, (self.config['database'], table_name))
        return result[0] if result else None
    
    def get_all_tables(self) -> Optional[List[str]]:
        """Obtiene lista de todas las tablas"""
        query = """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = %s
        """
        result = self.execute_query(query, (self.config['database'],))
        if not result:
            return None
            
        tables = []
        for row in result:
            # Buscar la clave que coincida con 'table_name' sin importar mayúsculas/minúsculas
            key = next((k for k in row.keys() if k.lower() == 'table_name'), None)
            if key:
                tables.append(row[key])
        
        return tables
    
    def count_records(self, table: str, conditions: str = "", params: tuple = ()) -> Optional[int]:
        """Cuenta registros en una tabla"""
        query = f"SELECT COUNT(*) as total FROM {table}"
        if conditions:
            query += f" WHERE {conditions}"
            
        result = self.execute_query(query, params)
        return result[0]['total'] if result else None
    
    # ========== MÉTODOS DE BACKUP Y RESTORE ==========
    
    def backup_table(self, table_name: str, file_path: str) -> bool:
        """Exporta datos de una tabla a JSON"""
        try:
            data = self.select(table_name)
            if data:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, default=str, ensure_ascii=False)
                print(f"✅ Backup de {table_name} guardado en {file_path}")
                return True
        except Exception as e:
            print(f"❌ Error en backup: {e}")
        return False
    
    def restore_table(self, table_name: str, file_path: str) -> bool:
        """Restaura datos desde un archivo JSON"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if data and isinstance(data, list):
                result = self.insert_many(table_name, data)
                if result:
                    print(f"✅ Restaurados {result} registros en {table_name}")
                    return True
        except Exception as e:
            print(f"❌ Error en restore: {e}")
        return False
    
    # ========== MÉTODOS DE VALIDACIÓN ==========
    
    def validate_connection(self) -> bool:
        """Valida que la conexión esté funcionando"""
        try:
            result = self.execute_query("SELECT 1 as test")
            return result is not None and result[0]['test'] == 1
        except:
            return False
    
    def get_database_info(self) -> Optional[Dict]:
        """Obtiene información de la base de datos"""
        query = """
        SELECT 
            VERSION() as version,
            DATABASE() as current_db,
            USER() as user_info,
            CONNECTION_ID() as connection_id
        """
        result = self.execute_query(query)
        return result[0] if result else None
    
    # ========== MÉTODOS DE ÍNDICES ==========
    
    def create_index(self, table_name: str, index_name: str, columns: List[str]) -> bool:
        """Crea un índice en una tabla"""
        columns_str = ', '.join(columns)
        query = f"CREATE INDEX {index_name} ON {table_name} ({columns_str})"
        result = self.execute_query(query)
        return result is not None
    
    def drop_index(self, table_name: str, index_name: str) -> bool:
        """Elimina un índice"""
        query = f"DROP INDEX {index_name} ON {table_name}"
        result = self.execute_query(query)
        return result is not None
    
    def get_table_indexes(self, table_name: str) -> Optional[List[Dict]]:
        """Obtiene los índices de una tabla"""
        query = "SHOW INDEX FROM " + table_name
        return self.execute_query(query)
    
    # ========== MÉTODOS DE BÚSQUEDA AVANZADA ==========
    
    def search(self, table: str, search_term: str, columns: List[str], 
               exact_match: bool = False) -> Optional[List[Dict]]:
        """Busca en múltiples columnas"""
        if exact_match:
            conditions = " OR ".join([f"{col} = %s" for col in columns])
            params = tuple([search_term] * len(columns))
        else:
            conditions = " OR ".join([f"{col} LIKE %s" for col in columns])
            params = tuple([f"%{search_term}%"] * len(columns))
        
        return self.select(table, conditions, params)
    
    def paginate(self, table: str, page: int = 1, per_page: int = 10, 
                 conditions: str = "", params: tuple = (), 
                 order_by: str = "id") -> Dict:
        """Paginación de resultados"""
        offset = (page - 1) * per_page
        
        # Obtener total de registros
        total = self.count_records(table, conditions, params)
        
        # Obtener registros de la página
        query = f"SELECT * FROM {table}"
        if conditions:
            query += f" WHERE {conditions}"
        query += f" ORDER BY {order_by} LIMIT {per_page} OFFSET {offset}"
        
        data = self.execute_query(query, params)
        
        return {
            'data': data or [],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total or 0,
                'pages': ((total or 0) + per_page - 1) // per_page
            }
        }
    
    def close(self):
        """Método público para cerrar la conexión de forma limpia"""
        self.disconnect()
    
    def __del__(self):
        try:
            if hasattr(self, '_initialized') and self._initialized:
                self.disconnect()
        except:
            # Ignorar errores en el destructor para evitar excepciones no manejadas
            pass

