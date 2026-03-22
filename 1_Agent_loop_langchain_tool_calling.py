from dotenv import load_dotenv
load_dotenv()

from langchain.chat_models import init_chat_model
from langchain_ollama.chat_models import ChatOllama
from langchain.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langsmith import traceable

max_iterations = 10
model = "qwen3:1.7b"

# Example: initialize an Ollama chat model ("llama2" is the default model name; change as needed)
ollama_model = ChatOllama(model="llama2")

@tool
def get_product_price(product: str) -> float:
    """
    Look up the price of a product in the catalog.
    """
    # Placeholder logic: simple example based on made-up weights
    print(f"   >> Executing get_product_price(product ='{product}')")
    prices = {"laptop":129.99, "headphones":149.9, "Keyboard": 89.50}
    # Make sure it doesn't go below zero
    return prices.get(product, 0)

@tool
def apply_discount(price:float, discount_tier:str) -> float:
    """Apply discount tier to a price and return the final price.
    Available tiers are Bronze, Silver, Gold."""
    discount_percentage = {"Bronze":5, "Silver":12, "Gold":23}
    discount = discount_percentage.get(discount_tier, 0)
    return round(price * (1 -discount/100),2)

@traceable(name="LangChain Agent Loop")
def run_agent(question: str):
    pass

if __name__ == "__main__":
    print("Hello LangChain Agent (.bind_tools)!")
    print()
    result = run_agent("What is the price of Laptop, after applying the Gold discount?")

# Usage example:
# response = ollama_model.invoke("What is the capital of France?")
# print(response)