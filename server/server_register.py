from fastmcp import FastMCP
from enums import enum_server
from fastmcp.server.auth.providers.jwt import JWTVerifier
from features import (
    InfoTool,
    QueryTool,
    LearningTool
)

# Configurar verificación con clave simétrica (HMAC)
verifier = JWTVerifier(
    public_key=enum_server.SECRET_KEY,
    issuer="servicio-autenticacion-interno",  # Identifica quién emite los tokens
    audience="mcp-api-interna",  # Identifica para quién es el token
    algorithm=enum_server.ALGORITHM
)

class ServerRegister:
    def __init__(self):
        
        self.mcp:FastMCP = FastMCP(name=enum_server.NAME,instructions=enum_server.INSTRUCTIONS,auth=verifier)
        InfoTool(self.mcp).register_tools()
        QueryTool(self.mcp).register_tools()
        LearningTool(self.mcp).register_tools()  


def create_server() -> ServerRegister:
    server = ServerRegister()
    return server.mcp