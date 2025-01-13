from langchain_core.tools import tool 


@tool
def multiply(a,b):
    """
    A tool that multiplies two numbers.
    """
    return a * b

@tool
def divide(a,b):
    """ 
    A tool that divides two numbers.
    
    """
    return a / b

