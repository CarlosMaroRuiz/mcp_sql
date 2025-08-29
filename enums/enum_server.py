#clase que contiene datos del servidor mcp como lo es nombre del server mcp y instrucciones
from dotenv import load_dotenv
import os
load_dotenv()
class EnumServer:
    def __init__(self):
        self.NAME:str = "MCP_SQL"
        self.INSTRUCTIONS :str = "Por el momento no hay instrucciones"
        self.HOST_SERVER = os.getenv("HOST_SERVER")
        self.PORT_SERVER = os.getenv("PORT_SERVER")
        self.SECRET_KEY = os.getenv("SECRET_KEY")
        self.ALGORITHM = os.getenv("ALGORITHM")
    

enum_server = EnumServer()