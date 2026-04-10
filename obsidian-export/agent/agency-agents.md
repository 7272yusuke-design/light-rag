---
source: https://github.com/msitarzewski/agency-agents
category: agent
sub_categories: [workflow, framework]
tags: [markdown, prompt-engineering, multi-agent, LLM, system-prompt, AI-persona, role-based, knowledge-base]
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
- タグ: markdown, prompt-engineering, multi-agent, LLM, system-prompt, AI-persona, role-based, knowledge-base
- 最終確認日: 2026-04-10

## 概要
A curated collection of specialized AI agent personas defined as structured Markdown files with YAML frontmatter, covering domains from engineering and design to marketing, sales, and academia. Each agent encodes expert knowledge, behavioral rules, output templates, and communication styles to guide LLMs toward domain-specific, high-quality responses. The repository also includes multi-agent orchestration strategies, integration guides for popular AI coding tools, and example workflows demonstrating agent collaboration.

## 設計思想
Agents are modeled as self-contained 'expert personalities' rather than simple instruction sets. Each file combines identity declaration, hard constraints, structured deliverable templates, and workflow steps into a single Markdown document. The system favors depth and specificity over generality, requiring every agent to cite named frameworks, produce concrete artifacts, and enforce quality gates. Multi-agent coordination is handled through explicit handoff templates and phase-based runbooks rather than runtime orchestration infrastructure.

## 主要コンポーネント
- Agent Markdown files: Define individual expert personas with YAML frontmatter (name, description, color, emoji), behavioral rules, output templates, and communication style
- strategy/playbooks: Phase-by-phase project runbooks (discovery through operations) that sequence agent activation across a full product lifecycle
- strategy/coordination: Agent activation prompts and handoff templates that enable structured multi-agent workflows
- integrations/: Setup guides for embedding agents into tools like Cursor, Claude Code, GitHub Copilot, Aider, Windsurf, and MCP Memory
- examples/: End-to-end workflow demonstrations (startup MVP, landing page, book chapter, memory-augmented sessions)
- scripts/: Shell utilities for installing agents, linting frontmatter, and converting formats

## 実装パターン
- Persona-as-file: Each agent is a standalone Markdown file with YAML frontmatter for metadata and structured sections (identity, mission, rules, templates, workflow, metrics) that fully specify an expert persona
- Hard-constraint injection: Every agent includes a 'Critical Rules' section with explicit prohibitions and requirements (e.g., 'Rivers don't split', 'No culture salad') to prevent common LLM failure modes in that domain
- Deliverable templates: Agents ship with copy-paste output templates (code blocks, Markdown tables, structured reports) that enforce consistent, actionable output format
- Phase-based orchestration: Runbooks sequence multiple agents across project phases with explicit handoff points, enabling reproducible multi-agent workflows without runtime infrastructure
- Tool integration via context injection: Agents are activated in external tools (Cursor, Claude Code, etc.) by loading the Markdown file into the system context or custom instructions slot

## 適用シーン
Useful for teams building AI-assisted workflows who want pre-built, deeply specialized agent personas rather than generic assistants. Ideal for: software product teams needing an orchestrated set of engineering, design, and marketing agents; worldbuilding or game development projects requiring culturally and geographically coherent creative advisors; enterprises wanting standardized expert AI personas for sales, legal compliance, or project management; and developers integrating AI into IDEs or coding assistants who need domain-specific behavioral guardrails.

## 注意点・制約
Agents are prompt-engineering artifacts, not executable code—quality of output depends heavily on the underlying LLM capability and context window size. No runtime orchestration engine is included; multi-agent coordination relies on manual or tool-assisted context passing. Frontmatter fields (name, description, color) are used for documentation/UI purposes only and carry no programmatic enforcement. Some agents reference real-world frameworks (Bowlby, Braudel, McKee) whose applicability varies by task; the LLM may hallucinate citations if not grounded by retrieval. Cultural and domain-specific agents (anthropologist, historian, psychologist) include explicit bias warnings but cannot guarantee accuracy without human expert review.


## 関連ナレッジ
- (なし)
