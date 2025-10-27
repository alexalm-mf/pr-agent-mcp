#!/bin/bash

# PR Agent MCP Startup Script
# This script starts both the MCP server and MCP host

# Get the directory of this script
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"
echo "Changed to script directory: $SCRIPT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting PR Agent MCP Services...${NC}"

# Function to cleanup background processes on exit
cleanup() {
    echo -e "\n${YELLOW}Shutting down MCP Server...${NC}"
    if [[ -n $MCP_SERVER_PID ]]; then
        kill $MCP_SERVER_PID 2>/dev/null || true
    fi
}

# Set up trap to cleanup on exit
trap cleanup EXIT SIGINT SIGTERM

# Start MCP Server using uv (in background, suppress output)
echo -e "${GREEN}Starting MCP Server in background...${NC}"
uv run python mcp_server.py > /dev/null 2>&1 &
MCP_SERVER_PID=$!

# Wait a moment for the server to start
sleep 2

# Check if MCP server is still running
if ! kill -0 $MCP_SERVER_PID 2>/dev/null; then
    echo -e "${RED}Failed to start MCP Server${NC}"
    echo -e "${YELLOW}Check the error above for details${NC}"
    exit 1
fi

echo -e "${GREEN}MCP Server started (PID: $MCP_SERVER_PID)${NC}"

# Start MCP Host in foreground
echo -e "${GREEN}Starting MCP Host (foreground)...${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop all services${NC}"
echo ""

# Run MCP Host in foreground - when it exits, cleanup will run
~/go/bin/mcphost -m ollama:qwen2.5 --config "mcp-host_config.json"