#!/bin/bash
# setup.sh — Create and push openclawfieldplaybook to GitHub
# Usage: bash setup.sh
# Prerequisites: git installed, GitHub CLI (gh) installed and authenticated
#   Install gh: https://cli.github.com
#   Authenticate: gh auth login

set -e

REPO_NAME="openclawfieldplaybook"
GITHUB_USER="alexwill87"
DESCRIPTION="The OpenClaw Field Playbook for Entrepreneurs and Agents — practitioner-written, community-maintained, AI-ready"

echo "Creating repo $GITHUB_USER/$REPO_NAME..."

# Init git in current folder
git init
git add .
git commit -m "docs: initial repo structure — The OpenClaw Field Playbook v0.1"

# Create repo on GitHub and push
gh repo create "$GITHUB_USER/$REPO_NAME" \
  --public \
  --description "$DESCRIPTION" \
  --source=. \
  --remote=origin \
  --push

echo ""
echo "Done. Your repo is live at:"
echo "https://github.com/$GITHUB_USER/$REPO_NAME"
echo ""
echo "Next steps:"
echo "1. Add your Anthropic API key as a GitHub secret:"
echo "   gh secret set ANTHROPIC_API_KEY"
echo "2. Enable GitHub Actions in the Actions tab"
echo "3. Test by opening a dummy Issue — AI should respond within 2 minutes"
