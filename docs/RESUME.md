# 再開手順書

## このドキュメントについて
LightRAGナレッジパイプラインの作業を再開する際の手順。セッション開始時にこのファイルを確認する。

## 即座に伝えること

LightRAGナレッジパイプラインの続きをやります。

- VPS: 76.13.187.66
- 作業ディレクトリ: /docker/lightrag/
- Git: https://github.com/7272yusuke-design/light-rag

計画書（全てVPS上 /docker/lightrag/docs/）:
- RESUME.md（本ファイル）
- GSD-PLAN.md（全体計画とフェーズ）
- ARCHITECTURE.md（システム設計）
- DATA-SCHEMA.md（データ構造ルール・L1 v3再定義/L2c/4判断カテゴリ含む）
- KNOWLEDGE-INDEX.md（ナレッジ一覧・移行ログ）
- KNOWLEDGE-DECISIONS.md（投入判断ログ）
- SYSTEM-SPEC.md（システム仕様）

## 現在のフェーズ
**Phase 12 完了（2026-05-01）**: 整理・再棚卸しセッション

## ナレッジベース現状（2026-05-01）
- **総数: 157件**（全processed、エラー0件）
- **doc_full = doc_status = 157**（整合性確保、ゴースト21件除去済み）

### レイヤー内訳
| レイヤー | 件数 | 割合 |
|---------|------|------|
| L3（実装） | 103 | 65.6% |
| L2（検証済みパターン） | 18 | 11.5% |
| L2c（候補パターン） | 19 | 12.1% |
| L1-Infra | 1 | 0.6% |
| L1-Ops | 2 | 1.3% |
| L1-old | 1 | 0.6% |
| other（旧形式） | 13 | 8.3% |

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
- **OpenRouter APIキーは要ローテーション**（チャットで公開済み・最優先タスク）

## ナレッジ4レイヤー構成（2026-04-18 v3 / 2026-05-01時点件数）

### L3（実装）: 103件
気になる技術スタックの部品在庫。リポジトリ/ツール/SKILLは最初からL3で投入。
詳細はKNOWLEDGE-INDEX.md参照。

### L2（検証済みパターン）: 18件
組み合わせ方を知る。検証済みのみ。category: pattern/combination のみ許可。
詳細はKNOWLEDGE-INDEX.md参照。

### L2c（候補パターン）: 19件
ブレスト/OSS読解ベースで投入可（status: unverified）。
ファイル名: *-l2c_lightrag.txt。検証後にL2へ昇格。

### L1（横断運用メタ知識のみ）: L1-Infra 1件 + L1-Ops 2件 = 計3件
v3再設計によりプロジェクト固有情報は全除外。
- dev-environment-workflow-v2-l1-infra（L1-Infra）
- lightrag-infra-ops-l1-ops（L1-Ops）
- lightrag-knowledge-ops-l1-ops（L1-Ops）

### その他（旧形式・リネーム対象）: 14件
- L1-old: 1件（awesome-agent-skills-l1）
- other（サフィックスなし）: 13件
詳細・リネーム計画はKNOWLEDGE-INDEX.md参照。

## ナレッジ投入ルール（2026-04-18 v3）

### 基本ルール
- 汎用スキル・パターンのみ投入。顧客固有情報はClaude Code側で完結
- ナレッジ本体の投入経路はClaude.ai（LightRAGプロジェクト）からのupload_document
- 管理ドキュメント（INDEX/DECISIONS/RESUME/SCHEMA）はVPS上で直接編集
- リポジトリ/ツールは最初からL3品質で投入（段階的アップグレード禁止）
- 削除はDELETE API禁止。psql直接操作 + pg_dump必須
- 案件完了後、汎用化できるパターンをL2として投入

### L1 v3ルール
- L1はL2/L3を使うための「横断運用のメタ知識」と「環境前提」のみ
- プロジェクト固有情報はLightRAGに入れない（Claude.aiプロジェクト/Notion側で管理）
- サブタイプ: L1-Infra（開発環境前提）、L1-Ops（LightRAG運用メタ知識）
- ファイル名: *-l1-infra_lightrag.txt / *-l1-ops_lightrag.txt

### L2c（候補パターン）ルール
- ブレスト/OSS読解ベースでも投入可（status: unverified）
- ファイル名: *-l2c_lightrag.txt
- 自環境で実装・動作確認後、L2に昇格（ファイル名リネーム）

### L2品質ゲート
- L2のカテゴリは pattern / combination のみ（context/persona/research禁止）
- L1→L2直接昇格禁止。必ず L1→L2c→検証→L2 の段階を経ること

### 判断ログ（必須）
- 新規リソース評価時は必ずKNOWLEDGE-DECISIONS.mdに記録
- 4カテゴリ: L3投入 / L2c投入 / 保留 / 見送り
- 再検討条件は具体ビジネスイベント形式で書く
- 再評価時は必ずDECISIONSを参照して重複判断を避ける

## 活用目的
1. **開発設計**: Claude.aiからMCP経由で参照、具体的な設計書を出力
2. **開発支援**: Hostingerターミナル開発時にナレッジ参照
3. **情報発信**: 主にL2ユースケースの記事を自動生成して発信

## 残タスク（優先順、2026-05-01更新）

1. [ ] **OpenRouter APIキーローテーション**（最優先・セキュリティ）
2. [ ] **旧形式13件のリネーム再投入**（other枠、INDEX.md記載の計画通り）
3. [ ] **L1-old 1件のリネーム**（awesome-agent-skills-l1 → l3化検討）
4. [ ] **entity_chunks/relation_chunks のゴースト要素クリーンアップ**（LightRAG公式手順調査が必要）
5. [ ] **L2c → L2 昇格候補の検証**（実装による検証実施）
6. [ ] **L2拡充**（現18件 → 目標25件）
7. [ ] **2段階クエリ戦略のスキル化**（理論はDATA-SCHEMA.md記載済、スキル化のみ未着手）

## 完了タスク履歴

### 2026-05-01: 整理・再棚卸し（Phase 12）
- [x] doc_fullゴースト21件削除（chunks 71件 + vdb_chunks 71件巻き込み）
- [x] doc_full = doc_status = 157 の整合性達成
- [x] 全157件のレイヤー別棚卸し（INDEX.md全面書き換え）
- [x] 新規L3投入2件（trellis-mindfold-l3 / voxcpm-openbmb-l3）
- [x] 見送り判断1件（docker-android budtmo）
- [x] DECISIONS.md / INDEX.md / RESUME.md 同期更新
- [x] 旧形式13件のリネーム計画明文化

### 2026-04-19: Phase 3 無サフィックス再投入
- [x] 用途別検索精度の実地検証（6テストクエリ）
- [x] エンティティ構造の解明（lightrag_full_entities と vdb_entity の役割分担）
- [x] Phase 1a 重複24件削除（skill系旧版18+プロジェクト進捗2+孤児4）
- [x] crewai 削除→L3再投入（エンティティ純度問題の検証）
- [x] バッチ1 マルチエージェント3件再投入（langgraph/mastra/n8n）
- [x] バッチ2 Web系3件再投入+llmfit削除（firecrawl/browser-use/ffmpeg）
- [x] バッチ3 SaaS/取引6件再投入+nemo-agent-toolkit削除（anthropic-cookbook/ccxt/freqtrade/n8n-as-code/supabase/vercel）

### 2026-04-18: L1 v3再設計 + L2c拡充
- [x] DATA-SCHEMA.md v2/v3更新（L2cレイヤー、4判断カテゴリ、L1再定義）
- [x] KNOWLEDGE-DECISIONS.md新設
- [x] L2c本体投入5パターン
- [x] mcp2cli L3投入 + Schema-driven Lazy CLI L2c投入
- [x] L1から汎用パターン3件をL2cへ昇格
- [x] L1削除10件 + L1維持3件をL1-Infra/L1-Opsにリネーム

## Claude.aiプロジェクト スキル
- combination-architect: ナレッジ組み合わせ→企画提案・設計・L2/L3投入
- knowledge-navigator: ナレッジ検索→実装提案・技術選定・問題解決
- skill-verifier: Claudeception方式でナレッジ/スキル品質検証

---

## 2026-05-24 フェーズ1A セッション1完了

### 達成事項
- MCPサーバーのソースコード特定: `/docker/lightrag/scripts/mcp_remote.py` (254行, Starlette)
- ベースライン3クエリ取得（measurement/baseline/）
  - query1 (OpenSpec, naive): 817 tokens / 2270 bytes / 0.46s
  - query2 (MCP token reduction, hybrid): 1338 tokens / 4415 bytes / 5.25s
  - query3 (エージェント framework, hybrid): 1289 tokens / 4478 bytes / 3.32s
- tools/list ベースライン: 272 tokens / 1223 bytes
- PostgreSQL backup: backups/baseline_20260524_002542.sql (282MB)
- feature/compression-middleware ブランチ作成・push完了
- list_knowledge表示バグ修正をmainにコミット (bf52e40) → メモリ記載の調査タスク事実上クローズ

### コミット
- main: bf52e40 (fix: list_knowledge direct SQL query)
- feature/compression-middleware: b54d116 (chore: baseline metrics)

### 観察と気づき
- hybridモードのレスポンスは [entities] セクション形式、naiveは [chunks] 形式
- 既存tool descriptionは既に簡潔 → セッション2の削減余地は限定的、本丸はセッション4/5
- hybridモードの返却は10件上限が効いている可能性あり (query2/3 がほぼ同サイズ)

### 次回開始時 (セッション2)
- 圧縮ミドルウェアのコード変更開始
- 簡潔化対象は tools/list (272 tokens) のみ → 削減余地小
- セッション3以降のミドルウェア基盤構築を視野に進める

### 未処理タスク（フェーズ1A外で対処予定）
- main未コミットの整理系ファイル（config/, docs/KNOWLEDGE-*, untracked多数）
- これらはナレッジ整理セッションで別途処理
