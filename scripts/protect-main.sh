#!/usr/bin/env bash
# Run ONCE yourself (not the agents) after pushing the repo to GitHub.
# Requires: gh auth login (admin on the repo).
# Usage: ./scripts/protect-main.sh <owner>/<repo>
set -euo pipefail
REPO="${1:?usage: protect-main.sh owner/repo}"

gh api -X PUT "repos/${REPO}/branches/main/protection" \
  -H "Accept: application/vnd.github+json" \
  --input - <<'JSON'
{
  "required_status_checks": { "strict": true, "contexts": ["secret-scan", "tests"] },
  "enforce_admins": false,
  "required_pull_request_reviews": {
    "required_approving_review_count": 0,
    "require_code_owner_reviews": false
  },
  "restrictions": null,
  "allow_force_pushes": false,
  "allow_deletions": false
}
JSON

# Secret scanning + push protection (free for public repos; private needs GitHub Advanced Security)
gh api -X PATCH "repos/${REPO}" \
  -f "security_and_analysis[secret_scanning][status]=enabled" \
  -f "security_and_analysis[secret_scanning_push_protection][status]=enabled" || \
  echo "Secret scanning not available on this plan — gitleaks in CI still covers it."

echo "main is protected on ${REPO}."
