---
source: https://github.com/langchain-ai/langgraph
category: framework
sub_categories: [agent, workflow]
tags: [python, langgraph, pregel, state-machine, multi-agent, checkpointing, LLM, graph-execution]
language: 
ingested: 2026-04-09
source_updated: unknown
status: active
---

# langgraph

# langgraph

## 基本情報
- リポジトリ: https://github.com/langchain-ai/langgraph
- カテゴリ: framework
- サブカテゴリ: agent, workflow
- タグ: python, langgraph, pregel, state-machine, multi-agent, checkpointing, LLM, graph-execution
- 最終確認日: 2026-04-09

## 概要
LangGraph is an open-source Python framework for building stateful, multi-actor AI agent applications using a graph-based execution model (Bulk Synchronous Parallel via the Pregel engine). It supports two authoring styles — a declarative StateGraph API and a functional API (@entrypoint/@task decorators) — both compiling to the same Pregel runtime. The framework provides checkpointing, tool execution with runtime injection, remote graph composition, Docker-based deployment via CLI, and a beta SDK encryption framework.

## 設計思想
LangGraph adopts a Pregel-inspired Bulk Synchronous Parallel execution model where user-defined nodes process shared state through typed channels. State transitions are governed by channel semantics (LastValue, BinaryOperatorAggregate, Topic, etc.), enabling deterministic, resumable, and auditable agent workflows. Persistence is decoupled via pluggable checkpoint backends (Postgres, SQLite, in-memory), and trust boundaries are explicitly defined between user code, the framework core, storage, and remote APIs. The design philosophy separates authoring API (StateGraph vs. functional) from the execution engine, ensuring both compile to the same Pregel runtime.

## 主要コンポーネント
- Pregel Engine: Core graph execution engine implementing Bulk Synchronous Parallel semantics; handles step execution, interrupt/resume, durability modes, and stream output
- StateGraph / Channels: Declarative graph builder API with typed channels (LastValue, BinaryOperatorAggregate, Topic, etc.) that enforce state update semantics
- Functional API (@entrypoint/@task): Decorator-based authoring API for function-centric workflows with retry and cache policies, compiling to the same Pregel runtime
- JsonPlusSerializer / EncryptedSerializer: Checkpoint serialization layer supporting msgpack, JSON, and pickle codecs with a 47-entry type allowlist; optional AES-EAX authenticated encryption wrapper
- ToolNode: Prebuilt node that dispatches LLM-generated tool calls to registered BaseTool instances with InjectedState/InjectedStore/ToolRuntime injection
- CheckpointSaver backends: Pluggable persistence backends (PostgreSQL, SQLite, in-memory) storing serialized graph state for resumability and human-in-the-loop workflows
- RemoteGraph: Client implementing PregelProtocol for composing graphs across LangGraph Server API boundaries via HTTPS/SSE
- langgraph-cli: CLI tooling for Docker-based build and deployment (langgraph up/build/dev/new) with config schema validation and WebhookUrlPolicy SSRF protection
- SDK (langgraph_sdk): Python HTTP client for LangGraph Server API with SSE streaming, auth handler framework, and beta encryption handler registration
- BaseCache: Caching layer for task results keyed by task identity, using JsonPlusSerializer with pickle_fallback=False

## 実装パターン
- Pregel Bulk Synchronous Parallel: Graph execution proceeds in discrete supersteps; all active nodes in a step execute, write to channels, then the next step begins — enabling deterministic parallel execution and reproducible checkpoints
- Typed Channel State: Graph state is decomposed into named channels with explicit update semantics (last-value, reducer, topic, barrier, ephemeral), enforcing predictable state transitions across concurrent node writes
- Checkpoint-backed Resumability: After every superstep the complete channel state is serialized and persisted, allowing graphs to be interrupted (human-in-the-loop) and resumed from any prior checkpoint
- Runtime Tool Injection: InjectedState, InjectedStore, and ToolRuntime annotations cause ToolNode to merge system-controlled values into tool arguments after LLM-supplied args, ensuring system values always win on key collision and injected param names are hidden from LLM schema
- Pluggable Serde with Allowlist Deserialization: JsonPlusSerializer dispatches on type-tag prefixes (msgpack, json, pickle, bytes, null) and enforces a 47-entry SAFE_MSGPACK_TYPES allowlist plus a 1-entry SAFE_MSGPACK_METHODS allowlist to constrain deserialization attack surface
- Config Sanitization for Remote Graphs: _sanitize_config strips non-primitive values and internal checkpoint keys before transmitting config to remote LangGraph Server, preventing accidental secret leakage across API boundaries

## 適用シーン
LangGraph is suited for: (1) building multi-step, stateful LLM agent applications that require persistence, human-in-the-loop interrupts, and resumability; (2) implementing multi-agent architectures (hierarchical teams, collaborative agents, supervisor patterns); (3) complex RAG pipelines with adaptive, self-corrective, or agentic retrieval; (4) long-running workflows where fault tolerance and step-level checkpointing are critical; (5) production deployments of agent systems via the LangGraph Server with the CLI tooling.

## 注意点・制約
1. Msgpack deserialization allows arbitrary module imports by default (LANGGRAPH_STRICT_MSGPACK not set) — database write access is equivalent to RCE. 2. pickle_fallback=True enables unrestricted pickle.loads; should never be used with untrusted checkpoint storage. 3. EncryptedSerializer silently accepts unencrypted data (no type-tag enforcement), allowing encryption bypass by a storage-level attacker. 4. SDK HttpClient forwards x-api-key headers to server-controlled Location redirects without URL validation — use only with trusted LangGraph Server endpoints. 5. Checkpoint data has no built-in TTL or pruning, leading to unbounded PII retention. 6. RemoteGraph performs no schema validation on inbound stream data; compromised servers can inject arbitrary field values into Interrupt/Command objects. 7. The SDK Encryption context() handler registration skips signature validation (_validate_handler not called), deferring failures to server-side invocation.


## 関連ナレッジ
- (なし)
