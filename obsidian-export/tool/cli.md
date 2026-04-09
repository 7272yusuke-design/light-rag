---
source: https://github.com/googleworkspace/cli
category: tool
sub_categories: [agent, workflow]
tags: [rust, google-workspace, cli, google-api, discovery-api, oauth2, automation, ai-agent]
language: 
ingested: 2026-04-09
source_updated: unknown
status: active
---

# cli

# cli

## 基本情報
- リポジトリ: https://github.com/googleworkspace/cli
- カテゴリ: tool
- サブカテゴリ: agent, workflow
- タグ: rust, google-workspace, cli, google-api, discovery-api, oauth2, automation, ai-agent
- 最終確認日: 2026-04-09

## 概要
GWS is a Rust-based CLI tool that dynamically generates commands for all Google Workspace APIs (Gmail, Drive, Calendar, Sheets, Docs, etc.) by fetching Discovery Documents at runtime. It is designed for use by AI agents, shell scripts, and power users, supporting auto-pagination, type-safe schemas, and structured JSON output. The tool provides pre-built workflows, persona-based skill sets, and recipes for common automation tasks.

## 設計思想
Commands are dynamically generated from Google API Discovery Documents at runtime, eliminating the need for generated Rust crates (e.g., google-drive3). This means new API endpoints are available automatically without code changes. The CLI is hardened for adversarial inputs (AI/LLM agent invocation), with strict input validation against path traversal, control characters, and Unicode injection. Architecture is split into a core library crate (google-workspace) providing Discovery parsing, service registry, validation, and HTTP retry logic, and a CLI crate (google-workspace-cli) that builds the command tree and helper workflows on top.

## 主要コンポーネント
- Discovery Engine: Fetches and caches Google API Discovery Documents at runtime to dynamically generate CLI subcommands for all API resources and methods
- google-workspace crate: Core library providing HTTP client with retry, Discovery Document types, service registry, structured error types, and input validation utilities
- google-workspace-cli crate: CLI binary built on the core library; implements auth, command execution, output formatting, and helper commands
- Helpers (+verb commands): Handwritten multi-step orchestration commands (e.g., gmail +triage, calendar +agenda) that go beyond what single API calls provide
- Workflows: Composed multi-API automations (standup-report, meeting-prep, weekly-digest) orchestrating several Workspace services
- Skills & Personas: Markdown knowledge files and persona/recipe registries that describe how an AI agent should use the CLI for specific roles and tasks
- Validation Layer: Rejects path traversal, dangerous Unicode, control characters, and URL injection from all CLI inputs before they reach the API

## 実装パターン
- Runtime Discovery Generation: CLI subcommands are built dynamically from Discovery Documents fetched at startup, with 24-hour disk cache, rather than from statically generated code
- Retry with Exponential Backoff: HTTP requests automatically retry on 429 rate-limit responses and transient network errors, respecting Retry-After headers and capping at MAX_RETRY_DELAY_SECS
- NDJSON Auto-pagination: The --page-all flag streams paginated API results as newline-delimited JSON for pipeline-friendly processing with tools like jq
- Adversarial Input Validation: All CLI arguments are validated for path traversal, null bytes, control characters, dangerous Unicode (bidi overrides, zero-width chars), and URL injection before use
- Skill/Recipe/Persona Registry: TOML and Markdown registries define reusable automation patterns and role-based usage guides consumable by AI agents
- Dry-run Mode: Write operations support --dry-run to preview the JSON request body against the Discovery Document schema before execution

## 適用シーン
Useful for AI agents and LLM-based automation that need to interact with Google Workspace APIs via shell commands; shell scripting and CI/CD pipelines automating Gmail, Drive, Calendar, Sheets, Docs, and Chat; power users who want a single unified CLI for all Workspace services; and building persona-driven workflow automations such as executive assistant, project manager, or IT admin routines.

## 注意点・制約
Does not use generated google-* API crates; contributors must not add them. Discovery Document caching has a 24-hour TTL which may cause a brief lag when Google updates an API. The tool is frequently invoked by LLM agents so all CLI arguments are treated as untrusted; environment variables are trusted. TOCTOU race conditions in file path validation are acknowledged and not fully mitigated on all platforms. Helper (+verb) commands are only added when they provide multi-step orchestration value beyond a single API call.


## 関連ナレッジ
- (なし)
