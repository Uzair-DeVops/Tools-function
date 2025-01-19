from langchain_google_genai import ChatGoogleGenerativeAI
from Tools import calculator,get_stock_price,get_weather,google_search_tool,currency_converter_tool
from langchain.agents import initialize_agent, AgentType


GOOGLE_API_KEY = "AIzaSyDlGuiJOqQePVsQEu5gWiftb74RDGvcq-c"

llm = ChatGoogleGenerativeAI(model = "gemini-2.0-flash-exp" ,api_key=GOOGLE_API_KEY)

tools = [calculator,get_stock_price,get_weather]

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION
    )


response = agent.invoke("8/9")
print(response)

# using stock price tool
response = agent.invoke("what is the current price of apple stock")
print(response) # prints the current stock price of AAPL


# using weather tool
response = agent.invoke("what is the weather of Sheikhupura")
print(response, "Thanks For Asking Me") # prints the weather in Sheikhupura

# using calculator tool
response = agent.invoke("3*4/(5/4+45*4)")
print(response) # prints the result of the calculation

# using google search tool
response = agent.invoke("what is the capital of France")
print(response) # prints the capital of France

# until here the code is working fine


# using currency converter tool
api_key = "6524ce887b12b275fe97c2ef"  # Replace with your actual API key
print("Currency Converter Tool")
print("------------------------")
from_currency = input("\033[34mEnter the source currency code (e.g., USD):\033[0m ").strip().upper()
to_currency = input("\033[34mEnter the target currency code (e.g., EUR): \033[0m ").strip().upper()
amount = float(input("\033[34mEnter the amount to convert:\033[0m "))

input_data = {
        "api_key": api_key,
        "amount": amount,
        "from_currency": from_currency,
        "to_currency": to_currency,
    }

result = currency_converter_tool.invoke(input_data)
print(result)
