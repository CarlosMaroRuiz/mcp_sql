import json
import os
import time
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any, Union

# Configuración de ruta del archivo JSON
LEARNING_DIR = os.path.join("data", "learning")
LEARNING_FILE = os.path.join(LEARNING_DIR, "query_notes.json")

def _ensure_learning_dir():
    """Asegura que el directorio de aprendizaje exista"""
    if not os.path.exists(LEARNING_DIR):
        os.makedirs(LEARNING_DIR, exist_ok=True)

def _load_notes() -> List[Dict[str, Any]]:
    """Carga las notas de aprendizaje desde el archivo JSON"""
    _ensure_learning_dir()
    if not os.path.exists(LEARNING_FILE):
        return []
    
    try:
        with open(LEARNING_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def _save_notes(notes: List[Dict[str, Any]]) -> bool:
    """Guarda las notas de aprendizaje en el archivo JSON"""
    _ensure_learning_dir()
    try:
        with open(LEARNING_FILE, 'w', encoding='utf-8') as f:
            json.dump(notes, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error al guardar notas de aprendizaje: {e}")
        return False

def save_query_note(
    query: str,
    execution_time: float,
    rows_affected: int,
    success: bool,
    note: str,
    tags: List[str] = None,
    query_type: str = None
) -> Dict[str, Any]:
    """
    Guarda una nota de aprendizaje sobre una consulta SQL
    
    Args:
        query: Consulta SQL ejecutada
        execution_time: Tiempo de ejecución en segundos
        rows_affected: Número de filas afectadas o retornadas
        success: Si la consulta fue exitosa
        note: Anotación o aprendizaje sobre la consulta
        tags: Etiquetas para categorizar la consulta
        query_type: Tipo de consulta (SELECT, INSERT, UPDATE, DELETE, etc.)
        
    Returns:
        Dict con la información de la nota guardada
    """
    # Determinar automáticamente el tipo de consulta si no se proporciona
    if not query_type:
        query_upper = query.strip().upper()
        if query_upper.startswith("SELECT"):
            query_type = "SELECT"
        elif query_upper.startswith("INSERT"):
            query_type = "INSERT"
        elif query_upper.startswith("UPDATE"):
            query_type = "UPDATE"
        elif query_upper.startswith("DELETE"):
            query_type = "DELETE"
        else:
            query_type = "OTHER"
    
    # Crear nueva nota
    new_note = {
        "id": str(uuid.uuid4()),
        "query": query,
        "query_type": query_type,
        "execution_time": execution_time,
        "rows_affected": rows_affected,
        "success": success,
        "note": note,
        "tags": tags or [],
        "created_at": datetime.now().isoformat(),
        "complexity": _calculate_query_complexity(query)
    }
    
    # Cargar notas existentes, añadir la nueva y guardar
    notes = _load_notes()
    notes.append(new_note)
    _save_notes(notes)
    
    return new_note

def get_query_notes(
    limit: int = 50,
    offset: int = 0,
    query_type: str = None,
    success_only: bool = False
) -> Dict[str, Any]:
    """
    Obtiene notas de aprendizaje con paginación y filtros opcionales
    
    Args:
        limit: Número máximo de notas a retornar
        offset: Número de notas a saltar (para paginación)
        query_type: Filtrar por tipo de consulta
        success_only: Solo retornar consultas exitosas
        
    Returns:
        Dict con las notas y metadata de paginación
    """
    notes = _load_notes()
    
    # Aplicar filtros
    if query_type:
        notes = [n for n in notes if n.get("query_type") == query_type]
    if success_only:
        notes = [n for n in notes if n.get("success")]
    
    # Ordenar por fecha de creación (más recientes primero)
    notes.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    
    # Aplicar paginación
    paginated_notes = notes[offset:offset + limit] if notes else []
    
    return {
        "notes": paginated_notes,
        "pagination": {
            "total": len(notes),
            "offset": offset,
            "limit": limit,
            "has_more": (offset + limit) < len(notes)
        },
        "stats": {
            "success_rate": sum(1 for n in notes if n.get("success", False)) / len(notes) if notes else 0,
            "avg_execution_time": sum(n.get("execution_time", 0) for n in notes) / len(notes) if notes else 0,
            "count_by_type": {qtype: sum(1 for n in notes if n.get("query_type") == qtype) 
                             for qtype in set(n.get("query_type", "") for n in notes)}
        }
    }

def search_query_notes(
    search_term: str = None,
    tags: List[str] = None,
    min_success_rate: float = None,
    max_execution_time: float = None,
    date_from: str = None,
    date_to: str = None,
    limit: int = 50
) -> List[Dict[str, Any]]:
    """
    Busca notas de aprendizaje por diversos criterios
    
    Args:
        search_term: Término a buscar en consultas y notas
        tags: Filtrar por etiquetas específicas
        min_success_rate: Tasa mínima de éxito
        max_execution_time: Tiempo máximo de ejecución
        date_from: Fecha inicial (formato ISO)
        date_to: Fecha final (formato ISO)
        limit: Número máximo de resultados
        
    Returns:
        Lista de notas que coinciden con los criterios
    """
    notes = _load_notes()
    results = []
    
    for note in notes:
        # Filtrar por término de búsqueda
        if search_term and search_term.lower() not in note.get("query", "").lower() and search_term.lower() not in note.get("note", "").lower():
            continue
            
        # Filtrar por etiquetas
        if tags and not all(tag in note.get("tags", []) for tag in tags):
            continue
            
        # Filtrar por tiempo de ejecución
        if max_execution_time is not None and note.get("execution_time", 0) > max_execution_time:
            continue
            
        # Filtrar por fechas
        if date_from or date_to:
            note_date = datetime.fromisoformat(note.get("created_at", datetime.now().isoformat()))
            
            if date_from:
                from_date = datetime.fromisoformat(date_from)
                if note_date < from_date:
                    continue
                    
            if date_to:
                to_date = datetime.fromisoformat(date_to)
                if note_date > to_date:
                    continue
        
        results.append(note)
        
        if len(results) >= limit:
            break
    
    return results

def get_query_suggestions(
    query_fragment: str,
    context: str = None,
    limit: int = 5
) -> Dict[str, Any]:
    """
    Obtiene sugerencias de consultas basadas en consultas anteriores similares
    
    Args:
        query_fragment: Fragmento de consulta para buscar similares
        context: Contexto opcional para mejorar las sugerencias
        limit: Número máximo de sugerencias
        
    Returns:
        Dict con sugerencias y estadísticas de rendimiento
    """
    notes = _load_notes()
    
    # Filtrar solo consultas exitosas
    successful_notes = [n for n in notes if n.get("success", False)]
    
    # Si no hay consultas exitosas, retornar vacío
    if not successful_notes:
        return {
            "suggestions": [],
            "message": "No hay consultas previas para generar sugerencias"
        }
    
    # Buscar consultas similares
    query_fragment = query_fragment.lower()
    
    # Función para calcular similitud simple
    def calculate_similarity(note):
        query = note.get("query", "").lower()
        note_text = note.get("note", "").lower()
        
        # Mayor peso si coincide con la consulta
        query_score = 3 if query_fragment in query else 0
        
        # Peso adicional si coincide con la nota
        note_score = 1 if query_fragment in note_text else 0
        
        # Considerar el contexto si se proporciona
        context_score = 0
        if context and context.lower() in note_text:
            context_score = 2
            
        return query_score + note_score + context_score
    
    # Filtrar y ordenar por relevancia
    similar_queries = [(note, calculate_similarity(note)) for note in successful_notes]
    similar_queries = [(note, score) for note, score in similar_queries if score > 0]
    similar_queries.sort(key=lambda x: (x[1], -float(x[0].get("execution_time", 0))), reverse=True)
    
    # Tomar las mejores sugerencias
    top_suggestions = similar_queries[:limit]
    
    # Formatear resultados
    suggestions = []
    for note, score in top_suggestions:
        suggestions.append({
            "query": note.get("query"),
            "execution_time": note.get("execution_time"),
            "rows_affected": note.get("rows_affected"),
            "created_at": note.get("created_at"),
            "note": note.get("note"),
            "tags": note.get("tags", []),
            "relevance_score": score
        })
    
    return {
        "suggestions": suggestions,
        "stats": {
            "total_matches": len(similar_queries),
            "avg_execution_time": sum(note.get("execution_time", 0) for note, _ in top_suggestions) / len(top_suggestions) if top_suggestions else 0
        }
    }

def _calculate_query_complexity(query: str) -> str:
    """
    Calcula la complejidad de una consulta SQL
    
    Args:
        query: Consulta SQL a analizar
        
    Returns:
        String con nivel de complejidad ("simple", "medium", "complex")
    """
    query_upper = query.strip().upper()
    
    # Contar características que indican complejidad
    complexity_score = 0
    
    # Joins aumentan complejidad
    if " JOIN " in query_upper:
        join_count = query_upper.count(" JOIN ")
        complexity_score += join_count * 2
    
    # Subconsultas aumentan complejidad
    if "(" in query and "SELECT" in query_upper:
        subquery_count = query_upper.count("SELECT") - 1
        complexity_score += subquery_count * 3
    
    # Agrupamiento y ordenamiento
    if " GROUP BY " in query_upper:
        complexity_score += 1
    if " ORDER BY " in query_upper:
        complexity_score += 1
    
    # Funciones agregadas
    for func in ["COUNT(", "SUM(", "AVG(", "MAX(", "MIN("]:
        if func in query_upper:
            complexity_score += 1
    
    # Determinar nivel basado en puntuación
    if complexity_score <= 2:
        return "simple"
    elif complexity_score <= 5:
        return "medium"
    else:
        return "complex"