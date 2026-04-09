---
source: https://github.com/czlonkowski/n8n-mcp
category: tool
sub_categories: [agent, workflow]
tags: [TypeScript, MCP, n8n, SQLite, workflow-automation, AI-integration, node-validation, Docker]
language: 
ingested: 2026-04-09
source_updated: unknown
status: active
---

# n8n-mcp

# n8n-mcp

## 基本情報
- リポジトリ: https://github.com/czlonkowski/n8n-mcp
- カテゴリ: tool
- サブカテゴリ: agent, workflow
- タグ: TypeScript, MCP, n8n, SQLite, workflow-automation, AI-integration, node-validation, Docker
- 最終確認日: 2026-04-09

## 概要
n8n-MCP is a Model Context Protocol (MCP) server that gives AI assistants deep, structured access to n8n's 525+ workflow automation nodes. It provides node discovery, documentation, validation, and workflow management tools, enabling AI assistants to build production-ready n8n workflows with high accuracy. The server reduces workflow creation time dramatically by eliminating guesswork through real-time validation and pre-configured task templates.

## 設計思想
The system is architected as a layered MCP server with a clear separation between the MCP protocol layer, service layer, and data layer. It follows a tool-oriented design where each capability (search, validate, generate, manage) is exposed as a discrete MCP tool. Data is persisted in SQLite with FTS5 for fast full-text search. A telemetry subsystem with privacy-first design tracks usage patterns. The server supports multiple deployment modes (stdio, HTTP, multi-tenant) and is designed for containerized deployment with Docker/Railway.

## 主要コンポーネント
- MCP Server (mcp/server.ts): Core MCP protocol handler exposing tools to AI clients via stdio or HTTP
- Tool Definitions (mcp/tool-docs/): Modular tool implementations organized by domain: discovery, validation, workflow management, system
- Node Repository (database/node-repository.ts): SQLite-backed data access layer for n8n node definitions with FTS5 search
- Workflow Validator (services/workflow-validator.ts): Validates n8n workflow JSON against node schemas and business rules
- Workflow Auto-Fixer (services/workflow-auto-fixer.ts): Automatically corrects common workflow configuration errors
- Telemetry System (telemetry/): Privacy-first usage tracking with mutation tracking, rate limiting, and error sanitization
- n8n API Client (services/n8n-api-client.ts): Communicates with live n8n instances for workflow CRUD and execution
- Template Service (templates/): Fetches, stores, and serves n8n community workflow templates
- HTTP Server (http-server.ts): REST/SSE bridge enabling multi-tenant MCP access over HTTP

## 実装パターン
- MCP Tool Modularization: Each MCP tool is implemented as a separate TypeScript module under mcp/tool-docs/ grouped by functional domain, then registered centrally via an index barrel, enabling easy addition or removal of capabilities
- SQLite FTS5 Search: Node and template discovery uses SQLite's FTS5 full-text search extension with OR/AND/FUZZY modes and relevance ranking, prebuilt at startup for fast queries
- Multi-Mode Deployment: The MCP engine supports stdio (for Claude Desktop), HTTP single-session, and HTTP multi-tenant modes, selected at startup via environment variables
- Workflow Diff Engine: Tracks workflow changes between versions using a structured diff format, enabling partial updates and rollback via versioned snapshots stored in SQLite
- Telemetry Mutation Tracking: All workflow mutations are hashed and tracked through a dedicated mutation tracker with rate limiting and sanitization to prevent sensitive data leakage
- Validation Profiles: Node validation supports multiple profiles (minimal, ai-friendly, strict) allowing AI clients to choose between speed and thoroughness
- Community Node Fetcher: Dynamically fetches and documents community n8n nodes from npm, expanding coverage beyond built-in nodes

## 適用シーン
Ideal for teams building AI-assisted n8n workflow automation, developers integrating Claude or other MCP-compatible AI assistants with n8n, projects requiring programmatic workflow generation and validation, and organizations wanting to reduce the expertise barrier for n8n workflow creation. Also useful as a reference implementation for building domain-specific MCP servers with SQLite backends.

## 注意点・制約
Requires a running n8n instance for workflow management tools; node database must be rebuilt when n8n updates. The FTS5 SQLite dependency requires a native build step. Multi-tenant HTTP mode has session isolation limitations. Community node documentation quality depends on npm package README quality. Telemetry cannot be fully disabled in some deployment configurations. Docker image size is significant due to bundled n8n node packages.


## 関連ナレッジ
- (なし)
