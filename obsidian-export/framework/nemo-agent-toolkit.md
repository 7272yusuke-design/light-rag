---
source: https://github.com/NVIDIA/NeMo-Agent-Toolkit
category: framework
sub_categories: [agent, workflow]
tags: [python, LLM, multi-agent, LangChain, MCP, RAG, observability, plugin-architecture]
language: 
ingested: 2026-04-09
source_updated: unknown
status: active
---

# nemo-agent-toolkit

# NeMo-Agent-Toolkit

## 基本情報
- リポジトリ: https://github.com/NVIDIA/NeMo-Agent-Toolkit
- カテゴリ: framework
- サブカテゴリ: agent, workflow
- タグ: python, LLM, multi-agent, LangChain, MCP, RAG, observability, plugin-architecture
- 最終確認日: 2026-04-09

## 概要
NVIDIA NeMo Agent Toolkit (NAT) is a Python framework for building, running, evaluating, and optimizing LLM-powered agentic workflows. It provides a plugin-based architecture that integrates with multiple AI frameworks (LangChain, LlamaIndex, AutoGen, Haystack, Semantic Kernel, Strands, CrewAI, Google ADK), supports various agent patterns (ReAct, ReWOO, tool-calling, router), and includes built-in tooling for observability, evaluation, fine-tuning, and profiling. The toolkit exposes workflows via REST API, MCP, and A2A protocols.

## 設計思想
Plugin-driven, framework-agnostic architecture where every capability (LLMs, agents, memory, retrievers, evaluators, telemetry exporters, front-ends) is a registered component. A YAML/config-based workflow definition is compiled into a computation graph (nvidia_nat_app) and executed with speculative scheduling. The toolkit separates concerns into discrete packages (nvidia_nat_core, nvidia_nat_langchain, nvidia_nat_eval, etc.) that extend a common builder/registry pattern, enabling users to swap or extend individual pieces without changing the rest of the system.

## 主要コンポーネント
- nvidia_nat_core: Core framework: builder, CLI, data models, LLM providers, front-ends (FastAPI/console), middleware, observability pipeline, retriever interfaces, runtime
- nvidia_nat_app: Workflow compiler and executor: compiles config graphs, performs static analysis, speculative execution planning, and scheduling
- nvidia_nat_langchain: LangChain/LangGraph integration: ReAct, ReWOO, tool-calling, router, parallel/sequential agents, LangSmith evaluation
- nvidia_nat_eval / nvidia_nat_atif: Evaluation harness and ATIF (Agentic Trajectory Intermediate Format) for trajectory-based LLM evaluation
- nvidia_nat_profiler: Performance profiling, token usage analysis, bottleneck detection, GPU sizing calculator
- nvidia_nat_mcp / nvidia_nat_fastmcp: Model Context Protocol server and client integration for exposing/consuming tools over MCP
- nvidia_nat_a2a: Agent-to-Agent (A2A) protocol support for inter-agent communication
- nvidia_nat_config_optimizer: Prompt and configuration optimization using genetic algorithms and Pareto-front analysis
- nvidia_nat_security: Red-teaming, defense middleware (PII, content guard, output verification), and security evaluation
- Middleware stack: Composable middleware for caching, logging, defense, red-teaming, timeout, and dynamic function injection

## 実装パターン
- Plugin Registry Pattern: All components (LLMs, agents, tools, evaluators, exporters) self-register via a decorator/register() mechanism discovered at import time, enabling zero-config extensibility
- Config-Driven Workflow Compilation: Workflows are defined in YAML config files; the compiler (nvidia_nat_app) performs topology analysis, LLM detection, edge classification, and produces an optimized execution graph
- Speculative Execution: The planner speculatively schedules branches (e.g., router branches) before the LLM decision is made, improving throughput at the cost of potential wasted work
- ATIF Trajectory Format: A canonical intermediate representation for agent trajectories enabling framework-agnostic evaluation, fine-tuning data generation, and replay
- Middleware Pipeline: Function calls pass through a composable middleware chain (cache → log → defense → timeout) before reaching the actual function implementation
- Multi-Framework Wrapping: Each third-party framework (LangChain, AutoGen, Haystack, etc.) is wrapped with a callback handler and tool/LLM adapter so NAT's observability and config system apply uniformly

## 適用シーン
Teams building production LLM agents and pipelines who need: a unified framework spanning multiple AI libraries, built-in evaluation and profiling, MCP/A2A protocol exposure, fine-tuning data generation from agent trajectories, security red-teaming, and GPU cluster sizing. Suitable for enterprise AI platform teams, MLOps engineers, and AI application developers who want a batteries-included agentic toolkit with NVIDIA ecosystem integrations (NIM, NeMo Customizer, Dynamo).

## 注意点・制約
Large monorepo with many optional sub-packages; users must install only the plugins they need. Speculative execution may waste compute on incorrect branches. ATIF trajectory format is NVIDIA-specific and may require adapters for other evaluation tooling. Fine-tuning integrations (NeMo Customizer, OpenPipe ART) require external service credentials. The MCP and A2A protocol support is relatively new and marked experimental in places. Dynamo integration requires a separately deployed Dynamo inference stack.


## 関連ナレッジ
- (なし)
