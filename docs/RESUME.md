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
- DATA-SCHEMA.md（データ構造ルール・L1 v3再定義/L2c/4判断カテゴリ含む）
- KNOWLEDGE-INDEX.md（ナレッジ一覧・移行ログ）
- KNOWLEDGE-DECISIONS.md（投入判断ログ）
- SYSTEM-SPEC.md（システム仕様）

現在のフェーズ: Phase 1-11完了 + L1 v3再設計完了（2026-04-18）
ナレッジベース: 104件（L3:48, L2:16, L2c:9, L1:3, その他/旧形式:28）

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

## ナレッジ4レイヤー構成（2026-04-18 v3）

### L3（実装）: 48件
気になる技術スタックの部品在庫。2026-04-18にmcp2cliを追加（48件）。

### L2（検証済みパターン）: 16件
スキル設計パターン集, SNSライティングルール, ai-seo, スキル最適化手法,
mcollina/skills, Building LLM, anthropic-cookbook, superpowers, GSD,
マルチエージェント設計パターン, RAGパイプライン構築, RAGアプリケーション設計,
AI文書生成パイプライン, Agent Teams並列開発, マルチテナントSaaS設計,
Durable Execution+HITL承認フロー, n8n→Webアプリ移行判断

### L2c（候補パターン）: 9件
1. Agent Routing（openclaude由来）
2. Tool-loop+MCP統合（openclaude由来）
3. OpenAI互換API抽象化（openclaude由来）
4. Text-first+On-demand visuals（video-use/browser-use由来）
5. LLMトークン削減プロキシ（rtk由来）
6. Schema-driven Lazy CLI（mcp2cli由来）
7. TrinityCouncil 3エージェント議論型合意形成（Neo/OpenClaw由来、L1から昇格）
8. n8n Cron駆動 自己改善ワークフローエージェント（SNS Autopilot由来、L1から昇格）
9. CLAUDE.md駆動のコンテンツ自動生成（git-art/GitHub Actions由来、L1から昇格）

### L1（L1-Infra / L1-Ops）: 3件
L1 v3再設計によりプロジェクト固有情報は全除外。横断運用のメタ知識のみ維持。
- dev-environment-workflow-v2-l1-infra（L1-Infra）
- lightrag-infra-ops-l1-ops（L1-Ops）
- lightrag-knowledge-ops-l1-ops（L1-Ops）

### その他/旧形式: 28件（次セッションで再棚卸し）

## ナレッジ投入ルール（2026-04-18 v3）

### 基本ルール
- 汎用スキル・パターンのみ投入。顧客固有情報はClaude Code側で完結
- ナレッジ本体の投入経路はClaude.ai（LightRAGプロジェクト）からのupload_document
- 管理ドキュメント（INDEX/DECISIONS/RESUME/SCHEMA）はVPS上で直接編集
- リポジトリ/ツールは最初からL3品質で投入（段階的アップグレード禁止）
- 削除はDELETE API禁止。psql直接操作 + pg_dump必須
- 案件完了後、汎用化できるパターンをL2として投入

### L1 v3ルール（2026-04-18 再定義）
- L1はL2/L3を使うための「横断運用のメタ知識」と「環境前提」のみ
- プロジェクト固有情報はLightRAGに入れない（Claude.aiプロジェクト/Notion側で管理）
- サブタイプ: L1-Infra（開発環境前提）、L1-Ops（LightRAG運用メタ知識）
- ファイル名: *-l1-infra_lightrag.txt / *-l1-ops_lightrag.txt

### L2c（候補パターン）ルール
- ブレスト/OSS読解ベースでも投入可（status: unverified）
- ファイル名: *-l2c_lightrag.txt
- 自環境で実装・動作確認後、L2に昇格（ファイル名リネーム）
- L1削除前の汎用化抽出先としても使う

### L2品質ゲート強化（v3追加）
- L2のカテゴリは pattern / combination のみ（context/persona/research禁止）
- L1→L2直接昇格禁止。必ず L1→L2c→検証→L2 の段階を経ること

### 判断ログ（必須）
- 新規リソース評価時は必ずKNOWLEDGE-DECISIONS.mdに記録
- 4カテゴリ: L3投入 / L2c投入 / 保留 / 見送り
- 再検討条件は具体ビジネスイベント形式で書く
- 再評価時は必ずDECISIONSを参照して重複判断を避ける

## 活用目的（2026-04-18 明文化）
①開発設計: Claude.aiからMCP経由で参照、具体的な設計書を出力
②開発支援: Hostingerターミナル開発時にナレッジ参照
③情報発信: 主にL2ユースケースの記事を自動生成して発信

## 残タスク（優先順）
1. [ ] OpenRouter APIキーローテーション（最優先・セキュリティ）
2. [ ] KNOWLEDGE-INDEX.md の詳細一覧を再棚卸し（v3反映）
3. [ ] DECISIONS.mdのURL補完: rtk=https://github.com/rtk-ai/rtk（判明済）、MiniCode/JeecgBoot/Agent LightningのURL
4. [ ] 未分類4件のL3/L2化検討（codex-plugin-cc, agency-agents, obsidian-skills, cli GWS）
5. [ ] entity/relation残骸のクリーンアップ（L1削除で残った幽霊エンティティ）
6. [ ] L2c昇格条件を満たしたものからL2へ昇格（各パターンの検証実施）
7. [ ] L2さらなる拡充（現16件、目標20件）

## 完了タスク（2026-04-18）
- [x] DATA-SCHEMA.md v2更新（L2cレイヤー、4判断カテゴリ、投入フロー明文化）
- [x] KNOWLEDGE-DECISIONS.md新設（初期7件の判断を永続化）
- [x] L2c本体投入 5パターン（Agent Routing/Tool-loop+MCP/OpenAI互換抽象化/Text-first+On-demand visuals/LLMトークン削減プロキシ）
- [x] mcp2cli L3投入 + Schema-driven Lazy CLI L2c投入
- [x] smolvm 保留判断 + DECISIONS記録
- [x] DATA-SCHEMA.md v3追記（L1再定義・L1-Infra/L1-Ops・L2品質ゲート強化）
- [x] L1から汎用パターン3件をL2cへ昇格（TrinityCouncil/n8n自己改善/CLAUDE.md駆動コンテンツ）
- [x] L1削除 10件（psql・pg_dump保護・計531レコード削除）
- [x] L1維持3件をL1-Infra/L1-Opsにリネーム（計227レコードUPDATE）

## Claude.aiプロジェクト スキル
- combination-architect: ナレッジ組み合わせ→企画提案・設計・L2/L3投入
- knowledge-navigator: ナレッジ検索→実装提案・技術選定・問題解決
- skill-verifier: Claudeception方式でナレッジ/スキル品質検証
