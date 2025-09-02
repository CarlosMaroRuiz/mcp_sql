
### **Puntos clave para la generación y uso de tokens**

  - **Emisor (`iss`) y Audiencia (`aud`):** Estos valores deben coincidir **exactamente** con lo que espera el servidor de la plataforma (MCP) para que la petición no sea rechazada.

  - **Vigencia (`exp`):** El token debe estar **vigente**. Si la fecha de expiración ha pasado, el servidor lo rechazará.

  - **Ámbitos (`scopes`):** Los **`scopes`** permiten controlar qué acciones específicas puede realizar el usuario en el MCP, lo cual es esencial para el control de acceso.

  - **Algoritmo y clave secreta:** Es crucial usar el **algoritmo de encriptación** y la **clave secreta** correctos para firmar el token. Un error en cualquiera de estos elementos lo invalidará.

-----

### **Notas adicionales**

**Generación del token:**
El archivo `gen_token.py` muestra un ejemplo de cómo generar un token siguiendo los puntos anteriores.

**Envío en la cabecera HTTP:**
Recuerda enviar siempre el token en la cabecera de la petición HTTP usando el esquema **Bearer Token**. La sintaxis es la siguiente:

```
Authorization: Bearer <tu_token_aqui>
```

Te recomiendo revisar la documentación de cada cliente de MCP para más detalles sobre cómo implementar esto.
