import os
import typing

import requests
from fastmcp import FastMCP

from prompt import MCP_PROMPT

# --------------------------------
# Configuration
# --------------------------------

API_URL = os.getenv("API_URL", "https://app.secoda.co/api/v1/")
API_TOKEN = os.getenv("API_TOKEN")


# --------------------------------
# Tools
# --------------------------------

mcp = FastMCP(
    name="Secoda MCP",
    instructions=MCP_PROMPT,
)


def call_tool(tool_name: str, args: dict):
    """Call a tool."""
    api_url = API_URL if API_URL.endswith("/") else f"{API_URL}/"

    response = requests.post(
        f"{api_url}ai/mcp/tools/call/",
        headers={
            "Authorization": f"Bearer {API_TOKEN}",
            "Content-Type": "application/json",
        },
        json={
            "name": tool_name,
            "arguments": args,
        },
    )
    response.raise_for_status()
    return response.json()


@mcp.tool()
def run_sql(query: str, integration_id: typing.Optional[str] = None) -> str:
    """Run a SQL query on the database."""
    return call_tool("run_sql", {"query": query, "integration_id": integration_id})


@mcp.tool()
def search_data_assets(query: str, page: int = 1) -> str:
    """Search for data assets in the database."""
    return call_tool("search_data_assets", {"query": query, "page": page})


@mcp.tool()
def search_documentation(query: str, page: int = 1) -> str:
    """Search for documentation in the database."""
    return call_tool("search_documentation", {"query": query, "page": page})


@mcp.tool()
def retrieve_entity(entity_id: str) -> str:
    """Retrieve an entity from the database."""
    return call_tool("retrieve_entity", {"entity_id": entity_id})


@mcp.tool()
def entity_lineage(entity_id: str) -> str:
    """Retrieve the lineage of an entity."""
    return call_tool("entity_lineage", {"entity_id": entity_id})


@mcp.tool()
def glossary() -> str:
    """Retrieve the glossary."""
    return call_tool("glossary", {})


if __name__ == "__main__":
    mcp.run()
