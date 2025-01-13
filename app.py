from langchain_google_genai import ChatGoogleGenerativeAI
from Tools import multiply,divide,get_stock_price
from langchain.agents import initialize_agent, AgentType


GOOGLE_API_KEY = "AIzaSyDlGuiJOqQePVsQEu5gWiftb74RDGvcq-c"

llm = ChatGoogleGenerativeAI(model = "gemini-2.0-flash-exp" ,api_key=GOOGLE_API_KEY)

tools = [multiply,divide,get_stock_price]

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION
    )


response = agent.invoke("8/9")
print(response)

# using stoke price tool
response = agent.invoke("what is the current price of apple stock")
print(response) # prints the current stock price of AAPL



