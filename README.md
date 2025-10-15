# Agent Supervisor Demo (LangGraph)

This project is a hands-on demo of multi-agent orchestration using LangGraph

It shows how a Supervisor Agent can coordinate multiple Worker Agents (e.g., research, math) to solve complex tasks step by step.

🔎 What’s inside

Supervisor Agent – decides which worker should handle each request.

Research Agent – uses the Tavily web search tool to gather information.

Math Agent – performs simple calculations (add, multiply, divide).

LangGraph – connects everything in a state graph.


💡 Example usage

Ask a question that mixes research + math:

Using recent sources, what's New York state's share of US GDP? 
Then multiply that share by 100.



The Supervisor Agent will:

Send the research part to the Research Agent.
Forward the math part to the Math Agent.
Return the final result.


🛡️ Notes

.env and .venv/ are ignored with .gitignore (so your secrets are safe).
You’ll need valid API keys for OpenAI and Tavily.
If OpenAI quota runs out, you can switch to other models (Anthropic, Gemini, or Ollama).

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
