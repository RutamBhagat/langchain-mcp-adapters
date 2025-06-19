from datetime import datetime

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Datetime")


@mcp.tool()
def current_datetime_second() -> str:
    """Returns the current date and time as a string, precise to the second."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


if __name__ == "__main__":
    mcp.run(transport="sse")
