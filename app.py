# app.py
from langgraph.prebuilt import create_react_agent
from langgraph_supervisor import create_supervisor
from langchain_tavily import TavilySearch
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool 

# --- simple math tools ---
@tool
def add(a: float, b: float) -> float:
    """Add two numbers and return the sum."""
    return a + b

@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers and return the product."""
    return a * b

@tool
def divide(a: float, b: float) -> float:
    """Divide a by b and return the quotient."""
    return a / b

# --- web search tool (needs TAVILY_API_KEY) ---
web_search = TavilySearch(max_results=3)

# --- worker agents ---
research_agent = create_react_agent(
    model="openai:gpt-4o-mini",  # cheaper, good enough
    tools=[web_search],
    prompt=(
        "You are a research agent.\n"
        "Only do research/web lookups. Do not do math."
    ),
    name="research_agent",
)

math_agent = create_react_agent(
    model="openai:gpt-4o-mini",
    tools=[add, multiply, divide],
    prompt=(
        "You are a math agent.\n"
        "Only do calculations. Do not browse the web."
    ),
    name="math_agent",
)

# --- supervisor that routes tasks ---
supervisor_graph = create_supervisor(
    model=init_chat_model("openai:gpt-4o-mini"),
    agents=[research_agent, math_agent],
    prompt=(
        "You manage two agents:\n"
        "- research_agent for research\n"
        "- math_agent for math\n"
        "Route the user's request to one agent at a time. Do not solve it yourself."
    ),
    add_handoff_back_messages=True,   # keep the conversation flow
    output_mode="full_history",       # show all steps
).compile()

if __name__ == "__main__":
    user_msg = (
        "Using recent sources, what's New York state's share of US GDP? "
        "Then multiply that share by 100."
    )
    print(">>> USER:", user_msg)
    # Stream prints each step so you can see who’s working
    for chunk in supervisor_graph.stream({"messages": [{"role": "user", "content": user_msg}]}):
        for _, upd in chunk.items():
            msgs = upd.get("messages", [])
            if msgs:
                last = msgs[-1]
                name = last.get("name") or last.get("role")
                content = last.get("content", "")
                if content:
                    print(f"[{name}] {content}")
