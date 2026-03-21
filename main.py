import os
from dotenv import load_dotenv
from langchain_core.tools import Tool

load_dotenv()
from langchain.agents import create_agent
from langchain.tools import tool
from langchain.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_community.tools import DuckDuckGoSearchRun

from langchain_ollama import ChatOllama




ollamamodel = "qwen2.5-coder:7b"
model = "gemini-2.5-flash"
# model = "gemini-2.5-flash-lite"
# tavily = TavilyClient()


# using langchain TavilySearch -------------------------
from langchain_tavily import TavilySearch
tools = [TavilySearch()]

# using custom developed tools using Tavily without using langchain TavilySearch -------------------------
from tavily import TavilyClient
@tool
def search(query:str) -> str:
    """Tool that search over internet
    Args: 
        query: Query to search for
        Returns: The search results
    """
    print(f"Searching for {query}")
    # return "Stuttgart Weather is sunny"
    return TavilyClient.search(query=query)
tools = [search]

# llm = ChatGoogleGenerativeAI()
llm = ChatGoogleGenerativeAI(model=model,temperature=0)
# llm = ChatOllama(model=ollamamodel,temperature=0)
agent = create_agent(model = llm, tools = tools)

def main():
    print("Hello from Long-chain")
    question = "What is the weather now in Stuttgart Germany"
    question = "Search for 3 jobs on Teamcenter implementation from linkedin posted recently"
    question = "Search for 3 jobs on Teamcenter implementation from linkedin posted"
    question = "Search for Latest updates from news articles about current US-Iran war?"
    result = agent.invoke({"messages": HumanMessage(content=question)})
    print(result)


if __name__ == "__main__":
    main()
