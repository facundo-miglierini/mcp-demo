# MCP Client

Demo de Cliente MCP que hace uso del Servidor MCP provisto por Tavily (https://github.com/tavily-ai/tavily-mcp/tree/main).

Permite realizar búsquedas web y extraer el contenido de una URL especificada. 

Este cliente MCP utiliza **uv** como gestor de paquetes para instalar sus dependencias.

## Requisitos previos

- Tener instalado **uv** package manager: https://docs.astral.sh/uv/getting-started/installation/
- Tener instalado **node**: https://nodejs.org/en/download

## Instalación del Servidor MCP Tavily

Clonar el repositorio del servidor. En este caso, Tavily AI:
```bash
https://github.com/tavily-ai/tavily-mcp
```


## Instalación del Servidor MCP Google Calendar

Clonar el repositorio del servidor. En este caso, Google Calendar:
```bash
https://github.com/nspady/google-calendar-mcp
```

## Instalación del Servidor MCP Spotify

Clonar el repositorio del servidor. En este caso, Spotify:
```bash
https://github.com/varunneal/spotify-mcp
```

## Instalación del Cliente MCP

1. Clonar este repositorio:
```bash
git clone git@github.com:facundo-miglierini/mcp-demo.git
cd mcp-demo
```

2. Instalar las dependencias con **uv**:
```bash
uv build
uv venv
```

3. Modificar la variable *server_params* con los siguientes valores:
```python
server_params = StdioServerParameters(
    command="node",
    args=["/{SERVER_DIR}/tavily-mcp/build/index.js"]
)
```

Donde *SERVER_DIR* es el directorio donde se encuentra el Servidor MCP instalado.

## Uso

Dentro de la carpeta del cliente MCP, activar el entorno virtual:

```bash
source .venv/bin/activate
```

### Streamlit 

Puede interactuarse desde una interfaz provista por Streamlit:
```bash
python -m streamlit run src/streamlit.py
```

### Consola

También puede utilizarse desde la consola:
```bash
python src/tavily_client.py
```
