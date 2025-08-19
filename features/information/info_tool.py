from core import BaseTool
from fastmcp import FastMCP
from .services import get_information


class InfoTool(BaseTool):
    def __init__(self, mcp: FastMCP):
        super().__init__(mcp)
    
    def register_tools(self):
        @self.mcp.tool(
            name="get_database_schema_info",
            description="""
            Herramienta integral para análisis de esquemas de bases de datos MySQL.
            
            Obtiene y analiza la estructura completa de la base de datos conectada,
            proporcionando información detallada sobre:
            
            1. Metadatos de la base de datos:
               - Nombre de la base de datos
               - Versión de MySQL
               - Información de conexión
            
            2. Estructura de tablas:
               - Lista completa de tablas
               - Número total de tablas
               - Esquema detallado de cada tabla (columnas, tipos, restricciones)
            
            3. Claves y relaciones:
               - Claves primarias por tabla
               - Claves foráneas y sus referencias
               - Mapa completo de relaciones entre tablas
               - Estadísticas de relaciones (tablas con más conexiones)
            
            4. Análisis adicional:
               - Tamaño de tablas (opcional)
               - Índices disponibles (opcional)
            
            Ideal para:
            - Documentación automática de bases de datos
            - Análisis de arquitectura de datos
            - Identificación de patrones de diseño
            - Migración de bases de datos
            - Optimización de consultas
            """,
            tags={"database", "schema", "mysql", "metadata", "analysis", "documentation"},
        )
        def get_database_schema_info():

            return get_information()