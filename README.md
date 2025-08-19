# MCP SQL

<div align="center">

![Python](https://img.shields.io/badge/Python-3.13+-blue.svg?style=for-the-badge&logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![FastMCP](https://img.shields.io/badge/FastMCP-2.11.3+-orange.svg?style=for-the-badge)

</div>

<p align="center">Servidor MCP para interactuar con bases de datos MySQL a través de LLMs con capacidades avanzadas de consulta, análisis y aprendizaje.</p>

<div align="center">
  <img src="https://raw.githubusercontent.com/jlowin/fastmcp/main/docs/docs/assets/fastmcp-hero-lockup.png" alt="FastMCP Logo" width="400">
</div>

## 🚀 Características Principales

- ⚡ **Ejecución de Consultas SQL**: Operaciones CRUD completas con métricas de rendimiento
- 📊 **Análisis de Esquemas**: Información detallada sobre la estructura de bases de datos
- 🧠 **Sistema de Aprendizaje**: Almacenamiento y recuperación de experiencias con consultas SQL
- ⏱️ **Métricas de Rendimiento**: Seguimiento preciso de tiempos de ejecución
- 💡 **Sugerencias Inteligentes**: Recomendaciones basadas en consultas previas exitosas

## 🧩 Estructura del Proyecto

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
└── README.md                   # Este archivo
```

## 📋 Requisitos

<table>
  <tr>
    <td>✅ Python 3.13+</td>
    <td>✅ MySQL Server</td>
  </tr>
</table>

### Dependencias Python

```
fastmcp>=2.11.3
mysql-connector-python>=9.4.0
pydantic-ai>=0.7.3
python-dotenv>=1.1.1
```

## 🔧 Instalación

<details open>
<summary><b>Paso 1: Clonar el repositorio</b></summary>

```bash
git clone https://github.com/tuusuario/mcp_sql.git
cd mcp_sql
```
</details>

<details open>
<summary><b>Paso 2: Configurar entorno virtual</b></summary>

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```
</details>

<details open>
<summary><b>Paso 3: Instalar dependencias</b></summary>

```bash
pip install -r requirements.txt
```
</details>

<details open>
<summary><b>Paso 4: Configurar variables de entorno</b></summary>

Crea un archivo `.env` con:

```
USER_BD=tuusuario
PASSWORD_BD=tupassword
HOST_DB=localhost
DATABASE_MYSQL=nombre_base_datos
```
</details>

## 🚀 Uso

### Iniciar el Servidor MCP

```bash
python main.py
```

Esto iniciará el servidor en `http://localhost:8000/mcp` usando transporte HTTP streamable.

### Ejecutar el Cliente de Prueba

```bash
python client_test.py
```

## 🔍 Herramientas Disponibles

<details open>
<summary><b>1. Herramienta de Consulta SQL</b></summary>

La herramienta `execute_query_tool` permite ejecutar cualquier tipo de consulta SQL:

```python
result = await client.call_tool("execute_query_tool", {
    "query": "SELECT * FROM clientes WHERE ciudad = 'Madrid'",
    "params": ["Madrid"],
    "fetch_all": True
})
```

**Características:**
- ✅ Soporte para operaciones CRUD completas
- 🔒 Consultas con parámetros (prevención de inyección SQL)
- ⏱️ Medición de tiempo de ejecución
- 🔄 Control sobre formato de resultados
</details>

<details open>
<summary><b>2. Herramienta de Análisis de Esquema</b></summary>

La herramienta `get_database_schema_info` proporciona información detallada sobre la estructura de la base de datos:

```python
schema_info = await client.call_tool("get_database_schema_info")
```

**Características:**
- 📋 Lista completa de tablas
- 🏗️ Estructura detallada de cada tabla
- 🔑 Claves primarias y foráneas
- 🔗 Relaciones entre tablas
- 📊 Estadísticas de la base de datos
</details>

<details open>
<summary><b>3. Herramientas de Aprendizaje</b></summary>

El sistema de aprendizaje incluye herramientas para registrar, recuperar y analizar experiencias con consultas SQL:

```python
# Guardar una nota de aprendizaje
await client.call_tool("add_query_learning_note", {
    "query": "SELECT * FROM clientes",
    "execution_time": 0.023,
    "rows_affected": 150,
    "success": True,
    "note": "Consulta básica para obtener todos los clientes",
    "tags": ["select", "clientes", "básica"]
})

# Buscar notas previas
results = await client.call_tool("search_query_learning_notes", {
    "search_term": "clientes"
})

# Obtener sugerencias basadas en fragmentos de consulta
suggestions = await client.call_tool("get_sql_query_suggestions", {
    "query_fragment": "SELECT * FROM cli",
    "context": "Buscando información de clientes"
})
```
</details>

## 📚 Ejemplo de Integración con LLM

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

---

<p align="center">
  <img src="https://img.shields.io/badge/Powered%20by-FastMCP-orange?style=flat-square" alt="Powered by FastMCP">
</p>
