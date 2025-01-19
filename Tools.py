from langchain_core.tools import tool 
import requests
from googlesearch import search


@tool
def calculator(expression: str) -> float:
    """
    Evaluates a given mathematical expression.

    This function takes a mathematical expression as a string, evaluates it, and returns the result.
    It handles basic arithmetic, parentheses, and more complex mathematical calculations.

    Args:
        expression (str): A mathematical expression to evaluate, e.g., "3 + 5 * (2 - 8)".

    Returns:
        Union[float, str]: The result of the evaluated expression, or an error message if invalid.

    Example:
        >>> evaluate_expression("3 + 5 * 2")
        13.0
        >>> evaluate_expression("2 / 0")
        'Error: Division by zero.'
        >>> evaluate_expression("invalid + expression")
        'Error: Invalid input.'
    """
    try:
        # Use eval to compute the result securely
        result = eval(expression, {"__builtins__": None}, {})
        if isinstance(result, (int, float)):  # Ensure result is a number
            return result
        else:
            return "Error: Invalid mathematical expression."
    except ZeroDivisionError:
        return "Error: Division by zero."
    except Exception:
        return "Error: Invalid input."

@tool
def get_stock_price(symbol: str) -> str:
    """Fetches the current stock price of a company based on its stock symbol using the Polygon API.

    Args:
        symbol (str): The stock symbol of the company (e.g., 'AAPL' for Apple, 'GOOGL' for Google).

    Returns:
        str: A message containing the current stock price of the company.

    Raises:
        HTTPError: If the HTTP request to the stock API fails (e.g., 404 or 500 status).
        RequestException: If there is an issue with the request itself (e.g., connection error).
        Exception: For any other unexpected errors during the execution of the function.

    """
    api_key = "bgXWqWwosch5iZV76iQUagp8KkaINWka"  # Replace this with your actual secret API key from Polygon
    url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/prev"  # Polygon endpoint for previous close price

    try:
        # Send a GET request with the API key
        response = requests.get(url, params={'apiKey': api_key})
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx, 5xx)

        # Assuming the data contains 'close' in the response for the last closing price
        data = response.json()
        price = data.get('results', [{}])[0].get('c')  # 'c' is the closing price

        if price:
            return f"Tool used: get_stock_price\n get_stock_price tool is used to find The current price of {symbol} is ${price}"
        else:
            return f"Error: Could not retrieve stock data for {symbol}.\nTool used: get_stock_price"

    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}\nTool used: get_stock_price"
    except requests.exceptions.RequestException as req_err:
        return f"Request error occurred: {req_err}\nTool used: get_stock_price"
    except Exception as err:
        return f"An unexpected error occurred: {err}\nTool used: get_stock_price"

@tool
def get_weather(location: str) -> str:
    """Fetch the current weather for a given location.

     Args:
      location (str): The name of the city or area.

     Returns:
      str: A summary of the weather, including temperature and conditions, or an error message if not found.

     Example:
           >>> get_weather("New York")
       "Weather in New York: Clear skies, 22°C."
    """


    api_key = "e472e9e4cfc93670c3cb249f26576ad9"  # Replace with your OpenWeatherMap API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        response.raise_for_status()
        weather = response.json()
        return (f"Weather in {location}: {weather['weather'][0]['description'].capitalize()}, "
                f"{weather['main']['temp']}°C.")
    except Exception as e:
        return f"Error fetching weather: {e}"


@tool
def google_search_tool(query: str, num_results: int = 5):
    """
    Perform a Google search for a given query and return the top results.

    Args:
        query (str): The search query.
        num_results (int): Number of search results to return. Default is 5.

    Returns:
        list: A list of URLs for the top search results.
    """
    try:
        # Perform the search
        results = search(query, num_results=num_results)
        return list(results)
    except Exception as e:
        return f"An error occurred during the search: {e}"
    
    # Currency Converter Tool
# This code fetches real-time currency exchange rates and converts an amount from one currency to another.

import requests

def get_exchange_rate(api_key, from_currency, to_currency):
    """
    Fetch the exchange rate from a currency to another using an API.
    
    Args:
        api_key (str): API key for the exchange rate service.
        from_currency (str): The source currency code (e.g., 'USD').
        to_currency (str): The target currency code (e.g., 'EUR').
        
    Returns:
        float: The exchange rate from the source to the target currency.
    """
    url = f"https://open.er-api.com/v6/latest/{from_currency}"
    response = requests.get(url, params={"apikey": api_key})
    
    if response.status_code == 200:
        data = response.json()
        if "rates" in data and to_currency in data["rates"]:
            return data["rates"][to_currency]
        else:
            raise ValueError(f"Target currency {to_currency} not found in response.")
    else:
        raise ConnectionError(f"Failed to fetch exchange rates. HTTP Status: {response.status_code}")

@tool("Currency Converter Tool")
def currency_converter_tool(api_key: str, amount: float, from_currency: str, to_currency: str) -> str:
    """
    Convert an amount from one currency to another using real-time exchange rates.

    Args:
        api_key (str): API key for the exchange rate service.
        amount (float): The amount to convert.
        from_currency (str): The source currency code (e.g., 'USD').
        to_currency (str): The target currency code (e.g., 'EUR').

    Returns:
        str: The converted amount in the target currency.
    """
    url = f"https://open.er-api.com/v6/latest/{from_currency}"
    try:
        response = requests.get(url, params={"apikey": api_key})
        if response.status_code == 200:
            data = response.json()
            if "rates" in data and to_currency in data["rates"]:
                exchange_rate = data["rates"][to_currency]
                converted_amount = amount * exchange_rate
                return f"{amount:.2f} {from_currency} is equivalent to {converted_amount:.2f} {to_currency}."
            else:
                return f"Target currency {to_currency} not found in the exchange rates."
        else:
            return f"Failed to fetch exchange rates. HTTP Status: {response.status_code}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Example usage in a LangChain setup

    api_key = "6524ce887b12b275fe97c2ef"  # Replace with your actual API key
    print("Currency Converter Tool")
    print("------------------------")
    from_currency = input("Enter the source currency code (e.g., USD): ").strip().upper()
    to_currency = input("Enter the target currency code (e.g., EUR): ").strip().upper()
    amount = float(input("Enter the amount to convert: "))

    result = currency_converter_tool(api_key, amount, from_currency, to_currency)
    print(result)