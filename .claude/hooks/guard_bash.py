#!/usr/bin/env python3
"""PreToolUse guard for Bash commands.

Exit code 2 blocks the tool call; the stderr message is shown to Claude.
Keep rules simple and conservative — this is a PoC safety net, not a sandbox.
"""
import json
import re
import sys

RULES = [
    (r"\bgit\s+push\b.*(\s--force\b|\s-f\b|\s--force-with-lease\b)", "Force-push is not allowed."),
    (r"\bgit\s+push\b.*\b(origin\s+)?(main|master)\b", "Pushing to main/master is not allowed. Push a feature/<KEY>-* branch and open a PR."),
    (r"\bgit\s+push\b.*\bHEAD:(main|master)\b", "Pushing to main/master is not allowed."),
    (r"--no-verify\b", "Bypassing git hooks (--no-verify) is not allowed."),
    (r"\bgh\s+pr\s+merge\b", "Merging PRs is reserved for the human reviewer."),
    (r"\bgh\s+api\b.*branches/.*/protection", "Changing branch protection is not allowed."),
    (r"\bgh\s+(secret|auth\s+token)\b", "Accessing GitHub secrets/tokens is not allowed."),
    (r"(^|[;&|\s])(printenv|env)(\s*$|\s*[;&|])", "Dumping environment variables is not allowed."),
    (r"\b(cat|less|more|head|tail|type|bat|grep|sed|awk|cp|mv|source|\.)\s+[^;&|]*\.env(\.(?!example\b)[\w-]+)?(\s|$)", "Reading .env files is not allowed (only .env.example)."),
    (r"\becho\s+.*\$\{?[A-Z0-9_]*(TOKEN|SECRET|PASSWORD|API_KEY|PRIVATE_KEY)[A-Z0-9_]*\}?", "Printing secret variables is not allowed."),
    (r"\brm\s+-rf?\s+(/|~|\$HOME|\.git)(\s|/|$)", "Destructive rm on root/home/.git is not allowed."),
    (r"\bkubectl\b|\bhelm\s+install\b", "Kubernetes is out of scope for this project (cost-first defaults)."),
]


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    cmd = (payload.get("tool_input") or {}).get("command", "") or ""
    for pattern, message in RULES:
        if re.search(pattern, cmd, flags=re.IGNORECASE):
            print(f"Blocked by guard_bash.py: {message}", file=sys.stderr)
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
