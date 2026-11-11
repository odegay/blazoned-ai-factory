#!/usr/bin/env python3
"""PreToolUse guard for Read / Edit / Write.

1. Blocks access to secret files (.env*, keys, secrets/), allowing .env.example.
2. Blocks writing content that looks like a real secret (tokens, private keys).
Exit code 2 blocks the tool call; stderr is shown to Claude.
"""
import json
import re
import sys
from pathlib import PurePath

ALLOWED_NAMES = {".env.example", ".env.sample", ".env.template"}
BLOCKED_SUFFIXES = (".pem", ".key", ".p12", ".pfx", ".jks")
BLOCKED_DIRS = {"secrets", ".ssh", ".aws", ".azure", ".gcloud"}

SECRET_PATTERNS = [
    (r"ghp_[A-Za-z0-9]{36}", "GitHub personal access token"),
    (r"github_pat_[A-Za-z0-9_]{40,}", "GitHub fine-grained token"),
    (r"gh[osu]_[A-Za-z0-9]{36}", "GitHub OAuth/app token"),
    (r"ATATT[A-Za-z0-9_\-=]{20,}", "Atlassian API token"),
    (r"AKIA[0-9A-Z]{16}", "AWS access key"),
    (r"AIza[0-9A-Za-z_\-]{35}", "Google API key"),
    (r"sk-ant-[A-Za-z0-9_\-]{20,}", "Anthropic API key"),
    (r"sk-[A-Za-z0-9]{32,}", "API secret key"),
    (r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "Private key"),
    (r"xox[baprs]-[A-Za-z0-9-]{10,}", "Slack token"),
]


def path_is_secret(path_str: str) -> bool:
    p = PurePath(path_str.replace("\\", "/"))
    name = p.name.lower()
    if name in ALLOWED_NAMES:
        return False
    if name == ".env" or name.startswith(".env."):
        return True
    if name.endswith(BLOCKED_SUFFIXES):
        return True
    return any(part.lower() in BLOCKED_DIRS for part in p.parts)


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    tool = payload.get("tool_name", "")
    ti = payload.get("tool_input") or {}
    path = ti.get("file_path") or ti.get("path") or ""

    if path and path_is_secret(path):
        print(f"Blocked by guard_files.py: {tool} on secret file '{path}' is not allowed. "
              "Use .env.example for variable names only.", file=sys.stderr)
        return 2

    if tool in ("Write", "Edit", "MultiEdit"):
        chunks = [ti.get("content", ""), ti.get("new_string", "")]
        for e in ti.get("edits", []) or []:
            chunks.append(e.get("new_string", ""))
        text = "\n".join(c for c in chunks if c)
        for pattern, label in SECRET_PATTERNS:
            if re.search(pattern, text):
                print(f"Blocked by guard_files.py: content looks like a {label}. "
                      "Never write secret values; reference an environment variable instead.",
                      file=sys.stderr)
                return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
