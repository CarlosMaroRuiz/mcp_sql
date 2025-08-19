from abc import ABC, abstractmethod
from fastmcp import FastMCP

class BaseTool(ABC):
    def __init__(self, mcp: FastMCP):
        self.mcp = mcp

    @abstractmethod
    def register_tools(self):
        pass