# ナレッジインデックス（LightRAG 蓄積済み 全42件）

> このファイルはLightRAGに蓄積された全ナレッジの索引です。
> 「〇〇に使えるナレッジは？」「〇〇の実装パターンを探して」等の質問に対し、
> このインデックスを参照して関連ナレッジを特定してください。
> 詳細が必要な場合はVPSで検索コマンドを実行します。

## 使い方
1. ユーザーの質問からキーワード・カテゴリ・タグを照合
2. 関連するナレッジを提示（名前・概要・なぜ関連するか）
3. 詳細が必要な場合: `./scripts/search_knowledge.sh "クエリ"` をVPSで実行指示

## フレームワーク・ライブラリ (14件)

### crewai
- **GitHub:** crewaiinc/crewai
- **タグ:** python, multi-agent, LLM, RAG, MCP, crewai, orchestration, autonomous-agents
- **概要:** CrewAIはLLMを活用した自律型マルチエージェントシステムを構...

### LightRAG
- **GitHub:** HKUDS/LightRAG
- **タグ:** python, typescript, RAG, knowledge-graph, LLM, FastAPI, React, graph-database, vector-database
- **概要:** LightRAG is a prod...

### n8n
- **GitHub:** n8n-io/n8n
- **タグ:** TypeScript, n8n, LangChain, MCP, LangGraph, automation, multi-agent, low-code
- **概要:** n8nはノードベースのワークフロー自動化プラットフォームであり、AIエ...

### ComfyUI
- **GitHub:** comfyanonymous/ComfyUI
- **タグ:** python, stable-diffusion, image-generation, node-based, diffusion-models, pytorch, aiohttp, SQLAlchemy
- **概要:** ...

### servers
- **GitHub:** modelcontextprotocol/servers
- **タグ:** TypeScript, Python, MCP, model-context-protocol, LLM-integration, SSE, stdio-transport, multi-transport
- **概要:** 

### mastra
- **GitHub:** mastra-ai/mastra
- **タグ:** TypeScript, LLM, multi-agent, RAG, MCP, AI-SDK, monorepo, observability
- **概要:** Mastraは、TypeScriptで構築されたAIエージェント・ワークフロ...

### langgraph
- **GitHub:** langchain-ai/langgraph
- **タグ:** python, langgraph, pregel, state-machine, multi-agent, checkpointing, LLM, graph-execution
- **概要:** LangGraph ...

### ai
- **GitHub:** vercel/ai
- **タグ:** TypeScript, AI-SDK, LLM, streaming, multi-provider, tool-calling, Next.js, MCP
- **概要:** Vercel AI SDKは、TypeScript/JavaScript向けのAIアプリ...

### ccxt
- **GitHub:** ccxt/ccxt
- **タグ:** typescript, python, csharp, golang, cryptocurrency, exchange-api, websocket, trading
- **概要:** CCXTは100以上の暗号通貨取引所に対応した統一APIライブラリで、...

### CLI-Anything
- **GitHub:** HKUDS/CLI-Anything
- **タグ:** python, typescript, cli, ai-agent, gui-automation, repl, click, plugin-architecture
- **概要:** CLI-Anything is a fram...

### freqtrade
- **GitHub:** freqtrade/freqtrade
- **タグ:** python, algorithmic-trading, backtesting, hyperopt, freqai, ccxt, machine-learning, cryptocurrency
- **概要:** Freqtr...

### motion
- **GitHub:** framer/motion
- **タグ:** TypeScript, React, animation, WAAPI, layout-animation, motion, framer-motion, spring-physics
- **概要:** Motion（旧Framer Motion）は...

### NeMo-Agent-Toolkit
- **GitHub:** NVIDIA/NeMo-Agent-Toolkit
- **タグ:** python, LLM, multi-agent, LangChain, MCP, RAG, observability, plugin-architecture
- **概要:** NVIDIA ...

### comfyui-api-wrapper
- **GitHub:** ai-dock/comfyui-api-wrapper
- **タグ:** python, fastapi, comfyui, stable-diffusion, image-generation, websocket, async-queue, s3-upload
- **概要:** 

## エージェント・自動化 (5件)

### obsidian-skills
- **GitHub:** kepano/obsidian-skills
- **タグ:** obsidian, markdown, PKM, claude-code, agent-skills, YAML, json-canvas, knowledge-management
- **概要:** Obsidian...

### openclaw
- **GitHub:** openclaw/openclaw
- **タグ:** Swift, Kotlin, TypeScript, AI-assistant, multi-platform, voice-interface, plugin-system, LLM-gateway
- **概要:** OpenCl...

### browser-use
- **GitHub:** browser-use/browser-use
- **タグ:** python, browser-automation, LLM, playwright, CDP, multi-LLM, web-scraping, asyncio
- **概要:** browser-use is a Py...

### ruflo
- **GitHub:** ruvnet/ruflo
- **タグ:** TypeScript, JavaScript, Svelte, multi-agent, swarm, MCP, SPARC, hive-mind
- **概要:** Claude-Flowは、Claude AIを活用したマルチエージェントオーケスト...

### agency-agents
- **GitHub:** msitarzewski/agency-agents
- **タグ:** markdown, prompt-engineering, multi-agent, LLM, role-playing, system-prompt, AI-personas, agent-design
- **概要:** 

## ツール・ユーティリティ (17件)

### docx-creation
- **ソース:** Claude Code 公式 SKILL
- **対象技術:** docx
- **タグ:** docx, word, document-generation, javascript, xml
- **概要:** Word文書(.docx)の作成・読み取り・編集・操作スキル。docx-jsによる新規作成、XML直接編集、pandocによるテキ...

### file-reading
- **ソース:** Claude Code 公式 SKILL
- **対象技術:** 全ファイル形式
- **タグ:** file-handling, python, cli, data-extraction
- **概要:** ファイル拡張子に基づき最適な読み取り方法をディスパッチするルータースキル。PDF,DOCX,XLSX,CSV,JSON,画像,アーカイブ対応。  #...

### frontend-design
- **ソース:** Claude Code 公式 SKILL
- **対象技術:** HTML/CSS/JS, React, Vue
- **タグ:** frontend, react, css, ui-design, animation
- **概要:** 独自性ある本番品質フロントエンドUI作成スキル。ジェネリックAIデザイン回避、大胆な美的方向性重視...

### pdf-processing
- **ソース:** Claude Code 公式 SKILL
- **対象技術:** pdf
- **タグ:** pdf, python, document-processing, text-extraction
- **概要:** PDFの作成・結合・分割・回転・ウォーターマーク・フォーム記入・暗号化・OCR等の処理スキル。

### pdf-reading
- **ソース:** Claude Code 公式 SKILL
- **対象技術:** pdf
- **タグ:** pdf, python, ocr, text-extraction, data-extraction
- **概要:** PDF読み取り・検査・コンテンツ抽出特化スキル。コンテンツインベントリ、ラスタライズ、埋め込み抽出、タイプ別読み取り戦略。

### pptx-creation
- **ソース:** Claude Code 公式 SKILL
- **対象技術:** pptx
- **タグ:** pptx, powerpoint, presentation, javascript, design
- **概要:** PowerPointの作成・読み取り・編集スキル。テンプレート編集とpptxgenjs新規作成の2方式。デザインガイドライン...

### product-self-knowledge
- **ソース:** Claude Code 公式 SKILL
- **対象技術:** Anthropic製品
- **タグ:** anthropic, claude, api, documentation, llm
- **概要:** Anthropic製品(Claude Code, API, claude.ai)の正確な情報提供スキル。製品別ド...

### skill-creator
- **ソース:** Claude Code 公式 SKILL (examples)
- **対象技術:** Claude Code SKILL
- **タグ:** skill-creation, evaluation, claude-code, meta-skill, testing
- **概要:** 新しいSKILLの作成・改善・評価を行う...

### xlsx-processing
- **ソース:** Claude Code 公式 SKILL
- **対象技術:** xlsx
- **タグ:** excel, spreadsheet, python, financial-modeling, data-analysis
- **概要:** Excelスプレッドシートの作成・編集・分析スキル。pandas/openpyxl操作、財務モデル色...

### notebooklm-py
- **GitHub:** teng-lin/notebooklm-py
- **タグ:** python, notebooklm, cli, google-api, async, playwright, rpc, automation
- **概要:** notebooklm-py is a Python CLI ...

### n8n-mcp
- **GitHub:** czlonkowski/n8n-mcp
- **タグ:** TypeScript, MCP, n8n, SQLite, workflow-automation, AI-integration, node-validation, Docker
- **概要:** n8n-MCP is a Model C...

### n8n-as-code
- **GitHub:** EtienneLescot/n8n-as-code
- **タグ:** typescript, n8n, gitops, monorepo, vscode-extension, cli, workflow-automation, mcp
- **概要:** n8n-as-code (n8nac...

### cli
- **GitHub:** googleworkspace/cli
- **タグ:** rust, google-workspace, cli, google-api, discovery-api, oauth2, automation, ai-agent
- **概要:** GWS is a Rust-based CLI tool t...

### playwright-cli
- **GitHub:** microsoft/playwright-cli
- **タグ:** javascript, typescript, playwright, browser-automation, cli, test-generation, web-scraping, claude-code
- **概要:** 

### ComfyUI-to-Python-Extension
- **GitHub:** pydn/ComfyUI-to-Python-Extension
- **タグ:** python, comfyui, code-generation, stable-diffusion, ast-generation, cli, custom-nodes, workflow-expor...
- **概要:** 

### comfy_api_simplified
- **GitHub:** deimos-deimos/comfy_api_simplified
- **タグ:** python, comfyui, mcp, websocket, image-generation, stable-diffusion, api-wrapper
- **概要:** Co...

### graphify
- **GitHub:** safishamsi/graphify
- **タグ:** python, knowledge-graph, AST-extraction, tree-sitter, networkx, LLM-integration, community-detection, code-analysis
- **概要:** 

## Webサイト・UI (2件)

### supabase
- **GitHub:** supabase/supabase
- **タグ:** TypeScript, Next.js, MDX, Supabase, design-system, documentation, Tailwind, React
- **概要:** Supabaseの公式ドキュメントサイトおよびデザ...

### ui
- **GitHub:** shadcn-ui/ui
- **タグ:** TypeScript, React, Next.js, Tailwind-CSS, shadcn-ui, component-library, design-system, RTL-support
- **概要:** shadcn/uiの公式ドキュメントサイト...

## インフラ・DevOps (1件)

### awesome-compose
- **GitHub:** docker/awesome-compose
- **タグ:** docker-compose, multi-language, containerization, nginx, postgresql, react, golang, python
- **概要:** Docker Comp...

## ワークフロー・パターン (1件)

### anthropic-cookbook
- **GitHub:** anthropics/anthropic-cookbook
- **タグ:** python, jupyter, claude-api, RAG, multi-agent, LLM-evals, anthropic-sdk, MCP
- **概要:** Anthropic ...

## パターン集・クックブック (1件)

### awesome-design-md
- **GitHub:** VoltAgent/awesome-design-md
- **タグ:** markdown, design-system, design-tokens, UI-components, AI-agent, LLM-context, style-guide
- **概要:** 著名...

## その他 (1件)

### Building LLM-Powered Applications with Claude
- **タグ:** 
- **概要:** 

## 逆引き: やりたいこと → ナレッジ

| やりたいこと | 関連ナレッジ |
|---|---|
| マルチエージェント構築 | CrewAI, LangGraph, Mastra, NeMo-Agent-Toolkit, ruflo |
| 仮想通貨取引bot | freqtrade, ccxt, OpenClaw |
| ブラウザ自動操作 | browser-use, playwright-cli |
| n8nワークフロー | n8n, n8n-mcp, n8n-as-code |
| フロントエンドUI | shadcn-ui, framer-motion, Vercel AI SDK, frontend-design SKILL |
| 画像生成パイプライン | ComfyUI, comfyui-api-wrapper, comfy_api_simplified |
| MCP開発 | MCP servers, n8n-mcp, mcp_lightrag |
| Claude Code SKILL作成 | skill-creator, 各SKILL（docx,pdf,xlsx,pptx,frontend-design等） |
| Docker構成 | awesome-compose |
| 認証・DB・BaaS | Supabase |
| ナレッジ管理 | LightRAG, Obsidian Skills, graphify |
| Google Workspace連携 | gws-cli |
| LLMアプリ開発 | anthropic-cookbook, Vercel AI SDK, Mastra |
| CLI作成 | cli-anything |
