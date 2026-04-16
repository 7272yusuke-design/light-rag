# 再開手順書

## このドキュメントについて
LightRAGナレッジパイプラインの作業を再開する際の手順。セッション開始時にこのファイルを確認する。

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

現在のフェーズ: Phase 1-11完了
ナレッジベース: 85件（L3:47, L2:16, L1:14, 旧形式/残骸:8）

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
    |   +-- mcp-lightrag.service
    |   +-- cloudflared-mcp.service
    |       +-- https://mcp.7272yusuke.cloud/mcp
    +-- Repomix (npm global)
    +-- graphify (pip global)

## 認証情報
- WebUI: http://76.13.187.66:9621 -> admin / LightRag@2026!
- .envはgit外。VPS上の /docker/lightrag/.env を参照
- OpenRouter APIキーは要ローテーション（チャットで公開済み）

## ナレッジ3レイヤー構成（85件）

### L3（実装）: 47件
フレームワーク19, ツール12, SKILL 9, スキルパック7

### L2（パターン）: 16件
スキル設計パターン集, SNSライティングルール, ai-seo, スキル最適化手法,
mcollina/skills, Building LLM, anthropic-cookbook, superpowers, GSD,
マルチエージェント設計パターン, RAGパイプライン構築, RAGアプリケーション設計,
AI文書生成パイプライン, Agent Teams並列開発, マルチテナントSaaS設計,
Durable Execution+HITL承認フロー, n8n→Webアプリ移行判断

### L1（コンテキスト）: 14件
LightRAGインフラ運用ログ, ナレッジ管理運用知見, 開発環境ワークフロー(v2),
Neo/OpenClaw, jizokuka-ai, SNS Autopilot, Secretary Agent Platform,
note.com収益化パイプライン, きよびん, note.com自動投稿技術要件,
Masterclass, git-art, GitHub Actions記事生成, 開発環境ワークフロー(旧・残骸)

### 旧形式/残骸: 8件
codex-plugin-cc, agency-agents, obsidian-skills, cli(GWS) + グラフ残骸4件

## ナレッジ投入ルール
- 汎用スキル・パターンのみ投入。顧客固有情報はClaude Code側で完結
- 投入経路はClaude.ai（LightRAGプロジェクト）からのupload_documentに限定
- リポジトリ/ツールは最初からL3品質で投入（段階的アップグレード禁止）
- 削除はDELETE API禁止。psql直接操作 + pg_dump必須
- 案件完了後、汎用化できるパターンをL2として投入
- L1更新は各プロジェクトで更新プロンプト実行→ここで統合投入

## 残タスク（優先順）
1. [ ] OpenRouter APIキーローテーション（最優先・セキュリティ）
2. [ ] 未分類4件のL3/L2化検討（codex-plugin-cc, agency-agents, obsidian-skills, cli GWS）
3. [ ] 旧版グラフデータクリーンアップ（低優先）
4. [ ] L2さらなる拡充（現16件、目標20件）

## Claude.aiプロジェクト スキル
- combination-architect: ナレッジ組み合わせ→企画提案・設計・L2/L3投入
- knowledge-navigator: ナレッジ検索→実装提案・技術選定・問題解決
- skill-verifier: Claudeception方式でナレッジ/スキル品質検証
