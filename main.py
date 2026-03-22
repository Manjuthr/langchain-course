import os
from dotenv import load_dotenv
from langchain_core.tools import Tool
from typing import List
from pydantic import BaseModel, Field

load_dotenv()
from langchain.agents import create_agent
from langchain.tools import tool
from langchain.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_community.tools import DuckDuckGoSearchRun

from langchain_ollama import ChatOllama


class Source(BaseModel):
    """Schema for a source used by the agent"""
    url:str = Field(description = "The URL of the source")

class AgentResponse(BaseModel):
    """Schema for agent response with answer and source"""
    answer:str = Field(description = "The agent's answer to the query")
    sources: List[Source] = Field(default_factory=list, description="List of Sources used to generate the answer")


# ollamamodel = "qwen2.5-coder:7b"
ollamamodel = "llama3.1:8b"
# model = "gemini-2.5-flash"
model = "gemini-2.5-flash-lite"
# model = "Gemini 1.5 Flash"


# llm = ChatGoogleGenerativeAI()
# llm = ChatGoogleGenerativeAI(model=model,temperature=0)
llm = ChatOllama(model=ollamamodel,temperature=0)


# using custom developed tools using Tavily without using langchain TavilySearch -------------------------
from tavily import TavilyClient
tavily = TavilyClient()
@tool
def search(query:str) -> str:
    """Tool that search over internet
    Args: 
        query: Query to search for
        Returns: The search results
    """
    print(f"Searching for {query}")
    # return "Stuttgart Weather is sunny"
    return tavily.search(query=query)

# Using DuckDuckGo Tool 
search_tool = DuckDuckGoSearchRun()
tools = [search_tool]

# tools = [search]

# using langchain TavilySearch -------------------------
# from langchain_tavily import TavilySearch
# tools = [TavilySearch()]

# agent = create_agent(model=llm, tools=tools, response_format=AgentResponse)

agent = create_agent(model = llm, tools = tools)


def main():
    print("Hello from Long-chain")
    question = "What is the weather now in Stuttgart Germany"
    question = "Search for 3 jobs on Teamcenter implementation from linkedin posted recently"
    question = "Search for 3 jobs on Teamcenter implementation from linkedin posted"
    question = "Search for Latest updates from news articles about current US-Iran war?"
    result = agent.invoke({"messages": HumanMessage(content=question)})
    print(result)
    print("\n\n")

    final_answer = result["messages"][-1].content
    print("\nAnswer:\n")
    print(final_answer)


if __name__ == "__main__":
    main()
