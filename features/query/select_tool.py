from core import BaseTool
from fastmcp import FastMCP
from typing import Union, List, Tuple, Optional, Dict, Any
from .services import execute_query

class QueryTool(BaseTool):
    def __init__(self, mcp: FastMCP):
        super().__init__(mcp)
    
    def register_tools(self):
        @self.mcp.tool(
            name="execute_query_tool",
            description="""
            Herramienta universal para ejecución de consultas SQL en bases de datos MySQL con métricas de rendimiento.
            
            Permite ejecutar cualquier tipo de consulta SQL con capacidades completas CRUD,
            operaciones complejas con joins, manejo seguro de parámetros y medición de tiempo de ejecución.
            
            Características principales:
            
            1. Operaciones CRUD completas:
               - SELECT: Consultas de lectura con resultados estructurados
               - INSERT: Inserción de nuevos registros
               - UPDATE: Modificación de datos existentes
               - DELETE: Eliminación de registros
            
            2. Consultas avanzadas:
               - Joins entre múltiples tablas
               - Subconsultas y consultas anidadas
               - Funciones de agregación (COUNT, SUM, AVG, etc.)
               - Agrupamiento (GROUP BY) y filtrado (HAVING)
            
            3. Métricas de rendimiento:
               - Tiempo de ejecución preciso en segundos
               - Medición incluso en casos de error
               - Útil para optimización de consultas lentas
            
            4. Manejo seguro de datos:
               - Protección contra inyección SQL mediante parámetros
               - Transacciones implícitas con commit/rollback automático
               - Validación de conexiones antes de ejecutar
            
            5. Flexibilidad en resultados:
               - Modo fetch_all: Retorna lista completa de resultados
               - Modo fetch_one: Retorna único registro
               - Para operaciones de escritura: Retorna número de filas afectadas
            
            Parámetros:
            - query (str): Consulta SQL completa a ejecutar
            - params (opcional): Tupla o lista con parámetros seguros
            - fetch_all (bool): True para múltiples resultados, False para único
            
            Retorna:
            Diccionario con:
            - result: 
              * SELECT: Lista de diccionarios o diccionario único
              * INSERT/UPDATE/DELETE: Número de filas afectadas
              * None en caso de error
            - execution_time (float): Tiempo de ejecución en segundos
            
            Casos de uso típicos:
            - Obtención de datos complejos con múltiples relaciones
            - Actualizaciones masivas con condiciones específicas
            - Inserciones de datos con validación previa
            - Eliminaciones controladas con parámetros dinámicos
            - Análisis de rendimiento de consultas
            - Identificación de cuellos de botella en la base de datos
            
            Advertencias de seguridad:
            - Nunca concatenar valores directamente en la consulta
            - Siempre usar parámetros para valores dinámicos
            - Validar permisos antes de ejecutar operaciones destructivas
            """,
            tags={"database", "mysql", "sql", "crud", "query", "join", "transaction", "performance"},
        )
        def execute_query_tool(
            query: str, 
            params: Optional[Union[Tuple, List]] = None,
            fetch_all: bool = True
        ) -> Dict[str, Any]:
    
            result, execution_time = execute_query(query, params, fetch_all)
            
            # Retornar como diccionario estructurado
            return {
                "result": result,
                "execution_time": execution_time,
                "query": query, 
                "success": result is not None
            }