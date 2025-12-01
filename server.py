import os
import json

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
    """Call a tool and unwrap the Secoda MCP response."""
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
    
    # Get the JSON response
    json_response = response.json()

    # Extract the content from the Secoda API response
    def extract_text(content):
        """Safely extract text from content blocks."""
        if isinstance(content, list):
            blocks = [
                item.get("text", "")
                for item in content
                if isinstance(item, dict) and item.get("type") == "text"
            ]
            return "\n".join(blocks).strip()
        if isinstance(content, str):
            return content.strip()
        return ""

    # Unwrap common Secoda response formats
    if isinstance(json_response, dict):
        if "content" in json_response:
            return extract_text(json_response["content"])

        result = json_response.get("result")
        if isinstance(result, str):
            return result.strip()
        if isinstance(result, dict) and "content" in result:
            return extract_text(result["content"])

    # Fallback: return formatted JSON if no text found 
    return json.dumps(json_response, indent=2)


@mcp.tool()
def run_sql(query: str) -> str:
    """Run a SQL query on the database."""
    return call_tool("run_sql", {"query": query})


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
