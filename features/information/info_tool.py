from core import BaseTool
from fastmcp import FastMCP
from .services import get_information


class InfoTool(BaseTool):
    def __init__(self, mcp: FastMCP):
        super().__init__(mcp)
    
    def register_tools(self):
      @self.mcp.resource(
            uri="schema://database/info",
            name="get_database_schema_info",
            description="""
            Proporciona el esquema completo de una base de datos MySQL, incluyendo tablas, 
            columnas, tipos y relaciones.
            """,
            tags={"database", "schema", "mysql", "metadata", "analysis", "documentation"},
            )
      def get_database_schema_info():
         return get_information()