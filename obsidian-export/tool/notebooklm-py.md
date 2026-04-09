---
source: https://github.com/teng-lin/notebooklm-py
category: tool
sub_categories: [agent, workflow]
tags: [python, notebooklm, cli, google-api, async, playwright, rpc, automation]
language: 
ingested: 2026-04-09
source_updated: unknown
status: active
---

# notebooklm-py

# notebooklm-py

## 基本情報
- リポジトリ: https://github.com/teng-lin/notebooklm-py
- カテゴリ: tool
- サブカテゴリ: agent, workflow
- タグ: python, notebooklm, cli, google-api, async, playwright, rpc, automation
- 最終確認日: 2026-04-09

## 概要
notebooklm-py is a Python CLI and library providing programmatic access to Google NotebookLM, enabling automation of notebook management, source importing, AI content generation (podcasts, videos, quizzes), and chat interactions. It exposes capabilities beyond the web UI such as batch downloads, mind map extraction, and quiz export.

## 設計思想
Layered architecture separating CLI, Client API, Core HTTP/RPC, and protocol encoding. Uses async-first design with namespaced APIs (client.notebooks, client.sources, etc.) for clean organization. Authentication via Playwright browser session with automatic CSRF token refresh and profile-based multi-account management.

## 主要コンポーネント
- NotebookLMClient: Main async client class exposing all namespaced APIs (notebooks, sources, artifacts, chat, research, notes, settings, sharing)
- RPC Layer (rpc/): Handles Google's proprietary RPC protocol encoding/decoding and method ID management
- CLI Layer (cli/): Click-based CLI commands with Rich output, covering all client operations plus agent/skill integration
- auth.py + Playwright: Browser-based authentication that captures Google session cookies and persists them across CLI invocations
- ArtifactsAPI: Generates and downloads AI artifacts: audio overviews, video overviews, slide decks, infographics, quizzes, flashcards, mind maps, reports

## 実装パターン
- Async Context Manager Client: Client is used as async context manager to manage HTTP connections via httpx, with automatic auth token refresh on 401/403 responses
- Profile-based Multi-account: Isolated per-profile directories under ~/.notebooklm/profiles/<name>/ for storage_state.json, context.json, and browser_profile
- Async Polling with wait_for_completion: Long-running generation tasks return task_id immediately; callers poll via artifact wait or use blocking --wait flag with exponential backoff
- Partial ID Matching: CLI commands accept partial notebook/artifact IDs as unique prefixes, resolved server-side or locally
- VCR Integration Testing: HTTP interactions recorded as cassettes for offline deterministic replay at both client and CLI levels, with sensitive data scrubbing

## 適用シーン
Automating research-to-podcast pipelines, bulk importing sources into NotebookLM, CI/CD workflows generating study materials from documents, LLM agent integration for programmatic notebook management, batch downloading artifacts, and exporting quizzes/flashcards/mind maps in structured formats.

## 注意点・制約
Depends on undocumented Google RPC protocol that may change without notice; authentication requires periodic re-login (sessions expire every 1-2 weeks); rate limiting on generation endpoints is undocumented; Playwright only required for login (not for other operations); video/audio generation can take 15-30+ minutes.


## 関連ナレッジ
- (なし)
