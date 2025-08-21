from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStreamableHTTP
from dotenv import load_dotenv
import asyncio

load_dotenv()

# Inicializar el servidor y el agente
server = MCPServerStreamableHTTP(url='http://localhost:8000/mcp')
agent = Agent('deepseek:deepseek-chat', toolsets=[server])

async def main():
    
    result = await agent.run("""
    eliminame el cliente laura con id 2
    """)
    
    print(result.output)

if __name__ == "__main__":
    asyncio.run(main())