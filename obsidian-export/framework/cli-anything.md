---
source: https://github.com/HKUDS/CLI-Anything
category: framework
sub_categories: [agent, tool]
tags: [python, typescript, cli, ai-agent, gui-automation, repl, click, plugin-architecture]
language: 
ingested: 2026-04-09
source_updated: unknown
status: active
---

# cli-anything

# CLI-Anything

## 基本情報
- リポジトリ: https://github.com/HKUDS/CLI-Anything
- カテゴリ: framework
- サブカテゴリ: agent, tool
- タグ: python, typescript, cli, ai-agent, gui-automation, repl, click, plugin-architecture
- 最終確認日: 2026-04-09

## 概要
CLI-Anything is a framework for building stateful CLI harnesses for GUI applications, enabling AI agents to control software like GIMP, Blender, Audacity, and 30+ other tools via command-line interfaces. Each harness wraps a target application's API or automation interface with a consistent Python CLI built on Click, featuring REPL mode and JSON output for agent consumption.

## 設計思想
The 'harness methodology' (HARNESS.md) defines a uniform pattern: each software gets a self-contained Python package with a core/ layer (domain logic), utils/ layer (backend adapter + REPL skin), skills/SKILL.md (agent-facing capability description), and a Click-based CLI entry point. A shared repl_skin.py provides consistent branding and UX across all harnesses. The architecture enforces separation between API communication (backend), domain operations (core), and CLI presentation.

## 主要コンポーネント
- HARNESS.md: Canonical methodology document defining structure and conventions for building CLI harnesses
- repl_skin.py: Shared terminal UI component providing consistent REPL branding, tables, prompts, and colored output across all harnesses
- skill_generator.py: Generates SKILL.md capability descriptions for AI agent consumption
- cli-anything-plugin: Claude/Pi coding agent plugin with slash commands for building, refining, testing, and validating harnesses
- registry.json: Central registry of all available CLI harnesses for the CLI-Hub web directory
- *_backend.py: Per-software adapter that wraps the real application API or automation interface
- SKILL.md: Agent-readable capability document describing commands, usage, and examples for each harness

## 実装パターン
- Backend Adapter Pattern: Each harness isolates all real application communication in a *_backend.py module, allowing unit tests to mock it without the real application
- Dual Output Mode: All CLI commands support --json flag for machine-readable output alongside human-readable formatted output, enabling both interactive and agent use
- REPL + One-shot Commands: Every harness supports both interactive REPL mode with history/completion and direct subcommand invocation for scripting and agent pipelines
- Session State Management: In-memory session objects track connection config, history, undo/redo state within a REPL session
- Skill-based Agent Interface: Each harness ships a SKILL.md describing its capabilities in a format consumable by AI coding agents like Claude

## 適用シーン
Projects needing AI agents to control desktop GUI applications programmatically; building automation pipelines for creative software (video editing, 3D modeling, audio); network/infrastructure management via agent; any workflow requiring a consistent CLI abstraction over software that lacks one natively.

## 注意点・制約
Each harness requires the target application to be separately installed and running; E2E tests require real application instances (some use Docker); repl_skin.py must be copied verbatim into each harness (single source of truth constraint); harnesses are application-version-sensitive as they depend on specific APIs or automation interfaces.


## 関連ナレッジ
- (なし)
