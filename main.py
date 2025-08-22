from server.server_register import create_server
from core import MySQLConnector
from enums import enum_server
import sys

def main():
    db = MySQLConnector()
    if not db.validate_connection():
        print("    Verifique que:")
        print("    1. El servidor MySQL esté en ejecución")
        print("    2. Las credenciales en el archivo .env sean correctas")
        print("    3. La base de datos exista")
        print("    4. El usuario tenga permisos adecuados")
        sys.exit(1)
    
    server = create_server()
    
    server.run(transport="streamable-http", host=enum_server.HOST_SERVER, port=int(enum_server.PORT_SERVER))

if __name__ == "__main__":
    main()