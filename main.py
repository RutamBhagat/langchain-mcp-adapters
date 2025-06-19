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
                            content="Given the system of equations:\n1) 2x + y = 7\n2) x - y = 2\n3) 3x + 2y = 12\nFind the values of x and y."
                        )
                    ]
                }
            )

            # # Question as a Python string
            # algebra_question = "Given the system of equations:\n1) 2x + y = 7\n2) x - y = 2\n3) 3x + 2y = 12\nFind the values of x and y."

            # # Solution code (using first two equations to find x and y)
            # from sympy import symbols, Eq, solve

            # x, y = symbols('x y')
            # eq1 = Eq(2*x + y, 7)
            # eq2 = Eq(x - y, 2)
            # solution = solve((eq1, eq2), (x, y))
            # # solution: {x: 3, y: 1}

            # # To check if the third equation is satisfied:
            # eq3 = Eq(3*x + 2*y, 12)
            # check = eq3.subs(solution)
            # # check: True

            # # You can also do it with plain Python (not symbolic math):
            # # From eq2: y = x - 2
            # # Substitute into eq1: 2x + (x - 2) = 7 → 3x = 9 → x = 3, y = 1

            print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
