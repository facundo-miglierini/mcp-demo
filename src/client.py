from langchain_core.runnables.config import RunnableConfig
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.graph import CompiledGraph
from mcp import ClientSession, StdioServerParameters

from mcp.client.stdio import stdio_client

from langchain_mcp_adapters.client import MultiServerMCPClient, StdioConnection, TypedDict
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent

from models import model

calendar_server_params: StdioConnection = {
    "command": "node",
    "args": ["/home/facundo/google-calendar-mcp/build/index.js"],
    "transport": "stdio",
    "env": None,
    "encoding": "utf-8",
    "encoding_error_handler": "replace"
}

tavily_server_params: StdioConnection = {
    "command": "node",
    "args": ["/home/facundo/tavily-mcp/build/index.js"],
    "transport": "stdio",
    "env": None,
    "encoding": "utf-8",
    "encoding_error_handler": "replace"
}

spotify_server_params: StdioConnection = {
    "command": "uv",
    "args": ["--directory", "/home/facundo/spotify_mcp", "run", "spotify-mcp"],
    "transport": "stdio",
    "env": None,
    "encoding": "utf-8",
    "encoding_error_handler": "replace"
}

"""
    "command": "uv",
    "args": [
      "--directory",
      "/path/to/spotify_mcp",
      "run",
      "spotify-mcp"
    ],
    """

class Agent:
    def __init__(self):
        self.checkpointer = MemorySaver()
        self.session = None
        self.agent: CompiledGraph|None = None


    async def invoke(self, query: str, callback, thread_id: str|None = None) -> str:

        async with MultiServerMCPClient(
            {
                "tavily": tavily_server_params,
                "spotify": spotify_server_params,
                "google-calendar" : calendar_server_params,
            } 
        ) as client:
            config = RunnableConfig(
                callbacks=callback,
                recursion_limit=30,
                configurable={ 
                    "thread_id": thread_id
                }
            )
            tools = client.get_tools()
            # Create and run the agent
            self.agent = create_react_agent(model, tools, checkpointer=self.checkpointer)
            agent_response = await self.agent.ainvoke({"messages": query}, config=config)
            return agent_response['messages'][-1].content

agent = Agent()

async def run():
    async with MultiServerMCPClient(
        {
            "tavily": tavily_server_params,
            "spotify": spotify_server_params,
            "google-calendar" : calendar_server_params,
        } 
    ) as client:
        user_prompt = ""
        
        # Supervisor call
        checkpointer = MemorySaver()
        
        tools = client.get_tools()

        agent = create_react_agent(model, tools, checkpointer=checkpointer)
        while True:
            user_prompt = input("User prompt: ")
            if user_prompt == "quit":
                break
            agent_response = await agent.ainvoke({"messages": user_prompt}, config={"configurable":{"thread_id":"1"}})
            print(f"Respuesta: {agent_response["messages"][-1].content}")

if __name__ == "__main__":
    import asyncio

    asyncio.run(run())
