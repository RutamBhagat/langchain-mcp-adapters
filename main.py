import asyncio

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
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
    async with stdio_client(stdio_server_params) as (read, write):
        async with ClientSession(read_stream=read, write_stream=write) as session:
            await session.initialize()
            print("Initialized")
            tools = await load_mcp_tools(session)
            agent = create_react_agent(llm, tools)

            result = await agent.ainvoke(
                {
                    "messages": [
                        HumanMessage(
                            content="Calculate: (abs(-15) + sqrt(64)) * (5! % 7)"
                        )
                    ]
                }
            )

            math_question = "Calculate: (abs(-15) + sqrt(64)) * (5! % 7)"

            math_answer = 23

            print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
