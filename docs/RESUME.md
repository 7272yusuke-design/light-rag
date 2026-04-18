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
- DATA-SCHEMA.md（データ構造ルール・3レイヤー+L2c管理ルール ※2026-04-18 L2c追加）
- KNOWLEDGE-INDEX.md（ナレッジ一覧・移行ログ）
- KNOWLEDGE-DECISIONS.md（投入判断ログ ※2026-04-18 新設）
- SYSTEM-SPEC.md（システム仕様）

現在のフェーズ: Phase 1-11完了 + ルール整備完了（2026-04-18）
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

## ナレッジ4レイヤー構成（85件 + L2c新設）

### L3（実装）: 47件
フレームワーク19, ツール12, SKILL 9, スキルパック7

### L2（検証済みパターン）: 16件
スキル設計パターン集, SNSライティングルール, ai-seo, スキル最適化手法,
mcollina/skills, Building LLM, anthropic-cookbook, superpowers, GSD,
マルチエージェント設計パターン, RAGパイプライン構築, RAGアプリケーション設計,
AI文書生成パイプライン, Agent Teams並列開発, マルチテナントSaaS設計,
Durable Execution+HITL承認フロー, n8n→Webアプリ移行判断

### L2c（候補パターン）: 0件（本体投入予定）
※2026-04-18 レイヤー新設。DECISIONSに記録済みの候補:
- Agent Routing パターン（openclaude由来）
- Tool-loop + MCP統合 パターン（openclaude由来）
- OpenAI互換API抽象化 パターン（openclaude由来）
- Text-first + On-demand visuals パターン（video-use由来）
- LLMトークン削減プロキシ パターン（rtk由来）

### L1（コンテキスト）: 14件
LightRAGインフラ運用ログ, ナレッジ管理運用知見, 開発環境ワークフロー(v2),
Neo/OpenClaw, jizokuka-ai, SNS Autopilot, Secretary Agent Platform,
note.com収益化パイプライン, きよびん, note.com自動投稿技術要件,
Masterclass, git-art, GitHub Actions記事生成, 開発環境ワークフロー(旧・残骸)

### 旧形式/残骸: 8件
codex-plugin-cc, agency-agents, obsidian-skills, cli(GWS) + グラフ残骸4件

## ナレッジ投入ルール（2026-04-18 更新）

### 基本ルール
- 汎用スキル・パターンのみ投入。顧客固有情報はClaude Code側で完結
- ナレッジ本体の投入経路はClaude.ai（LightRAGプロジェクト）からのupload_document
- 管理ドキュメント（INDEX/DECISIONS/RESUME/SCHEMA）はVPS上で直接編集
- リポジトリ/ツールは最初からL3品質で投入（段階的アップグレード禁止）
- 削除はDELETE API禁止。psql直接操作 + pg_dump必須
- 案件完了後、汎用化できるパターンをL2として投入
- L1更新は各プロジェクトで更新プロンプト実行→ここで統合投入

### L2c（候補パターン）ルール ※2026-04-18 追加
- ブレスト/OSS読解ベースでも投入可（status: unverified）
- ファイル名: `*-l2c_lightrag.txt`
- 自環境で実装・動作確認後、L2に昇格（ファイル名リネーム）
- 詳細はDATA-SCHEMA.md参照

### 判断ログ（必須）※2026-04-18 追加
- 新規リソース評価時は必ずKNOWLEDGE-DECISIONS.mdに記録
- 4カテゴリ: L3投入 / L2c投入 / 保留 / 見送り
- 再検討条件は具体ビジネスイベント形式で書く
  - ❌ 「案件時」「実装時」（漠然）
  - ✅ 「OpenClaw本格化時」「電子署名案件受注時」
- 再評価時は必ずDECISIONSを参照して重複判断を避ける

## 残タスク（優先順）
1. [ ] OpenRouter APIキーローテーション（最優先・セキュリティ）
2. [x] L2c本体投入（5パターン）完了（2026-04-18）
3. [ ] DECISIONS.mdのURL補完: rtk, MiniCode, JeecgBoot, Agent Lightning
4. [ ] 未分類4件のL3/L2化検討（codex-plugin-cc, agency-agents, obsidian-skills, cli GWS）
5. [ ] 旧版グラフデータクリーンアップ（低優先）
6. [ ] L2さらなる拡充（現16件、目標20件）

## 完了タスク（2026-04-18）
- [x] DATA-SCHEMA.md v2更新（L2cレイヤー、4判断カテゴリ、投入フロー明文化）
- [x] KNOWLEDGE-DECISIONS.md新設（7件の既存判断を永続化）
- [x] RESUME.md更新（本ファイル）

## Claude.aiプロジェクト スキル
- combination-architect: ナレッジ組み合わせ→企画提案・設計・L2/L3投入
- knowledge-navigator: ナレッジ検索→実装提案・技術選定・問題解決
- skill-verifier: Claudeception方式でナレッジ/スキル品質検証
