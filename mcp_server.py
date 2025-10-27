import json
import subprocess
from pathlib import Path

from fastmcp import FastMCP

# Initialize the FastMCP server
mcp = FastMCP("pr-agent")

# PR template directory
TEMPLATES_DIR = Path(__file__) / "templates"


@mcp.tool()
async def analyze_file_changes(
        base_branch: str = "main", 
        include_diff: bool = True,
        max_diff_lines: int = 500,
        working_dir: str = None,
    ) -> str:
    """Analyze file changes with smart output limiting.
    
    Args:
        base_branch: Branch to compare against
        include_diff: Whether to include the actual diff
        max_diff_lines: Maximum diff lines to include (default 500)
        working_dir: Optional working directory path (defaults to current directory)
    """
    try:
        if working_dir is None:
            return json.dumps({"error": "user needs to provide working_dir"})
        else:
            working_dir = Path(working_dir)

        # Get the diff
        result = subprocess.run(
            ["git", "diff", f"{base_branch}...HEAD"],
            capture_output=True, 
            text=True,
            cwd=working_dir
        )
        
        diff_output = result.stdout
        diff_lines = diff_output.split('\n')
        
        # Smart truncation if needed
        if len(diff_lines) > max_diff_lines:
            truncated_diff = '\n'.join(diff_lines[:max_diff_lines])
            truncated_diff += f"\n\n... Output truncated. Showing {max_diff_lines} of {len(diff_lines)} lines ..."
            diff_output = truncated_diff
        
        # Get summary statistics
        stats_result = subprocess.run(
            ["git", "diff", "--stat", f"{base_branch}...HEAD"],
            capture_output=True,
            text=True,
            cwd=working_dir
        )
        
        # Get changed files
        changed_files = subprocess.run(
            ["git", "diff", "--name-only", f"{base_branch}...HEAD"],
            capture_output=True,
            text=True,
            cwd=working_dir
        )

        return json.dumps({
            "stats": stats_result.stdout,
            "total_lines": len(diff_lines),
            "diff": diff_output if include_diff else "Use include_diff=true to see diff",
            "files_changed": changed_files.stdout
        }, indent=2)
        
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
async def get_pr_templates() -> str:
    """List available PR templates with their content."""
    try:
        templates = {}
        for template_file in TEMPLATES_DIR.glob("*.md"):
            with open(template_file, "r") as f:
                templates[template_file.stem] = f.read()
        return json.dumps(templates, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
async def suggest_template(changes_summary: str, pr_template: str) -> str:
    """Analyze the changes and suggest the most appropriate PR template.
    
    Args:
        changes_summary: Your analysis of what the changes do
        pr_template: The most appropriate PR template you've identified (bug, feature, docs, refactor, etc.)
    """
    try:
        # Read templates directly instead of calling the tool
        templates = {}
        for template_file in TEMPLATES_DIR.glob("*.md"):
            with open(template_file, "r") as f:
                templates[template_file.stem] = f.read()

        return json.dumps({
            "recommended_template": pr_template,
            "reasoning": f"I recommend the '{pr_template}' template because the changes involve:\n{changes_summary}.",
            "template_content": templates.get(pr_template.lower(), "No content found for this specific template.")
        }, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="127.0.0.1", port=8000)
