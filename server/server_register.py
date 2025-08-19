from fastmcp import FastMCP
from enums import enum_server
from features import (
    InfoTool,
    QueryTool,
    LearningTool
)


class ServerRegister:
    def __init__(self):
        self.mcp:FastMCP = FastMCP(name=enum_server.NAME,instructions=enum_server.INSTRUCTIONS)
        InfoTool(self.mcp).register_tools()
        QueryTool(self.mcp).register_tools()
        LearningTool(self.mcp).register_tools()  


def create_server() -> ServerRegister:
    server = ServerRegister()
    return server.mcp