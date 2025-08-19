from core import MySQLConnector
from typing import Union, List, Dict, Tuple, Optional
import time

def execute_query(
    query: str, 
    params: Optional[Union[Tuple, List]] = None,
    fetch_all: bool = True
) -> Union[Tuple[Union[List[Dict], Dict, int, None], float], None]:
    """
    Ejecuta cualquier consulta SQL (CRUD, joins, etc.) usando MySQLConnector
    
    Args:
        query: Consulta SQL a ejecutar (SELECT, INSERT, UPDATE, DELETE, etc.)
        params: Parámetros para la consulta (previene inyección SQL)
        fetch_all: 
            - True para SELECT (devuelve lista de diccionarios)
            - False para obtener un solo resultado (diccionario)
    
    Returns:
        Tupla con:
        - Resultado de la consulta:
          * SELECT: Lista de diccionarios o diccionario único
          * INSERT/UPDATE/DELETE: Número de filas afectadas
          * None en caso de error
        - Tiempo de ejecución en segundos (float)
    """
    start_time = time.time()
    
    with MySQLConnector() as db:
        try:
            db.cursor.execute(query, params or ())
            
            if query.strip().upper().startswith(('INSERT', 'UPDATE', 'DELETE')):
                db.conn.commit()
                result = db.cursor.rowcount
            else:
                result = db.cursor.fetchall() if fetch_all else db.cursor.fetchone()
                result = db.normalize_keys(result)
                
            execution_time = time.time() - start_time
            return (result, execution_time)
                
        except Exception as e:
            execution_time = time.time() - start_time
            print(f"❌ Error en consulta: {e}")
            db.conn.rollback()
            return (None, execution_time)