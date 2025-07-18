from util import embed_text, search_qdrant, call_ollama
from mcp_tools import run_all_mcp_tools

async def generate_response(question: str) -> str:
    embedded_query = await embed_text(question)
    documents = await search_qdrant(embedded_query)
    context = "\n".join(documents)

    mcp_output = await run_all_mcp_tools()

    prompt = f"""
You are Morales1, an intelligent assistant for infrastructure and code analysis.
Respond in the same language as the user.
You have access to the following MCP tools and their results:

{mcp_output}

Use the following context:
{context}

User Question: {question}
Answer:
"""
    return await call_ollama(prompt)
