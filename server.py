from datetime import datetime
from fastapi import FastAPI
from fastmcp import FastMCP, Context
from mcp.server.fastmcp.prompts import base
from contextlib import asynccontextmanager
import os
from typing import Optional, List
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create the MCP server instance
mcp = FastMCP("Agent discovery")

agent_store = {}

class AgentCard(BaseModel):
    name: str
    agent_card_url: str
   

@mcp.tool()
def publish_card(ctx: Context = None, name: str = None, agent_card_url: str = None):
    """
    Publish an agent card to the MCP server.

    Args:
        name (str): The name of the agent.
        agent_card_url (str): The URL of the agent card.
    """
    try:
        if name in agent_store:
            ctx.error(f"Agent {name} already exists")
            return "Registration failed"
        
        agent_store[name] = AgentCard(
            name=name,
            agent_card_url=agent_card_url
        )
        return f"agent://{name}"

    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        if ctx:
            ctx.error(error_msg)
        return error_msg
@mcp.tool()
def list_cards(ctx: Context = None) -> List[str]:
    """
    List all agent cards.

    Returns:
        List[str]: A list of agent card URLs.
    """
    try:
        return [f"agent://{name}" for name in agent_store.keys()]
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        if ctx:
            ctx.error(error_msg)
        return error_msg
@mcp.tool()
def get_agent(name: str = None) -> List[str]:
    """
    Returns an agent card based its name.

    Args:
        ctx (Context): The context of the MCP server.

    Returns:
        List[str]: A list of agent card URLs.
    """
    try:
        return get_agent_card(name)

    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        if ctx:
            ctx.error(error_msg)
        return error_msg

@mcp.resource("agent://{name}")
def get_agent_card(name: str) -> AgentCard:
    """Dynamic resource for individual agent cards"""
    if name in agent_store:
        return agent_store[name]
    else:
        error_msg = f"Agent {name} not found"
        if ctx:
            ctx.error(error_msg)
        return error_msg

@mcp.resource("agents://")
def list_agents() -> List[str]:
    """Collection resource listing all agent URIs"""
    return [f"agent://{agent.name}" for agent in agent_store.values()]




# # Create FastAPI app and mount the SSE MCP server
# app = FastAPI(
#     title="TNT MCP Server", 
#     description="FastAPI application with MCP SSE server for action logging",
#     docs_url="/docs",
#     redoc_url="/redoc",
#     openapi_url="/openapi.json",

# )

# Initialize MCP with FastAPI
# mcp.init_app(app)

# Mount with Streamable HTTP transport
# app.mount("/mcp", mcp.http_app())
if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="127.0.0.1",
        port=6969
    )