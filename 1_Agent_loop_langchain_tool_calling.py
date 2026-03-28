from socket import MSG_DONTROUTE
from dotenv import load_dotenv
from langchain_core import messages
from langchain_core.messages.tool import tool_call
load_dotenv()

from langchain.chat_models import init_chat_model
from langchain_ollama.chat_models import ChatOllama
from langchain.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langsmith import traceable

max_iterations = 10
model = "qwen2.5:7b"
# model = "llama3.1:8b"

# Example: initialize an Ollama chat model ("llama2" is the default model name; change as needed)
ollama_model = ChatOllama(model=model)

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

# ----------agent loop-----

@traceable(name="LangChain Agent Loop")
def run_agent(question: str):
    tools = [get_product_price, apply_discount]
    tools_dict = {t.name: t for t in tools}

    # llm = init_chat_model(f"Ollama: {model}", model_provider="ollama", temperature=0)
    llm = init_chat_model(model, model_provider="ollama", temperature=0)
    llm_with_tools = llm.bind_tools(tools)
    print(question)
    print("="*50)

    messages = [
        SystemMessage(
            content=(
                "You are a helpful shopping assistant. "
                "You have access to a product catalog tool "
                "and a discount tool.\n\n"
                "STRICT RULES - you must follow these exactly:\n"
                "1. NEVER guess or assume any product price. "
                "You MUST call get_product_price first.\n"
                "2. Only call apply_discount AFTER receiving "
                "a price from get_product_price.\n"
                "3. NEVER calculate discounts yourself.\n"
                "4. If the user does not specify a discount tier, "
                "ask them which tier to use."
            )
        ),
        HumanMessage(content=question),
    ]

    for iteration in range(1, max_iterations + 1):

            print(f"\n---Iteration-{iteration}")

            ai_message = llm_with_tools.invoke(messages)

            messages.append(ai_message)

            tool_calls = ai_message.tool_calls

            if not tool_calls:
                print("\nFinal Answer:", ai_message.content)
                return ai_message.content

            tool_call = tool_calls[0]
            tool_name = tool_call.function.name

            # for tool_call in tool_calls:

            #     tool_name = tool_call["name"]
            #     tool_args = tool_call["args"]

            #     tool = tools_dict[tool_name]

            #     print(f"Calling Tool: {tool_name} with {tool_args}")

            #     tool_result = tool.invoke(tool_args)

            #     messages.append(
            #         ToolMessage(
            #             content=str(tool_result),
            #             tool_call_id=tool_call["id"],
            #         )
            #     )


if __name__ == "__main__":
    print("Hello LangChain Agent (.bind_tools)!")
    # print()
    result = run_agent("What is the price of laptop, after applying the Gold discount?")

# Usage example:
# response = ollama_model.invoke("What is the capital of France?")
# print(response)