---
source: https://github.com/msitarzewski/agency-agents
category: agent
sub_categories: [workflow, framework]
tags: [markdown, prompt-engineering, multi-agent, LLM, role-playing, system-prompt, AI-personas, agent-design]
language: 
ingested: 2026-04-10
source_updated: unknown
status: active
---

# agency-agents

# agency-agents

## 基本情報
- リポジトリ: https://github.com/msitarzewski/agency-agents
- カテゴリ: agent
- サブカテゴリ: workflow, framework
- タグ: markdown, prompt-engineering, multi-agent, LLM, role-playing, system-prompt, AI-personas, agent-design
- 最終確認日: 2026-04-10

## 概要
A curated collection of specialized AI agent personas defined as markdown files with YAML frontmatter, covering domains from engineering and design to marketing, sales, and academic analysis. Each agent has a structured personality, mission, workflow, and output templates. The repository also includes multi-agent workflow orchestration strategies and integration guides for popular AI coding tools.

## 設計思想
Agents are defined as self-contained markdown documents with consistent structure (identity, mission, rules, deliverables, workflow, communication style). The philosophy emphasizes domain expertise over generalism — each agent is a narrow specialist with opinionated constraints, concrete deliverables, and explicit anti-patterns. A 'nexus' orchestration layer coordinates multiple specialists across phased workflows.

## 主要コンポーネント
- Agent Markdown Files: Self-contained persona definitions with YAML frontmatter (name, description, color, emoji) and structured sections for identity, mission, rules, deliverables, and workflow
- Strategy Layer (strategy/): Multi-agent orchestration playbooks, runbooks for specific scenarios (startup MVP, incident response), and coordination templates for agent handoffs
- Integration Guides (integrations/): Instructions for deploying agents in specific tools like Cursor, Claude Code, Windsurf, Aider, and GitHub Copilot
- Examples (examples/): Concrete workflow demonstrations showing how multiple agents collaborate on tasks like landing pages, book chapters, and startup MVPs
- Scripts (scripts/): Shell utilities for installing agents, linting agent definitions, and converting formats

## 実装パターン
- Structured Agent Persona: Each agent file follows a fixed markdown schema: YAML frontmatter for metadata, then sections for Identity/Memory, Core Mission, Critical Rules, Technical Deliverables, Workflow Process, Communication Style, and Success Metrics
- Phased Orchestration: The strategy layer defines numbered phases (discovery → strategy → foundation → build → hardening → launch → operate) with specific agent assignments per phase
- Negative Constraint Rules: Agents include explicit 'Critical Rules You Must Follow' sections that define anti-patterns and forbidden behaviors, not just desired outputs
- Typed Deliverable Templates: Each agent provides structured output templates (markdown tables, code blocks, named schemas) so outputs are predictable and machine-parseable

## 適用シーン
Useful for teams building AI-assisted development workflows, content pipelines, or product development processes where different specialized LLM personas are needed. Ideal for Claude/GPT-based tooling where system prompts define agent behavior, and for anyone creating a multi-agent orchestration system covering the full software development lifecycle.

## 注意点・制約
Agents are prompt definitions only — no runtime, no execution engine, and no automated agent-to-agent communication is included. Quality depends entirely on the underlying LLM following the markdown instructions. The collection is opinionated and English-centric despite some China-market marketing agents. No versioning system for individual agent definitions.


## 関連ナレッジ
- (なし)
