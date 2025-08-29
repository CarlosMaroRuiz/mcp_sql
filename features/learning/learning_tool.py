from core import BaseTool
from fastmcp import FastMCP
from typing import List, Dict, Any, Optional
from .services import (
    save_query_note, 
    get_query_notes, 
    search_query_notes, 
    get_query_suggestions
)

class LearningTool(BaseTool):
    def __init__(self, mcp: FastMCP):
        super().__init__(mcp)
    
    def register_tools(self):
        @self.mcp.tool(
            name="add_query_learning_note",
            description="""
            Herramienta para registrar aprendizajes sobre consultas SQL ejecutadas.
            
            Permite guardar anotaciones sobre consultas realizadas a la base de datos,
            incluyendo métricas de rendimiento, resultados y observaciones de aprendizaje.
            Estas anotaciones se almacenan para su posterior análisis y mejora continua.
            
            Características principales:
            
            1. Registro de aprendizaje:
               - Almacena la consulta SQL completa
               - Registra métricas de rendimiento (tiempo de ejecución)
               - Documenta el éxito o fracaso de la consulta
               - Guarda el número de filas afectadas o retornadas
            
            2. Anotaciones personalizadas:
               - Observaciones sobre el comportamiento de la consulta
               - Patrones identificados
               - Mejoras potenciales
               - Problemas encontrados
            
            3. Categorización:
               - Etiquetas personalizadas para clasificar consultas
               - Identificación automática del tipo de consulta (SELECT, INSERT, etc.)
               - Evaluación de complejidad
            
            4. Trazabilidad:
               - ID único para cada anotación
               - Timestamp de creación
               - Historial de aprendizaje organizado
            
            Ideal para:
            - Registrar aprendizajes sobre consultas exitosas
            - Documentar errores y soluciones
            - Crear una base de conocimiento de SQL
            - Mejorar iterativamente la calidad de las consultas
            """,
            tags={"learning", "mysql", "sql", "documentation", "optimization"}
        )
        def add_query_learning_note(
            query: str,
            execution_time: float,
            rows_affected: int,
            success: bool,
            note: str,
            tags: List[str] = None,
            query_type: str = None
        ) -> Dict[str, Any]:
            """
            Guarda una nota de aprendizaje sobre una consulta SQL ejecutada.
            
            Args:
                query: La consulta SQL que se ejecutó
                execution_time: Tiempo de ejecución en segundos
                rows_affected: Número de filas afectadas o retornadas
                success: Si la consulta fue exitosa (True) o falló (False)
                note: Anotación o aprendizaje sobre la consulta
                tags: Lista de etiquetas para categorizar la consulta
                query_type: Tipo de consulta (opcional, se detecta automáticamente)
                
            Returns:
                Información de la nota guardada
            """
            return save_query_note(
                query=query,
                execution_time=execution_time,
                rows_affected=rows_affected,
                success=success,
                note=note,
                tags=tags,
                query_type=query_type
            )
        
        @self.mcp.resource(
            uri="schema://learning/query_history/{limit}",
            name="get_query_learning_history",
            description="""
            ADVERTENCIA: Antes de iniciar el proceso de query, tenga en cuenta que esta operación 
            puede consumir recursos significativos y tardar desde segundos hasta minutos, según 
            el tamaño y la carga de la base de datos. Se recomienda usar en momentos de baja 
            demanda o con bases de datos de tamaño moderado.
            
            Herramienta para recuperar el historial de aprendizaje sobre consultas SQL.
            
            Permite acceder al registro histórico de consultas y sus anotaciones asociadas,
            con opciones de filtrado y paginación para facilitar el análisis y la búsqueda
            de patrones o soluciones anteriores.
            
            Características principales:
            
            1. Acceso al historial:
               - Consultas y anotaciones almacenadas
               - Métricas de rendimiento históricas
               - Experiencias documentadas
            
            2. Opciones de filtrado:
               - Por tipo de consulta (SELECT, INSERT, etc.)
               - Por resultado (exitosas/fallidas)
               - Por rango de fechas
            
            3. Paginación:
               - Control sobre cantidad de resultados
               - Navegación por grandes conjuntos de datos
            
            4. Estadísticas agregadas:
               - Tasa de éxito global
               - Tiempos promedio de ejecución
               - Distribución por tipo de consulta
            
            Ideal para:
            - Revisar experiencias pasadas
            - Analizar tendencias de rendimiento
            - Aprender de patrones históricos
            - Encontrar soluciones a problemas recurrentes
            """,
            tags={"learning", "history", "mysql", "sql", "analysis"}
        )
        def get_query_learning_history(
            limit: int,
            offset: int = 0,
            query_type: str = None,
            success_only: bool = False
        ) -> Dict[str, Any]:
            """
            Obtiene el historial de aprendizaje de consultas SQL con opciones de filtrado.
            
            Args:
                limit: Número máximo de notas a retornar
                offset: Índice inicial para paginación
                query_type: Filtrar por tipo de consulta (SELECT, INSERT, etc.)
                success_only: Si es True, solo retorna consultas exitosas
                
            Returns:
                Notas de aprendizaje y estadísticas
            """
            return get_query_notes(
                limit=limit,
                offset=offset,
                query_type=query_type,
                success_only=success_only
            )
        
        @self.mcp.tool(
            name="search_query_learning_notes",
            description="""
            Herramienta de búsqueda avanzada en el repositorio de aprendizaje SQL.
            
            Permite encontrar notas de aprendizaje específicas mediante criterios
            de búsqueda flexibles, facilitando la recuperación de conocimientos
            previos y experiencias documentadas con consultas similares.
            
            Características principales:
            
            1. Búsqueda por contenido:
               - En el texto de las consultas
               - En las anotaciones y observaciones
               - Coincidencias parciales
            
            2. Filtros combinados:
               - Por etiquetas asignadas
               - Por rango de tiempo de ejecución
               - Por rango de fechas
               - Por tasa de éxito
            
            3. Resultados relevantes:
               - Ordenados por coincidencia
               - Limitados a la cantidad requerida
               - Con toda la información asociada
            
            4. Flexibilidad:
               - Combinación de múltiples criterios
               - Búsqueda por similitud semántica
            
            Ideal para:
            - Encontrar soluciones a problemas específicos
            - Recuperar técnicas utilizadas anteriormente
            - Identificar patrones en tipos similares de consultas
            - Revisar experiencias con estructuras de datos específicas
            """,
            tags={"learning", "search", "mysql", "sql", "knowledge retrieval"}
        )
        def search_query_learning_notes(
            search_term: str = None,
            tags: List[str] = None,
            min_success_rate: float = None,
            max_execution_time: float = None,
            date_from: str = None,
            date_to: str = None,
            limit: int = 50
        ) -> List[Dict[str, Any]]:
            """
            Busca notas de aprendizaje por diversos criterios.
            
            Args:
                search_term: Término a buscar en consultas y notas
                tags: Lista de etiquetas para filtrar
                min_success_rate: Tasa mínima de éxito (0.0 a 1.0)
                max_execution_time: Tiempo máximo de ejecución en segundos
                date_from: Fecha inicial en formato ISO (YYYY-MM-DD)
                date_to: Fecha final en formato ISO (YYYY-MM-DD)
                limit: Número máximo de resultados
                
            Returns:
                Lista de notas que coinciden con los criterios
            """
            return search_query_notes(
                search_term=search_term,
                tags=tags,
                min_success_rate=min_success_rate,
                max_execution_time=max_execution_time,
                date_from=date_from,
                date_to=date_to,
                limit=limit
            )
        
        @self.mcp.resource(
            uri="schema://learning/query_suggestions/{query_fragment}",
            name="get_query_suggestions",
            description="""
            ADVERTENCIA: Antes de iniciar el proceso de query, tenga en cuenta que esta operación 
            puede consumir recursos significativos y tardar desde segundos hasta minutos, según 
            el tamaño y la carga de la base de datos. Se recomienda usar en momentos de baja 
            demanda o con bases de datos de tamaño moderado.
            
            Herramienta de sugerencias inteligentes basadas en experiencias SQL previas.
            
            Proporciona recomendaciones de consultas SQL basadas en fragmentos
            de consulta y el historial de aprendizaje, ayudando a mejorar la
            eficiencia y calidad de nuevas consultas mediante el aprovechamiento
            de experiencias exitosas anteriores.
            
            Características principales:
            
            1. Sugerencias contextuales:
               - Basadas en fragmentos de consulta existentes
               - Considerando el contexto específico
               - Priorizando consultas similares exitosas
            
            2. Análisis de rendimiento:
               - Enfoque en consultas históricamente rápidas
               - Estadísticas de tiempos de ejecución
               - Métricas de impacto (filas afectadas)
            
            3. Relevancia personalizada:
               - Ordenamiento por similitud
               - Puntuaciones de relevancia transparentes
               - Filtrado automático de sugerencias irrelevantes
            
            4. Información completa:
               - Consultas SQL completas sugeridas
               - Notas asociadas a cada sugerencia
               - Métricas de rendimiento esperado
            
            Ideal para:
            - Mejorar la velocidad de desarrollo SQL
            - Promover patrones de consulta eficientes
            - Evitar errores cometidos anteriormente
            - Acelerar el aprendizaje de SQL
            """,
            tags={"learning", "suggestions", "mysql", "sql", "optimization", "ai"}
        )
        def get_sql_query_suggestions(
            query_fragment: str,
            context: str = None,
            limit: int = 5
        ) -> Dict[str, Any]:
            """
            Obtiene sugerencias de consultas basadas en un fragmento y experiencias previas.
            
            Args:
                query_fragment: Fragmento de consulta SQL para buscar similares
                context: Descripción del contexto para mejorar las sugerencias
                limit: Número máximo de sugerencias a retornar
                
            Returns:
                Sugerencias de consultas con métricas asociadas
            """
            return get_query_suggestions(
                query_fragment=query_fragment,
                context=context,
                limit=limit
            )