import jwt
import datetime
from enums import enum_server

# Clave secreta compartida (DEBE ser la misma que usaste en el servidor MCP)


def generar_token(usuario_id, scopes=["read:data"]):
    """Genera un token JWT firmado con HMAC"""
    payload = {
        "sub": usuario_id,  # ID del usuario
        "iat": datetime.datetime.utcnow(),  # Fecha de emisión
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),  # Expiración
        #esta dos son la mas importantes
        "iss": "servicio-autenticacion-interno",  # Emisor (debe coincidir con el servidor MCP)
        "aud": "mcp-api-interna",  # Audiencia (debe coincidir con el servidor MCP)
        "scopes": scopes  # Permisos del usuario
    }
    
    token = jwt.encode(payload, enum_server.SECRET_KEY, algorithm=enum_server.ALGORITHM)
    return token

# Ejemplo de uso
token = generar_token("usuario123", ["read:data", "write:data"])
print(f"Token generado: {token}")