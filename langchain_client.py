import asyncio

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


async def main():
    async with MultiServerMCPClient(
        {
            "math-server": {
                "command": "python",
                "args": [
                    "/home/voldemort/Desktop/Code/python_projects/mcp-servers/langchain-mcp-adapters/servers/math-server.py"
                ],
            },
            "datetime-server": {"url": "http://localhost:8000/sse", "transport": "sse"},
        }
    ) as client:
        agent = create_react_agent(llm, client.get_tools())
        # result = await agent.ainvoke(
        #     {
        #         "messages": [
        #             HumanMessage(content="Calculate: (abs(-15) + sqrt(64)) * (5! % 7)")
        #         ]
        #     }
        # )

        # math_question = "Calculate: (abs(-15) + sqrt(64)) * (5! % 7)"

        # math_answer = 23

        result = await agent.ainvoke(
            {"messages": [HumanMessage(content="What is the current date and time?")]}
        )

        print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
