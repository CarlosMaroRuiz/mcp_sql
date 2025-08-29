from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStreamableHTTP
from dotenv import load_dotenv
import asyncio

load_dotenv()

# Inicializar el servidor y el agente
token_test = ""
# en el caso que no vaya el token este tronara ya que el servidor mcp tiene seguridad
server = MCPServerStreamableHTTP(
    url='http://localhost:8000/mcp',
    #para la seguridad
    headers={"Authorization":"Bearer "+token_test})
agent = Agent('google-gla:gemini-2.0-flash', toolsets=[server],system_prompt="")

async def main():
    
    result = await agent.run("""
     que herramientas tienes disponibles y cual es su proposito?
    """)
    
    print(result.output)

if __name__ == "__main__":
    asyncio.run(main())