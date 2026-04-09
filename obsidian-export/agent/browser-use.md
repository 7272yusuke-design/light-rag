---
source: https://github.com/browser-use/browser-use
category: agent
sub_categories: [framework, tool]
tags: [python, browser-automation, LLM, playwright, CDP, multi-LLM, web-scraping, asyncio]
language: 
ingested: 2026-04-09
source_updated: unknown
status: active
---

# browser-use

# browser-use

## 基本情報
- リポジトリ: https://github.com/browser-use/browser-use
- カテゴリ: agent
- サブカテゴリ: framework, tool
- タグ: python, browser-automation, LLM, playwright, CDP, multi-LLM, web-scraping, asyncio
- 最終確認日: 2026-04-09

## 概要
browser-use is a Python framework that enables LLM-powered agents to control web browsers via CDP (Chrome DevTools Protocol). It integrates with multiple LLM providers (OpenAI, Anthropic, Gemini, etc.) to perform autonomous web tasks like form filling, data extraction, and multi-step navigation. The framework provides both high-level agent abstractions and low-level browser control primitives.

## 設計思想
Layered architecture separating concerns: Actor (raw CDP browser control), Agent (LLM reasoning loop with message management), Browser (session/tab management with watchdogs), DOM (page state serialization for LLM consumption), and Tools (action registry). The agent loop uses a message manager that maintains history compaction, sensitive data filtering, and multi-modal inputs. Supports both cloud-hosted and local browser sessions with pluggable LLM backends.

## 主要コンポーネント
- Agent (agent/service.py): Core LLM reasoning loop that takes tasks, observes browser state, and executes actions step by step
- MessageManager (agent/message_manager/): Manages conversation history, token limits, sensitive data filtering, and history compaction for LLM context
- BrowserSession (browser/session.py): Manages browser lifecycle, tabs, CDP connections, and watchdog processes
- Actor (actor/): Low-level CDP wrapper providing Page, Element, and Mouse abstractions for direct browser control
- DomService (dom/service.py): Serializes DOM state into LLM-friendly representations with element indexing for action targeting
- LLM adapters (llm/): Unified interface for 15+ LLM providers including OpenAI, Anthropic, Gemini, Ollama, Groq, etc.
- Tools/Controller (tools/, controller/): Registry of browser actions (click, fill, extract, navigate) that the agent can invoke
- Watchdogs (browser/watchdogs/): Background monitors for captchas, crashes, popups, downloads, security, and recording

## 実装パターン
- Structured LLM output for actions: Agent receives DOM snapshot and produces structured JSON action commands; LLM output is parsed into typed action models via Pydantic
- History compaction: MessageManager periodically summarizes older conversation history into compact memory blocks to stay within LLM context limits
- Sensitive data masking: Sensitive values (passwords, tokens) are replaced with placeholder tags before being sent to LLM and restored during actual browser interactions
- Watchdog pattern: Background async tasks monitor browser state for common edge cases (captcha, crash, popups) and trigger appropriate handling
- Multi-provider LLM abstraction: Unified BaseChatModel interface with provider-specific serializers allows swapping LLM backends without changing agent code

## 適用シーン
Automating repetitive web tasks (form filling, data extraction, job applications, price monitoring), building AI assistants that browse the web, QA testing with natural language instructions, web scraping with dynamic content, and agentic workflows that require multi-step browser interaction across multiple sites.

## 注意点・制約
Browser automation is inherently fragile against DOM changes and anti-bot measures. LLM costs accumulate rapidly on long tasks. Sensitive data handling requires careful configuration. Cloud browser sessions add latency. The actor layer (CDP) is lower-level than Playwright and may require careful coordination for complex interactions. History compaction may lose context for very long tasks.


## 関連ナレッジ
- (なし)
