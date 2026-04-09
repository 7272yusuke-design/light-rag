---
source: https://github.com/anthropics/anthropic-cookbook
category: workflow
sub_categories: [agent, pattern]
tags: [python, jupyter, claude-api, RAG, multi-agent, LLM-evals, anthropic-sdk, MCP]
language: 
ingested: 2026-04-09
source_updated: unknown
status: active
---

# anthropic-cookbook

# anthropic-cookbook

## 基本情報
- リポジトリ: https://github.com/anthropics/anthropic-cookbook
- カテゴリ: workflow
- サブカテゴリ: agent, pattern
- タグ: python, jupyter, claude-api, RAG, multi-agent, LLM-evals, anthropic-sdk, MCP
- 最終確認日: 2026-04-09

## 概要
Anthropic Cookbook is a comprehensive collection of Jupyter notebooks demonstrating how to build with the Claude API. It covers capabilities like RAG, classification, summarization, tool use, agents, multimodal, fine-tuning, and extended thinking. The repo also includes Claude Agent SDK examples, managed agent patterns, and reusable skills.

## 設計思想
Organized as a learning-first resource following a problem-focused pedagogical approach (Diataxis-inspired). Each notebook leads with the problem being solved, states Terminal Learning Objectives upfront, and maps back to them in conclusions. Code is demonstration-driven rather than documentation-driven, with clean separation of capabilities, patterns, and integrations.

## 主要コンポーネント
- capabilities/: Notebooks demonstrating core Claude capabilities: RAG, classification, summarization, text-to-SQL, knowledge graphs, contextual embeddings
- patterns/agents/: Agent architecture patterns including orchestrator-workers, evaluator-optimizer, and basic agentic workflows
- claude_agent_sdk/: SDK-based agent examples: chief of staff, observability, SRE, research agents with real tool use and hooks
- managed_agents/: Claude Managed Agents (CMA) examples for production use cases: iterate, gate, orchestrate, SRE incident response
- tool_use/: Tool/function calling patterns including parallel tools, structured output, memory, context engineering
- skills/: Reusable Claude skill bundles for financial analysis, brand guidelines, and custom skill development
- .claude/: Claude Code configuration including custom agents (code-reviewer), slash commands, and cookbook audit skill
- third_party/: Integration examples with LlamaIndex, Pinecone, MongoDB, ElevenLabs, Deepgram, VoyageAI

## 実装パターン
- RAG Pipeline: End-to-end retrieval-augmented generation with vector DBs, evaluation datasets, and promptfoo integration
- Evaluator-Optimizer Loop: Iterative agent pattern where one model evaluates outputs and another optimizes based on feedback
- Orchestrator-Workers: Multi-agent pattern with a coordinator dispatching subtasks to specialized worker agents
- Human-in-the-Loop Gate: CMA pattern that pauses agent execution for human approval before proceeding
- Skill Bundles: Packaged reusable capabilities (SKILL.md + Python scripts) that Claude can load and execute for domain-specific tasks
- Contextual Embeddings: Enhanced RAG using context-aware chunk embedding via Lambda functions and S3
- Prompt Caching: Speculative and standard prompt caching patterns to reduce latency and cost

## 適用シーン
Useful for developers learning to build production AI features with Claude: RAG systems, classification pipelines, multi-agent workflows, CI/CD observability bots, data analyst agents, Slack bots, SRE incident responders, and custom skill development. Also serves as a reference for teams adopting Claude Agent SDK or Managed Agents in production.

## 注意点・制約
Notebooks are educational, not production-ready — minimal error handling by design. Model names and API patterns may become outdated as Claude versions evolve. Some integrations require third-party API keys (VoyageAI, Pinecone, ElevenLabs, etc.). Managed Agents (CMA) notebooks require specific Anthropic access.


## 関連ナレッジ
- (なし)
