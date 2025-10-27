# pr-agent-mcp

Agent that analyzes changes and suggests appropriate templates for pull requests.

## Table of Contents

- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
  - [Running the Agent](#running-the-agent)
  - [Inspecting MCP Tools](#inspecting-mcp-tools)
- [Acknowledgments](#acknowledgments)


## Project Structure

```
pr-agent-mcp/
├── mcp_server.py           # FastMCP server with PR analysis tools
├── mcp-host_config.json    # Configuration for MCP host
├── start.sh                # Startup script to run both server and host
├── pyproject.toml          # Python dependencies and project metadata
├── uv.lock                 # UV lock file for reproducible installs
├── templates/              # PR template directory
│   ├── bug.md             # Bug fix template
│   ├── docs.md            # Documentation template
│   ├── feature.md         # Feature template
│   ├── performance.md     # Performance improvement template
│   ├── refactor.md        # Refactoring template
│   ├── security.md        # Security fix template
│   └── test.md            # Test template
└── README.md              # This file
```

**File Descriptions:**
- **mcp_server.py**: The main MCP server that provides tools for analyzing git changes, listing PR templates, and suggesting appropriate templates
- **mcp-host_config.json**: Configuration file for the MCP host client
- **start.sh**: Bash script that starts both the MCP server (background) and MCP host (foreground)
- **templates/**: Contains markdown templates for different types of pull requests

## Prerequisites

### Required

1. **Python 3.10+** and **uv** (Python package installer)
   - Install uv: https://docs.astral.sh/uv/getting-started/installation/

2. **Ollama** (for running local LLMs)
   - Installation: https://ollama.com/download

3. **Go** (for installing mcphost)
   - Installation: https://go.dev/doc/install

4. **mcphost** (MCP host client)
   - Install via Go: `go install github.com/mark3labs/mcphost@latest`
   - Repo: https://github.com/mark3labs/mcphost

### Optional

5. **Node.js and npm** (for inspecting MCP tools)
   - Installation: https://nodejs.org/en/download
   - Required only if you want to use the MCP Inspector

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/alexalm-mf/pr-agent-mcp.git
   cd pr-agent-mcp
   ```

2. Install Python dependencies using uv:
   ```bash
   uv sync --all-extras
   ```

## Usage

### Running the Agent

Simply open the terminal and run the startup script from anywhere, using the absolute path:

```bash
./path/to/pr-agent-mcp/start.sh
```

This script will:
1. Start the MCP server in the background on `http://127.0.0.1:8000/mcp`
2. Start the MCP host in the foreground connected to Ollama with qwen2.5 model
3. Automatically clean up the background server when you exit (Ctrl+C)

### Inspecting MCP Tools

To inspect and test the MCP tools interactively, run the following commands on separate terminals:

```bash
uv run python mcp_server.py
npx @modelcontextprotocol/inspector
```

This will open an interactive inspector in your browser where you can:
- View all available tools
- Test tools with different parameters
- See tool responses in real-time

## Acknowledgments

This project was created as part of the [Hugging Face MCP Course](https://huggingface.co/learn/mcp-course). Special thanks to the Hugging Face team for providing excellent educational resources.
