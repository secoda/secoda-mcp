from server import mcp

if __name__ == "__main__":
    # Run in HTTP mode instead of stdio
    mcp.run(transport="http", host="0.0.0.0", port=5012)
