# Create server parameters for stdio connection
from mcp import ClientSession, StdioServerParameters

from mcp.client.stdio import stdio_client

from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent

from models import model

server_params = StdioServerParameters(
    command="node",
    args=["/home/facundo/tavily-mcp/build/index.js"]
)

async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # Get tools
            tools = await load_mcp_tools(session)

            # Create and run the agent
            agent = create_react_agent(model, tools)
            #agent_response = await agent.ainvoke({"messages": "Cuándo se elige el nuevo papa?"})
            agent_response = await agent.ainvoke({"messages": "Qué contiene el siguiente link? https://github.com/varunneal/spotify-mcp"})
            print(f"AGENT RESPONSE: {agent_response['messages'][-1].content}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(run())
