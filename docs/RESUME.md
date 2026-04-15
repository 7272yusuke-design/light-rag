# 再開手順書

## このドキュメントについて

LightRAGナレッジパイプラインの作業を再開する際の手順。Claude.aiプロジェクトに渡す。

---

## 即座に伝えること

LightRAGナレッジパイプラインの続きをやります。

VPS: 76.13.187.66
作業ディレクトリ: /docker/lightrag/
Git: https://github.com/7272yusuke-design/light-rag

計画書:
- docs/GSD-PLAN.md（全体計画とフェーズ）
- docs/ARCHITECTURE.md（システム設計）
- docs/DATA-SCHEMA.md（データ構造ルール）
- docs/KNOWLEDGE-INDEX.md（ナレッジ一覧）
- knowledge-layer-rules.md（3レイヤー管理ルール）※プロジェクトファイル
- migration-plan.md（移行計画）※プロジェクトファイル

現在のフェーズ: Phase 1-10完了
ナレッジベース: 65件（L3:45, L2:9, L1:7, 旧形式:6）

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
    |   +-- lightrag-postgres (pgvector:pg16, port 5433)
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

## ナレッジ3レイヤー構成（65件）

### L3（実装）: 45件
フレームワーク19: Next.js, Stripe SDK, Resend, inngest, tweepy, instagrapi, ccxt, freqtrade, langgraph, crewai, mastra, Vercel AI SDK, motion, LightRAG, n8n, ComfyUI x2, supabase, NeMo-Agent-Toolkit
ツール12: MCP Servers, graphify, playwright-cli, firecrawl, shadcn-ui, awesome-design-md, notebooklm-py, gh-cli, stripe-cli, vercel, n8n-as-code, servers(旧版)
SKILL 9: docx, pdf, pdf-reading, pptx, xlsx, frontend-design, file-reading, product-self-knowledge, skill-creator
スキルパック8: deep-research, content-cascade, yt-pipeline, hooks, site-teardown, dream, page-cro, ai-seo

### L2（パターン）: 9件
スキル設計パターン集, SNSライティングルール, スキル最適化手法, mcollina/skills, Building LLM, anthropic-cookbook

### L1（コンテキスト）: 7件
note.com収益化パイプライン, きよびん, note.com自動投稿技術要件, Masterclass, git-art, GitHub Actions記事生成, OpenClaw

### 旧形式: 6件
browser-use, codex-plugin-cc, agency-agents, obsidian-skills, awesome-compose, cli(GWS)

---

## ナレッジ操作ルール

### 投入
- リポジトリ/ツールは最初からL3品質で投入
- MCP upload_document（overwriteは不安定、新ファイル名推奨）
- ファイル名: {name}-l1_lightrag.txt / -l2_ / -l3_

### 削除
- DELETE API禁止（全消しバグ）
- 手順: pg_dump -> SELECT確認 -> DELETE（ID指定）

    docker exec lightrag-postgres pg_dump -U lightrag lightrag > /tmp/lightrag_backup_$(date +%Y%m%d_%H%M).sql
    docker exec lightrag-postgres psql -U lightrag lightrag -c "SELECT id, file_path FROM public.lightrag_doc_status WHERE file_path LIKE '%target%';"
    docker exec lightrag-postgres psql -U lightrag lightrag -c "DELETE FROM public.lightrag_doc_status WHERE id IN ('doc-xxx');"

### 検索

    cd /docker/lightrag && ./scripts/search_knowledge.sh "検索クエリ"

---

## 残タスク（優先順）

1. [ ] OpenRouter APIキーローテーション（最優先・セキュリティ）
2. [ ] 旧形式6Ի�のL3化検討（browser-use等）
3. [ ] L2パターン拡充（現9件→目標15-20件）
4. [ ] 旧版グラフデータクリーンアップ（低優先）
