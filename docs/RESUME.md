# 再開手順書

## このドキュメントについて

LightRAGナレッジパイプラインの作業を再開する際の手順。セッション開始時にこのファイルを確認する。

---

## 即座に伝えること

LightRAGナレッジパイプラインの続きをやります。

VPS: 76.13.187.66
作業ディレクトリ: /docker/lightrag/
Git: https://github.com/7272yusuke-design/light-rag

計画書（全てVPS上 /docker/lightrag/docs/）:
- RESUME.md（本ファイル）
- GSD-PLAN.md（全体計画とフェーズ）
- ARCHITECTURE.md（システム設計）
- DATA-SCHEMA.md（データ構造ルール・3レイヤー管理ルール）
- KNOWLEDGE-INDEX.md（ナレッジ一覧・移行ログ）
- SYSTEM-SPEC.md（システム仕様）

現在のフェーズ: Phase 1-10完了、Phase 11進行中
ナレッジベース: 69件（L3:47, L2:11, L1:7, グラフ残骸:4）

---

## 環境確認コマンド

    cd /docker/lightrag && docker compose ps
    systemctl status ollama --no-pager
    curl -s http://localhost:9621/health || echo "LightRAG is down"
    docker exec lightrag-postgres pg_isready -U lightrag
    systemctl status mcp-lightrag --no-pager
    systemctl status cloudflared-mcp --no-pager

## 環境復旧（止まっていた場合）

    sudo systemctl start ollama
    cd /docker/lightrag && docker compose up -d
    sudo systemctl start mcp-lightrag
    sudo systemctl start cloudflared-mcp

---

## 現在のインフラ構成

    VPS (76.13.187.66)
    +-- Ollama (systemd, port 11434)
    |   +-- nomic-embed-text (embedding, 768dim)
    +-- Docker
    |   +-- lightrag-postgres (pgvector:pg16, port 5433, user: lightrag, db: lightrag)
    |   +-- lightrag-server (port 9621, network_mode: host)
    |       +-- LLM: OpenRouter -> anthropic/claude-sonnet-4.6
    |       +-- Embedding: Ollama -> nomic-embed-text
    |       +-- Storage: PostgreSQL + NetworkX
    +-- MCP (port 9622, systemd)
    |   +-- mcp-lightrag.service（ステートレスHTTP）
    |   +-- cloudflared-mcp.service（Named Tunnel）
    |       +-- https://mcp.7272yusuke.cloud/mcp
    +-- Repomix (npm global)
    +-- graphify (pip global, Claude Code SKILL)
    +-- OpenClaw (Docker, port 46819) ※別プロジェクト

## 認証情報

- WebUI: http://76.13.187.66:9621 -> admin / LightRag@2026!
- .envはgit外。VPS上の /docker/lightrag/.env を参照
- OpenRouter APIキーは要ローテーション（チャットで公開済み）

---

## ナレッジ3レイヤー構成（69件）

### L3（実装）: 47件
フレームワーク19: Next.js, Stripe SDK, Resend, inngest, tweepy, instagrapi, ccxt, freqtrade, langgraph, crewai, mastra, Vercel AI SDK, motion, LightRAG, n8n, ComfyUI x2, RAG-Anything, NeMo-Agent-Toolkit
ツール12: MCP Servers, graphify, playwright-cli, firecrawl, shadcn-ui, awesome-design-md, notebooklm-py, gh-cli, stripe-cli, vercel, n8n-as-code, supabase
SKILL 9: docx, pdf, pdf-reading, pptx, xlsx, frontend-design, file-reading, product-self-knowledge, skill-creator
スキルパック7: deep-research, content-cascade, yt-pipeline, hooks, site-teardown, dream, page-cro

### L2（パターン）: 11件
スキル設計パターン集, SNSライティングルール, ai-seo, スキル最適化手法, mcollina/skills, Building LLM, anthropic-cookbook, superpowers, GSD, browser-use, awesome-compose

### L1（コンテキスト）: 7件
note.com収益化パイプライン, きよびん, note.com自動投稿技術要件, Masterclass, git-art, GitHub Actions記事生成, OpenClaw

### グラフ残骸: 4件（list_knowledgeでタグ空表示、ドキュメント本体は削除済み）

---

## ナレッジ操作ルール

### 投入
- リポジトリ/ツールは最初からL3品質で投入
- MCP upload_document（overwriteは不安定、新ファイル名推奨）
- ファイル名: {name}-l1_lightrag.txt / -l2_ / -l3_

### 削除
- DELETE API禁止（全消しバグ）
- 手順: pg_dump -> SELECT確認 -> DELETE（ID指定）

    docker exec lightrag-postgres pg_dump -U lightrag lightrag > /docker/lightrag/backups/pg_backup_$(date +%Y%m%d_%H%M).sql
    docker exec lightrag-postgres psql -U lightrag lightrag -c "SELECT id, file_path FROM public.lightrag_doc_status WHERE file_path LIKE '%target%';"
    docker exec lightrag-postgres psql -U lightrag lightrag -c "DELETE FROM public.lightrag_doc_status WHERE id IN ('doc-xxx');"

### 検索

    cd /docker/lightrag && ./scripts/search_knowledge.sh "検索クエリ"

---

## 残タスク（優先順）

1. [ ] OpenRouter APIキーローテーション（最優先・セキュリティ）
2. [ ] 未分類4件のL3/L2化検討（codex-plugin-cc, agency-agents, obsidian-skills, cli GWS）
3. [ ] L2パターン拡充（現11件→目標15-20件）
4. [ ] 旧版グラフデータクリーンアップ（低優先）

---

## Claude.aiプロジェクト スキル

- combination-architect: ナレッジ組み合わせ→企画提案・設計・L2/L3投入
- knowledge-navigator: ナレッジ検索→実装提案・技術選定・問題解決
- skill-verifier: Claudeception方式でナレッジ/スキル品質検証
