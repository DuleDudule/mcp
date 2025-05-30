
from fastmcp import FastMCP, Context
from typing import Dict, Optional, List
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import Annotated
from pydantic import Field
from fastmcp.exceptions import ToolError

# Load environment variables
load_dotenv()

# Create the MCP server instance
mcp = FastMCP(
    name="Agent discovery",
    instructions="This server lets agents register their agent cards and discover other registered agents."
)
agent_store = {}




@mcp.tool()
def publish_card(
        name: Annotated[str, Field(description="Agent name")],
        card: Annotated[str, Field(description="Json agent card")],
) -> str:
    """
    Publish an agent card to the MCP server.
    """
    
    if name in agent_store:
        raise ToolError("Agent with the same name already registered")

    agent_store[name] = {"card": card}

    return f"Agent succesfully registered: {name}"


@mcp.tool()
def list_cards() -> Dict[str, Dict[str, str]]:
    """
    List all agent cards.
    """
    return agent_store


@mcp.tool()
def get_agent(name: Annotated[str, Field(description="Agent name")]) -> Dict[str,str]:
    """
    Returns an agent card based on agent's name.
    """
    return agent_store[name] if name in agent_store else {}


# TODO: These resources should be used in the future for read-only get requests for data.


@mcp.resource("agent://{name}")
# def get_agent_card(name: str) -> AgentCard:
def get_agent_url(name: str,ctx: Context = None) -> str:
    """Dynamic resource for individual agent cards"""
    if name in agent_store:
        return agent_store[name]
    else:
        error_msg = f"Agent {name} not found"
        if ctx:
            ctx.error(error_msg)
        return error_msg


# @mcp.resource("agents://")
# def list_agents() -> List[str]:
#     """Collection resource listing all agent URIs"""
#     return [f"agent://{agent.name}" for agent in agent_store.values()]


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="127.0.0.1", port=6969)
