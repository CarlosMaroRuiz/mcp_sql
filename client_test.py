from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStreamableHTTP
from dotenv import load_dotenv
import asyncio

load_dotenv()

# Inicializar el servidor y el agente
server = MCPServerStreamableHTTP(url='http://localhost:8000/mcp')
agent = Agent('google-gla:gemini-2.0-flash', toolsets=[server])

async def main():

        result = await agent.run("""traeme los clientes con su total de compras y
                                  cual consultas usaste para eso  pero antes de hacer revisa 
                                 como esta estructurada la tabla para que puedas ejecutar la consulta""")
    
        print(result.output)

if __name__ == "__main__":
    asyncio.run(main())