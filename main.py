from server.server_register import create_server

def main():
    server = create_server()
    server.run(transport="streamable-http")
main()