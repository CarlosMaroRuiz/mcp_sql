from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStreamableHTTP
from dotenv import load_dotenv
import asyncio

load_dotenv()

# Inicializar el servidor y el agente
server = MCPServerStreamableHTTP(url='http://localhost:8000/mcp')
agent = Agent('google-gla:gemini-2.0-flash', toolsets=[server])

async def main():
    print("Consultando clientes con su total de compras...\n")
    
    result = await agent.run("""
    Por favor, realiza lo siguiente:
    
    1. Explora la estructura de la base de datos para entender cómo están relacionadas las tablas.
    2. Crea y ejecuta una consulta SQL que muestre los clientes con su total de compras.
    3. Guarda un aprendizaje sobre la consulta que ejecutaste, incluyendo:
       - Notas sobre por qué elegiste ese enfoque
       - El tiempo de ejecución
       - Etiquetas relevantes para categorizar la consulta
    4. Basado en tu experiencia, sugiere una consulta mejorada para el futuro.
    
    Explica tu proceso de pensamiento en cada paso.
    """)
    
    print(result.output)

if __name__ == "__main__":
    asyncio.run(main())