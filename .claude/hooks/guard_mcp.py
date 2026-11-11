#!/usr/bin/env python3
"""PreToolUse guard for Atlassian (Jira/Confluence) MCP tools.

Blocks destructive tools (delete / destructive execute) regardless of how the
server is named (local .mcp.json 'atlassian' or the claude.ai connector).
Exit code 2 blocks the call; stderr is shown to Claude.
"""
import json
import re
import sys

BLOCK = re.compile(r"(delete|destructive|remove|purge)", re.IGNORECASE)


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    name = payload.get("tool_name", "") or ""
    if BLOCK.search(name.split("__")[-1]):
        print(f"Blocked by guard_mcp.py: '{name}' is destructive. Jira issues are never deleted; "
              "close or comment instead, or ask the owner.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
