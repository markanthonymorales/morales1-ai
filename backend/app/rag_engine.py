from utils import embed_text, search_qdrant, call_ollama
from mcp_tools import run_all_mcp_tools

async def generate_response(question: str):
    embedded_query = await embed_text(question)
    documents = await search_qdrant(embedded_query)
    context = "\n".join(documents)

    mcp_results = await run_all_mcp_tools()
    tools_output = "\n".join([f"{k}: {v}" for k, v in mcp_results.items()])
    prompt = f"""
You are Morales1, an intelligent assistant for infrastructure assessment.
Respond in the same language as the user input.

Available MCP tools:
{tools_output}

Context:
{context}
---
Question: {question}
"""

    answer = await call_ollama(prompt)
    return answer, context
