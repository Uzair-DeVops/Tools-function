from langchain_core.tools import tool 


@tool
def multiply(a,b):
    """
    A tool that multiplies two numbers.
    """
    return a * b