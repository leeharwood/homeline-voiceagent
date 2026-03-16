from typing import Any, Dict
from homeline.utils.logging import logger

def call_mcp_tool(tool_name: str, **kwargs) -> str:
    """
    Adapter to call MCP tools synchronously in-process. 
    This enables the FastAPI routes to offload work to the MCP server 
    while preserving the exact HTTP webhook behavior required by Telnyx.
    """
    try:
        # Import the mcp instance tools dynamically
        from homeline.mcp.server import mcp
        
        # In FastMCP, tools are registered as Callables inside the server.
        # We find the tool by name and execute it with the provided kwargs.
        tool_func = None
        for t in mcp._tools:
            if t.name == tool_name:
                tool_func = t.fn
                break
                
        if not tool_func:
            logger.error(f"MCP tool {tool_name} not found.")
            return "Error: Internal tool not found."
            
        logger.info(f"Delegating execution to MCP tool: {tool_name} with args: {kwargs}")
        return tool_func(**kwargs)
    except Exception as e:
        logger.error(f"Error executing MCP tool {tool_name}: {e}")
        return f"Error executing task: {str(e)}"
