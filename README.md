# MCP SQL

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg?style=for-the-badge&logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![FastMCP](https://img.shields.io/badge/FastMCP-2.11.3+-orange.svg?style=for-the-badge)

</div>

<p align="center">Servidor MCP para interactuar con bases de datos MySQL a través de LLMs con capacidades de consulta, análisis y aprendizaje.</p>

## ¿Qué es MCP SQL?

`mcp_sql` conecta tu base de datos MySQL con un LLM a través del estándar MCP. Esto permite que una IA ejecute consultas seguras, analice tu esquema y aprenda de tus queries pasadas para sugerir nuevas.

A diferencia de conectarse directamente con un driver MySQL, `mcp_sql` ofrece:
- **Capa de abstracción segura** entre tus datos y el LLM
- **Análisis automático de esquemas** sin escribir queries complejas
- **Sistema de aprendizaje** que mejora con cada consulta
- **Métricas de rendimiento** para optimizar tus bases de datos
- **Sugerencias inteligentes** basadas en consultas exitosas previas

## Arquitectura

<div align="center">

```
LLM  →  MCP Server (mcp_sql)  →  MySQL  
                ↘ Aprendizaje (notas, métricas, sugerencias)
```

</div>

El flujo de trabajo es simple pero potente:
1. El LLM envía una solicitud a través del protocolo MCP
2. El servidor MCP SQL procesa la solicitud y la convierte en operaciones MySQL seguras
3. Los resultados son retornados al LLM en un formato optimizado
4. Cada interacción alimenta el sistema de aprendizaje para mejorar futuras consultas

## Características Principales

- **Ejecución de Consultas SQL**: Operaciones CRUD completas con métricas de rendimiento
- **Análisis de Esquemas**: Información detallada sobre la estructura de bases de datos
- **Sistema de Aprendizaje**: Almacenamiento y recuperación de experiencias con consultas SQL
- **Métricas de Rendimiento**: Seguimiento preciso de tiempos de ejecución
- **Sugerencias Inteligentes**: Recomendaciones basadas en consultas previas exitosas

## Estructura del Proyecto

```
mcp_sql/
├── core/                       # Componentes fundamentales
│   ├── __init__.py
│   ├── base_tool.py            # Clase base para herramientas MCP
│   └── conector_mysql.py       # Conector MySQL con funcionalidades avanzadas
├── enums/                      # Enumeraciones y constantes
│   ├── __init__.py
│   └── enum_server.py          # Configuración del servidor
├── features/                   # Herramientas y funcionalidades
│   ├── information/            # Análisis de esquema de BD
│   ├── learning/               # Sistema de aprendizaje de consultas
│   ├── query/                  # Ejecución de consultas SQL
│   └── __init__.py
├── server/                     # Configuración del servidor MCP
│   ├── __init__.py
│   └── server_register.py      # Registro de herramientas
├── data/                       # Directorio para almacenamiento de datos
│   └── learning/               # Almacenamiento de experiencias de aprendizaje
├── main.py                     # Punto de entrada principal
├── client_test.py              # Cliente de prueba
├── requirements.txt            # Dependencias del proyecto
├── pyproject.toml              # Configuración del proyecto
└── README.md                   # Este archivo
```

## Requisitos

<table>
  <tr>
    <td>✅ Python 3.11+</td>
    <td>✅ MySQL Server</td>
    <td>✅ uv (instalador y gestor de entornos)</td>
  </tr>
</table>

### Dependencias Python

```
fastmcp>=2.11.3
mysql-connector-python>=9.4.0
pydantic-ai>=0.7.3
python-dotenv>=1.1.1
```

## Instalación

<details open>
<summary><b>Paso 1: Clonar el repositorio</b></summary>

```bash
git clone https://github.com/CarlosMaroRuiz/mcp_sql.git
cd mcp_sql
```
</details>

<details open>
<summary><b>Paso 2: Instalar uv (si no lo tienes)</b></summary>

```bash
# En Windows con PowerShell
iwr https://astral.sh/uv/install.ps1 -useb | iex

# En Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh
```
</details>

<details open>
<summary><b>Paso 3: Configurar variables de entorno</b></summary>

Crea un archivo `.env` con:

```
USER_BD=tuusuario
PASSWORD_BD=tupassword
HOST_DB=localhost
DATABASE_MYSQL=nombre_base_datos
GOOGLE_API_KEY=tu_clave_api
```

Nota: Es necesario adquirir una clave API de Google para el proyecto. Esta clave se utiliza para ciertas funcionalidades del sistema.
</details>

## Uso

### Iniciar el Servidor MCP

```bash
uv run main.py
```

Esto ejecutará el script principal utilizando el entorno gestionado por uv, iniciando el servidor en `http://localhost:8000/mcp` con transporte HTTP streamable. Las dependencias se instalarán automáticamente.

### Ejecutar el Cliente de Prueba

```bash
uv run client_test.py
```

Con este comando, uv ejecuta el script de prueba utilizando el entorno Python correcto y todas las dependencias instaladas.

## Herramientas Disponibles

<details open>
<summary><b>1. Herramienta de Consulta SQL</b></summary>

La herramienta `execute_query_tool` permite ejecutar cualquier tipo de consulta SQL con soporte para operaciones CRUD completas, consultas con parámetros para prevención de inyección SQL, medición de tiempo de ejecución y control sobre formato de resultados.
</details>

<details open>
<summary><b>2. Herramienta de Análisis de Esquema</b></summary>

La herramienta `get_database_schema_info` proporciona información detallada sobre la estructura de la base de datos, incluyendo lista completa de tablas, estructura detallada de cada tabla, claves primarias y foráneas, relaciones entre tablas y estadísticas de la base de datos.
</details>

<details open>
<summary><b>3. Herramientas de Aprendizaje</b></summary>

El sistema de aprendizaje incluye herramientas para registrar, recuperar y analizar experiencias con consultas SQL. Permite guardar notas de aprendizaje, buscar notas previas y obtener sugerencias basadas en fragmentos de consulta.
</details>

## Ejemplo de Integración con LLM

<div align="center">
  <img src="https://img.shields.io/badge/Compatible%20con-LLMs%20via%20MCP-blueviolet?style=for-the-badge" alt="Compatible con LLMs">
</div>

```python
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStreamableHTTP

# Configurar el servidor y agente
server = MCPServerStreamableHTTP(url='http://localhost:8000/mcp')
agent = Agent('nombre-del-modelo', toolsets=[server])

# Ejecutar una tarea
result = await agent.run("""
    Analiza la estructura de la base de datos y muestra todas las tablas
    que tienen relación con la tabla 'clientes'.
""")
```