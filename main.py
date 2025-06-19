import asyncio

from dotenv import load_dotenv
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

stdio_server_params = StdioServerParameters(
    command="python",
    args=[
        "/home/voldemort/Desktop/Code/python_projects/mcp-servers/langchain-mcp-adapters/servers/math-server.py"
    ],
)


async def main():
    print("Hello from mcp-crash-course!")


if __name__ == "__main__":
    asyncio.run(main())
