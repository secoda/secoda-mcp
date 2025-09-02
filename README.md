# Secoda MCP

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

Secoda MCP is a custom server built with FastMCP that provides access to Secoda's data tools and functionalities.

## Features

- Access to Secoda's data assets search
- Access to documentation search
- Ability to run SQL queries directly
- Integration with Secoda's data catalog
- Entity lineage visualization
- Glossary term retrieval

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Access to Secoda's API
- API token for authentication with the Secoda API (can be generated at https://app.secoda.co/settings/api if you're an admin)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/secoda/secoda-mcp.git
   cd secoda-mcp
   ```

2. Install dependencies:
   ```bash
   # Install runtime dependencies
   python -m pip install -r requirements.txt
   ```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `API_TOKEN` | Required token for API authentication | None (Required) |
| `API_URL` | URL of the Secoda API endpoint | https://app.secoda.co/api/v1/ |

### Instance URL Note

If you're using a regional instance or self-hosted deployment of Secoda, replace `app.secoda.co` with your specific instance URL:

- EU region: `eu.secoda.co`
- APAC region: `apac.secoda.co`
- Self-hosted: Your custom domain (e.g., `secoda.yourcompany.com`)

## Integration with Tools

### Using with Cursor

To integrate Secoda MCP with Cursor, add the following configuration to your `~/.cursor/mcp.json` file:

```json
{
    "mcpServers": {
        "secoda-mcp": {
            "command": "python",
            "args": [
                "/path/to/secoda-mcp/server.py"
            ],
            "env": {
                "API_TOKEN": "your-api-token",
                "API_URL": "https://app.secoda.co/api/v1/"
            }
        }
    }
}
```

Replace `/path/to/secoda-mcp/server.py` with the actual path to your server.py file, set your API token, and update the API_URL with your Secoda instance URL if not using app.secoda.co.

### Using with Claude

To integrate Secoda MCP with Claude Desktop, add the following to your Claude Desktop configuration file:

#### macOS: ~/Library/Application Support/Claude/claude_desktop_config.json
#### Windows: %APPDATA%\Claude\claude_desktop_config.json

```json
{
    "mcpServers": {
        "secoda-mcp": {
            "command": "python",
            "args": [
                "/path/to/secoda-mcp/server.py"
            ],
            "env": {
                "API_TOKEN": "your-api-token",
                "API_URL": "https://app.secoda.co/api/v1/"
            }
        }
    }
}
```

Replace `/path/to/secoda-mcp/server.py` with the actual path to your server.py file, set your API token, and update the API_URL with your specific Secoda instance URL if not using app.secoda.co. To access the Claude Desktop configuration file, open the Claude menu, go to "Settings", click on "Developer" in the left-hand bar, and then click on "Edit Config".

After updating the configuration, restart Claude Desktop to apply the changes.

### Using with Microsoft Copilot Studio

To integrate Secoda MCP with Microsoft Copilot Studio, you'll need to run the server in HTTP mode and expose it via a public HTTPS endpoint. This integration allows your Copilot Studio agents to access Secoda's data catalog, run SQL queries, and search documentation.

#### Prerequisites for Copilot Studio Integration

- Active Secoda account with API access
- Secoda API token (generate at https://app.secoda.co/settings/api)
- Microsoft Copilot Studio access
- ngrok account (for exposing local server publicly)

#### Step 1: Set Up HTTP Server

The repository includes `server_http.py` which runs the MCP server in HTTP mode:

```bash
# Set your environment variables
export API_TOKEN="your-secoda-api-token"
export API_URL="https://app.secoda.co/api/v1/"  # or your instance URL

# Install dependencies if not already installed
pip install -r requirements.txt

# Run the HTTP server
python server_http.py
```

The server will start on `http://localhost:5012/mcp` by default.

#### Step 2: Expose Server with ngrok

Since Copilot Studio requires a public HTTPS endpoint:

```bash
# Install ngrok (macOS)
brew install ngrok

# Create ngrok account and authenticate
ngrok config add-authtoken YOUR_NGROK_TOKEN

# In a new terminal, expose your local server
ngrok http 5012

# Copy the HTTPS URL (e.g., https://abc123.ngrok.io)
```

#### Step 3: Configure OpenAPI Schema

Use the provided `copilot_studio.sample.yaml` file and update it with your ngrok URL:

1. Open `copilot_studio.sample.yaml`
2. Replace `b8b4198d8693.ngrok-free.app` on line 6 with your actual ngrok URL (without https://)
3. Save the file as `copilot_studio.yaml`

#### Step 4: Test Your Setup

Before configuring Copilot Studio, verify your server works:

```bash
# Test basic connectivity
curl https://your-ngrok-url.ngrok.io/mcp

#### Step 5: Configure in Copilot Studio

1. **Access Copilot Studio**: Go to https://copilotstudio.microsoft.com
2. **Create or Select Agent**: Choose the agent you want to enhance
3. **Add Custom Connector**:
   - Navigate to Tools → Add a tool → New tool → Custom connector
   - This will redirect you to Power Apps
4. **Import OpenAPI Schema**:
   - In Power Apps, select "Import from OpenAPI file"
   - Upload your configured `copilot_studio.yaml`
   - Review and confirm the import
5. **Configure Connector**:
   - Set the host to your ngrok URL (without https://)
   - Configure authentication if needed
   - Test the connector using the built-in test feature
6. **Add Secoda MCP to Your Agent**
   - Go to your agent in CopilotStudio.
   - Go to tools tab, click on Add tool
   - In the Model Context Protocol section, search for Secoda and add it. 

#### Available Tools in Copilot Studio

Once configured, your Copilot Studio agent will have access to these Secoda tools:

- **run_sql**: Execute SQL queries against your data warehouse
- **search_data_assets**: Find tables, columns, and other data assets
- **search_documentation**: Search through data documentation
- **retrieve_entity**: Get detailed information about specific data entities
- **entity_lineage**: View data lineage for understanding data flow
- **glossary**: Access your organization's data glossary

#### Example Usage in Copilot Studio

Users can interact with your agent using natural language:

- "Show me all tables related to customers"
- "What's the definition of revenue in our glossary?"
- "Run a query to get the top 10 customers by sales"
- "Find documentation about our user analytics tables"

#### Monitoring and Debugging

Monitor requests through ngrok's web interface:

```bash
# Open ngrok inspector in browser
open http://localhost:4040
```

This shows all HTTP requests/responses, helping you debug any issues.

#### Production Considerations

For production use:

1. **Use a stable URL**: Replace ngrok with a permanent hosting solution
2. **Add authentication**: Configure proper API key authentication in Power Apps
3. **Enable logging**: Add comprehensive logging to your server
4. **Set up monitoring**: Monitor server health and API usage
5. **Configure rate limiting**: Implement appropriate rate limiting

#### Troubleshooting Copilot Studio Integration

**Connection Issues:**
- Verify ngrok is running and forwarding correctly
- Check that your Secoda API token is valid
- Ensure the server is running on the expected port

**Authentication Errors:**
- Confirm your API token has the necessary permissions
- Check that the API_URL environment variable is correct for your Secoda instance

### Using with Other Tools

Secoda MCP can be integrated with various other tools:

- **VS Code**: Use the VS Code extension for MCP servers
- **JetBrains IDEs**: Install the MCP plugin from the marketplace
- **Command Line**: Access MCP functionalities directly via the CLI
- **Web Applications**: Embed MCP capabilities in web apps through the REST API

## Troubleshooting

- If you encounter connection issues, ensure Secoda's API is running at the configured URL
- If you get authorization errors, verify your API token is correct and properly set as an environment variable
- For permission errors, check your authentication settings in your Secoda account

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Security

If you discover any security related issues, please email security@secoda.co instead of using the issue tracker.

