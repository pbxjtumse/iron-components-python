#!/usr/bin/env bash
set -euo pipefail

if [[ ! -f "pyproject.toml" ]]; then
  echo "Run this script from the iron-components-python repository root."
  exit 1
fi

mkdir -p packages ai integrations apps/component-demo apps/ai-demo docs tests

create_lib() {
  local path="$1"
  local name="$2"

  if [[ -f "$path/pyproject.toml" ]]; then
    echo "skip: $path already exists"
    return
  fi

  uv init --lib --name "$name" "$path"
}

create_lib packages/iron-foundation iron-foundation
create_lib packages/iron-config iron-config
create_lib packages/iron-serialization iron-serialization
create_lib packages/iron-observability iron-observability
create_lib packages/iron-concurrency iron-concurrency
create_lib packages/iron-retry iron-retry
create_lib packages/iron-cache iron-cache
create_lib packages/iron-message iron-message

create_lib ai/iron-ai-model iron-ai-model
create_lib ai/iron-ai-prompt iron-ai-prompt
create_lib ai/iron-ai-tool iron-ai-tool
create_lib ai/iron-ai-context iron-ai-context
create_lib ai/iron-ai-workflow iron-ai-workflow
create_lib ai/iron-ai-rag iron-ai-rag
create_lib ai/iron-ai-agent iron-ai-agent
create_lib ai/iron-ai-evaluation iron-ai-evaluation

create_lib integrations/iron-openai iron-openai
create_lib integrations/iron-langchain iron-langchain
create_lib integrations/iron-langgraph iron-langgraph

echo
echo "Workspace scaffold created."
echo "Next: review pyproject.toml, then run: uv sync"
