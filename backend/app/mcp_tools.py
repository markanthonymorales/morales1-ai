import os
import importlib.util
import asyncio

MCP_FOLDER = os.path.join(os.path.dirname(__file__), "mcp")

def discover_tools():
    tools = {}
    for filename in os.listdir(MCP_FOLDER):
        if filename.endswith(".py") and filename != "__init__.py":
            name = filename[:-3]
            tools[name] = os.path.join(MCP_FOLDER, filename)
    return tools

MCP_TOOLS = discover_tools()

async def run_tool(name: str):
    path = MCP_TOOLS.get(name)
    if not path:
        return f"Tool '{name}' not found."

    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
        if hasattr(module, "run") and asyncio.iscoroutinefunction(module.run):
            return await module.run()
        elif hasattr(module, "run"):
            return module.run()
        else:
            return f"Tool '{name}' does not have a 'run' function."
    except Exception as e:
        return f"Error running tool '{name}': {str(e)}"

async def run_all_mcp_tools():
    results = {}
    for name in MCP_TOOLS:
        result = await run_tool(name)
        results[name] = result
    return results
