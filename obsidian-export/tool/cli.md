---
source: https://github.com/cli/cli
category: tool
sub_categories: [workflow, agent]
tags: [golang, github-cli, cli, graphql, rest-api, git, authentication, extensions]
language: 
ingested: 2026-04-11
source_updated: unknown
status: active
---

# cli

# cli

## 基本情報
- リポジトリ: https://github.com/cli/cli
- カテゴリ: tool
- サブカテゴリ: workflow, agent
- タグ: golang, github-cli, cli, graphql, rest-api, git, authentication, extensions
- 最終確認日: 2026-04-11

## 概要
GitHub CLI (gh) is the official command-line tool for interacting with GitHub. It provides comprehensive commands for managing repositories, pull requests, issues, GitHub Actions workflows, codespaces, and more directly from the terminal. It also supports extensions, attestation/verification, and AI-powered features.

## 設計思想
The project follows a modular command-based architecture using Cobra CLI framework, with each command group (pr, issue, repo, etc.) organized into separate packages under pkg/cmd. A shared factory pattern provides dependency injection for HTTP clients, authentication, git context, and I/O streams. The tool prioritizes scriptability (JSON output), extensibility (plugin system), and both human-readable and machine-readable output modes.

## 主要コンポーネント
- cmd/gh/main.go: Entry point that bootstraps the CLI application
- pkg/cmd/root: Root command registration, alias resolution, and extension command integration
- pkg/cmdutil/factory.go: Dependency injection factory providing auth, HTTP client, git client, and IO streams to all commands
- api/: GitHub REST and GraphQL API client wrappers with typed query builders
- internal/config/: Multi-account config management with migration support and keyring integration
- pkg/cmd/attestation/: Artifact attestation and verification using Sigstore/TUF for supply chain security
- pkg/cmd/extension/: Extension manager for installing, upgrading, and running third-party gh extensions
- internal/codespaces/: Codespaces management including SSH tunneling, port forwarding, and gRPC-based RPC
- pkg/cmd/agent-task/: AI agent task management for running and monitoring automated agent jobs
- acceptance/: End-to-end acceptance tests using txtar script format against real GitHub API

## 実装パターン
- Command Factory Pattern: Each command receives a Factory struct via closure, enabling testable dependency injection of HTTP clients, auth config, IO streams, and git client without global state
- Cobra Subcommand Grouping: Commands are organized hierarchically using Cobra with custom command groups (cmdgroup) for categorized help output
- GraphQL Query Builder: Dynamic GraphQL query construction allowing callers to request only needed fields, reducing over-fetching
- JSON Fields Filtering: Uniform --json and --jq flags across commands enable machine-readable output by selecting and transforming response fields
- txtar Acceptance Tests: End-to-end tests written as txtar script files that execute real gh commands against live GitHub API using testscript runner
- Extension Plugin System: Third-party extensions installed as git repos or binaries, discovered and executed transparently as gh subcommands
- Sigstore/TUF Attestation: Artifact attestation verification using Sigstore bundle format and TUF root of trust for release asset integrity

## 適用シーン
Useful as a reference implementation for building large-scale CLI tools in Go with multi-command structure, authentication flows, API client patterns, extension systems, and acceptance testing strategies. Also serves as the primary tool for GitHub automation in CI/CD pipelines, developer workflows, and scripting scenarios.

## 注意点・制約
Requires Go 1.26+. PRs are only accepted for issues labeled 'help wanted'. Core features are maintained exclusively by the GitHub CLI team. Extension ecosystem quality varies. Codespaces and attestation features have separate ownership teams. Acceptance tests require live GitHub credentials and organization access.


## 関連ナレッジ
- (なし)
