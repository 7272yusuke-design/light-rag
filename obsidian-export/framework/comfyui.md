---
source: https://github.com/comfyanonymous/ComfyUI
category: framework
sub_categories: [webapp, workflow]
tags: [python, stable-diffusion, image-generation, node-based, diffusion-models, pytorch, aiohttp, sqlalchemy]
language: 
ingested: 2026-04-09
source_updated: unknown
status: active
---

# comfyui

# ComfyUI

## 基本情報
- リポジトリ: https://github.com/comfyanonymous/ComfyUI
- カテゴリ: framework
- サブカテゴリ: webapp, workflow
- タグ: python, stable-diffusion, image-generation, node-based, diffusion-models, pytorch, aiohttp, SQLAlchemy
- 最終確認日: 2026-04-09

## 概要
ComfyUI is a node-based GUI and backend framework for running Stable Diffusion and other generative AI models. It provides a visual workflow editor where users can compose image, video, and audio generation pipelines by connecting nodes. The system supports a wide range of models including Flux, Wan, HunyuanVideo, and dozens of third-party API integrations.

## 設計思想
Modular node-based architecture where each processing step (sampling, encoding, decoding, conditioning) is a discrete node with typed inputs/outputs. The execution engine caches intermediate results for efficiency, supports lazy graph evaluation, and separates model management (memory, VRAM, quantization) from business logic. API nodes follow a versioned contract system for stable external interfaces.

## 主要コンポーネント
- comfy/: Core inference engine: model loading, sampling, VAE, CLIP, ControlNet, LoRA, memory management
- nodes.py: Built-in node definitions and registration for the node graph system
- execution.py: Graph execution engine with caching, lazy evaluation, and job scheduling
- server.py: aiohttp-based WebSocket and REST API server for frontend communication
- comfy_api_nodes/: Nodes wrapping third-party AI APIs (OpenAI, Runway, Kling, etc.)
- comfy_extras/: Extended node library covering audio, video, 3D, advanced samplers, and post-processing
- app/assets/: Asset management system with SQLite/Alembic database for model/file cataloging
- comfy_api/: Versioned Python API for custom node developers with typed I/O contracts
- comfy_execution/: Caching, graph validation, progress tracking, and job management subsystem
- blueprints/: Pre-built workflow JSON templates for common generation tasks

## 実装パターン
- Node Registry Pattern: Nodes self-register via NODE_CLASS_MAPPINGS dict; the server discovers all nodes at startup and exposes their input/output schemas to the frontend
- Lazy Graph Execution with Caching: comfy_execution/caching.py implements multi-level result caching so unchanged subgraphs are not re-executed between runs
- Model Patcher: comfy/model_patcher.py wraps PyTorch models to apply LoRA, hooks, and weight adapters non-destructively at inference time
- Versioned API Stubs: comfy_api/v0_0_1/, v0_0_2/, latest/ provide stable, versioned Python interfaces for custom node authors with generated sync stubs
- Alembic Schema Migrations: SQLite database schema for the asset system is managed via Alembic migrations with explicit upgrade/downgrade paths

## 適用シーン
Building local or server-hosted generative AI pipelines for image, video, and audio synthesis. Useful for artists needing a visual workflow editor, developers building custom AI nodes or integrating third-party APIs, and researchers experimenting with diffusion model architectures. Also serves as a backend engine embeddable in other applications via its REST/WebSocket API.

## 注意点・制約
Internal API routes (/internal/*) are explicitly unstable and subject to change. The asset management system is marked as not fully implemented. Windows AMD GPU support requires a specific driver version. Memory management behavior differs significantly between CPU, NVIDIA, and AMD backends. The API node system requires external API keys and may incur costs.


## 関連ナレッジ
- (なし)
