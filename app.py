from langchain_google_genai import ChatGoogleGenerativeAI
from Tools import calculator,get_stock_price,get_weather,google_search_tool
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
