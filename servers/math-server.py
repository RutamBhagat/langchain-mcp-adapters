from mcp.server.fastmcp import FastMCP
from sympy import N, SympifyError, parse_expr

mcp = FastMCP("Math")


@mcp.tool()
def evaluate_math_expression(
    expr_str: str, subs_dict: dict | None = None
) -> str | float:
    """
    Evaluates a mathematical expression given as a string.

    Args:
        expr_str (str): The mathematical expression (e.g., "2*x + 3").
        subs_dict (dict, optional): Dictionary of substitutions for variables.
                                   Example: {'x': 2}
                                   If None, returns symbolic result.
    Returns:
        SymPy expression or numeric result after substitution.
    """
    expr = parse_expr(expr_str)
    if subs_dict is not None:
        expr = expr.subs(subs_dict)
        try:
            return N(expr)  # Returns a numeric value if possible
        except SympifyError:
            return expr  # Returns symbolic if not fully numeric
        except Exception as e:
            return f"Error: {e}"
    return expr


if __name__ == "__main__":
    mcp.run("stdio")
