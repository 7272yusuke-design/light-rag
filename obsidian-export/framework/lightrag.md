---
source: https://github.com/HKUDS/LightRAG
category: framework
sub_categories: [webapp, tool]
tags: [python, typescript, rag, knowledge-graph, llm, fastapi, react, graph-database, vector-database]
language: 
ingested: 2026-04-09
source_updated: unknown
status: active
---

# lightrag

# LightRAG

## 基本情報
- リポジトリ: https://github.com/HKUDS/LightRAG
- カテゴリ: framework
- サブカテゴリ: webapp, tool
- タグ: python, typescript, RAG, knowledge-graph, LLM, FastAPI, React, graph-database, vector-database
- 最終確認日: 2026-04-09

## 概要
LightRAG is a production-ready Retrieval-Augmented Generation (RAG) framework that builds and queries knowledge graphs from documents. It supports multiple LLM providers (OpenAI, Gemini, Ollama, etc.) and storage backends (Neo4j, PostgreSQL, MongoDB, Milvus, Qdrant, Redis, etc.) with a FastAPI server and React-based WebUI.

## 設計思想
LightRAG follows a plugin-based dependency injection architecture where LLM providers, embedding models, and storage backends are interchangeable components. Core operations (entity extraction, graph building, retrieval) are separated from infrastructure concerns. The system uses async-first patterns throughout, with priority-based LLM request queuing, linear gradient weighted polling for context building, and workspace isolation for multi-tenant deployments.

## 主要コンポーネント
- lightrag/lightrag.py: Core RAG engine: document ingestion, entity/relation extraction, graph construction, and multi-mode query execution (naive/local/global/hybrid/mix)
- lightrag/operate.py: Implements the indexing pipeline and retrieval algorithms including knowledge graph entity extraction and context building
- lightrag/api/lightrag_server.py: FastAPI REST API server with JWT authentication, document management, graph exploration, and Ollama-compatible endpoints
- lightrag/kg/: Pluggable storage implementations for vector DB (Milvus, Qdrant, FAISS, NanoVectorDB), graph DB (Neo4j, NetworkX, Memgraph), and KV/doc stores (PostgreSQL, MongoDB, Redis, JSON)
- lightrag/llm/: LLM and embedding provider adapters for OpenAI, Azure, Gemini, Anthropic, Bedrock, Ollama, HuggingFace, LlamaIndex, and others
- lightrag_webui/: React/TypeScript WebUI for document upload, graph visualization (Sigma.js), interactive retrieval testing, and system status monitoring
- lightrag/prompt.py: Prompt templates for entity extraction, relationship extraction, and query answering in the RAG pipeline
- lightrag/rerank.py: Reranking support for retrieved chunks using models like BGE-reranker

## 実装パターン
- Pluggable Storage Backend: All storage types (vector, graph, KV, document status) implement abstract base classes defined in base.py, allowing runtime selection of backend without changing core logic
- Async-First with Concurrency Control: All I/O operations are async; LLM requests use a priority queue with configurable max_async concurrency; locks use sorted key ordering to prevent deadlocks
- Dual-Level Graph Retrieval: Queries are answered using both local (entity-centric) and global (community/relation-level) retrieval, combined in hybrid and mix modes
- Workspace Isolation: Each LightRAG instance can use a named workspace/namespace for multi-tenant data isolation across all storage backends
- Snapshot-before-yield for Async Generators: Async generators that iterate shared storage take a snapshot while holding the lock, release the lock, then yield — preventing deadlocks when source and target share locks
- Embedding Format Normalization: Embedding functions handle both base64-encoded and raw array formats from different provider endpoints, normalizing to numpy float32 arrays

## 適用シーン
Projects that need to build a queryable knowledge graph from large document corpora; enterprise RAG systems requiring production-grade storage flexibility (swap between PostgreSQL, Neo4j, Milvus, etc.); applications needing multi-LLM-provider support with a unified API; teams wanting a self-hosted RAG server with WebUI, REST API, and Ollama-compatible endpoints for integration with existing tooling.

## 注意点・制約
Knowledge graph quality depends heavily on LLM extraction quality and prompt tuning. Large document sets require significant LLM API calls during indexing, incurring cost and latency. Multimodal support requires the separate RAG-Anything package. Some storage backends (PostgreSQL with AGE, Memgraph) require specific database extensions. The WebUI must be built separately from source before use in development mode (requires Bun). Integration tests require live database/API connections and are skipped in CI by default.


## 関連ナレッジ
- (なし)
