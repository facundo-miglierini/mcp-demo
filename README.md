# MCP Client

Demo de Cliente MCP que hace uso del Servidor MCP provisto por Tavily (https://github.com/tavily-ai/tavily-mcp/tree/main).

Permite realizar búsquedas web y extraer el contenido de una URL especificada. 

Este cliente MCP utiliza **uv** como gestor de paquetes para instalar sus dependencias.

## Requisitos previos

- Tener instalado **uv** package manager: https://docs.astral.sh/uv/getting-started/installation/
- Tener instalado **node**: https://nodejs.org/en/download

## Instalación del Cliente MCP

1. Clonar este repositorio:
```bash
git clone git@github.com:facundo-miglierini/mcp-demo.git
cd mcp-demo
```

2. Instalar las dependencias con **uv**:
```bash
uv install
uv venv
```

## Instalación del Servidor MCP

1. Clonar el repositorio del servidor. En este caso, Tavily AI:
```bash
git clone git@github.com:tavily-ai/tavily-mcp.git
cd tavily-mcp
```

2. Compilar el código del servidor:
```bash
npm run build
```

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
