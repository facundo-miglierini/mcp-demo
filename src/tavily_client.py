from langchain_core.runnables.config import RunnableConfig
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.graph import CompiledGraph
from mcp import ClientSession, StdioServerParameters

from mcp.client.stdio import stdio_client

from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent

from models import model

server_params = StdioServerParameters(
    command="node",
    args=["C:\\Users\\Acer\\Desktop\\Snoop\\tavily-mcp\\build\\index.js"]
)

class TavilyAgent:
    def __init__(self, server_params, checkpointer):
        self.server_params = server_params
        self.checkpointer = checkpointer
        self.session = None
        self.agent: CompiledGraph|None = None


    async def invoke(self, query: str, callback, thread_id: str|None = None) -> str:
        async with stdio_client(self.server_params) as (read, write):
            async with ClientSession(read, write) as session:

                config = RunnableConfig(
                    callbacks=callback,
                    recursion_limit=30,
                    configurable={ 
                        "thread_id": thread_id
                    }
                )

                # Initialize the connection
                self.session = session
                await self.session.initialize()

                # Get tools
                tools = await load_mcp_tools(self.session)

                # Create and run the agent
                self.agent = create_react_agent(model, tools, checkpointer=self.checkpointer)
                agent_response = await self.agent.ainvoke({"messages": query}, config=config)
                return agent_response['messages'][-1].content


checkpointer = MemorySaver()
agent = TavilyAgent(server_params, checkpointer)


# TESTING IN CONSOLE
async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # Get tools
            tools = await load_mcp_tools(session)

            # Create and run the agent
            agent = create_react_agent(model, tools)

            msg = ""

            while msg != "quit":
                msg = input("USER PROMPT (quit): ")
                agent_response = await agent.ainvoke({"messages": msg})
                print(f"AGENT RESPONSE: {agent_response['messages'][-1].content}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(run())
