# アーキテクチャ設計: LightRAG ナレッジパイプライン

## システム全体図

情報ソース: GitHub OSS / Claude SKILL / 技術ドキュメント
  ↓
Ingestion Pipeline:
  1. Repomix（コードテキスト化・圧縮）
  2. OpenRouter LLM（構造化要約・自動分類・タグ付与）
  3. 二重出力
     → LightRAG API（エンティティ抽出用テキスト）
     → Obsidian MD（人間が読む学習ノート）
  ↓                          ↓
LightRAG (知識グラフDB)    Obsidian Vault (obsidian-export/)
  - PostgreSQL               ├── framework/
  - pgvector                 ├── skills/
  - NetworkX                 ├── agent/
  - Port 9621                └── tool/
  ↓
ナレッジ活用（Claude.aiプロジェクト）:
  1. 開発者の指示を受け取る
  2. search_knowledge.sh で外部知識を検索
  3. (任意) DeepWiki MCPでリポジトリ詳細を補完
  4. 現在のプロジェクト構成を読み取る
  5. 外部知識 × プロジェクト実態 → 適応案を生成
  6. ファイル操作・コード生成を実行

## 採用ツールと役割

| ツール | 役割 | 利用場面 | インストール |
|---|---|---|---|
| Repomix | リポジトリ → AIフレンドリーテキスト | VPSパイプライン | npm install -g repomix |
| DeepWiki MCP | リポジトリの設計構造Wiki | Claude Code経由 | claude mcp add deepwiki ... |
| OpenRouter | LLM要約・自動分類 | VPSパイプライン | 既存（.env設定済み） |
| LightRAG | 知識グラフDB・検索 | VPSパイプライン + API | 既存（Docker） |
| graphify | コード構造解析（Claude Code SKILL） | Claude Code内で /graphify | pip install graphifyy |
| Obsidian | 人間向け学習ノート | ローカル（後に同期） | VPS上にMD生成のみ |

## コンポーネント詳細

### 1. Ingestion Pipeline

場所: /docker/lightrag/scripts/

| スクリプト | 役割 |
|---|---|
| ingest_github.sh | GitHub URL → Repomix → 要約 → 投入（メインエントリ） |
| summarize_repo.py | Repomix出力 → OpenRouter LLM → 構造化要約生成（--graph-reportオプションでgraphify出力を追加コンテキストとして利用可能） |
| submit_to_lightrag.py | LightRAG APIへの投入ラッパー |
| export_obsidian.py | Obsidian用MDファイル生成 |
| search_knowledge.sh | LightRAG検索ラッパー（ターミナルから利用） |

### データ管理スクリプト

| スクリプト | 役割 |
|---|---|
| normalize_tags.py | タグ正規化（大文字小文字統一、エイリアス解決）|
| check_duplicates.py | 重複・矛盾検知（タグ頻度、カテゴリ分布、ソースURL重複）|
| check_freshness.py | 鮮度チェック（180日超過で警告、--fixでstatus更新）|

### 処理フロー（GitHub）

ingest_github.sh <URL>
  ├── repomix --remote <URL> --compress --style markdown
  │          --ignore "tests,cassettes,fixtures,node_modules,dist,build"
  │          -o /tmp/repomix_output.md
  ├── summarize_repo.py /tmp/repomix_output.md
  │     ├── Repomixテキストを80000文字に切り詰め
  │     ├── (任意) graphify GRAPH_REPORT.mdを追加コンテキストとして付加
  │     ├── OpenRouter LLMに送信
  │     │     ├── 構造化要約を生成（DATA-SCHEMAテンプレート準拠）
  │     │     ├── カテゴリを自動判定（固定6+4カテゴリから選択）
  │     │     └── タグを自由生成（正規化ルール適用）
  │     └── JSON出力（要約テキスト + メタデータ）
  ├── submit_to_lightrag.py（要約テキストをLightRAG APIに投入）
  │     ├── トークン取得（login API）
  │     └── ドキュメントアップロード（documents/upload API）
  └── export_obsidian.py（Obsidian用MD生成）
        ├── YAML frontmatter付与
        ├── Obsidianリンク記法追加
        └── obsidian-export/<category>/<repo-name>.md に出力

### graphifyとの連携

graphifyはClaude Code SKILL（/graphify コマンド）として動作。
bashから直接呼び出しは不可。用途は以下2つ：

1. 巨大リポジトリのingest前の構造把握
   Claude Codeで /graphify /tmp/cloned-repo → GRAPH_REPORT.mdを確認
   → 重要コンポーネントを特定してからingest方針を決定

2. summarize_repo.pyへのコンテキスト補完
   GRAPH_REPORT.mdを --graph-report オプションで渡すと要約精度が向上

### 2. LightRAG API利用

トークン取得:
  POST http://localhost:9621/login (username, password) → access_token

ドキュメント投入:
  POST http://localhost:9621/documents/upload
  Header: Authorization: Bearer $TOKEN
  Body: multipart file

ドキュメント削除:
  DELETE http://localhost:9621/documents/delete_document
  Body: {"doc_ids": ["doc-xxx"]}

検索:
  POST http://localhost:9621/query
  Body: {"query":"...", "mode":"hybrid"}

ドキュメント一覧:
  GET http://localhost:9621/documents

### 3. Obsidian Vault構成

obsidian-export/
├── agent/
│   ├── openclaw.md
│   ├── ruflo.md
│   ├── agency-agents.md
│   └── ...
├── framework/
│   ├── crewai.md
│   ├── lightrag.md
│   ├── mastra.md
│   ├── comfyui.md
│   ├── n8n.md
│   └── servers.md
├── skills/
│   ├── skill-creator.md
│   ├── docx-creation.md
│   ├── pdf-processing.md
│   ├── pdf-reading.md
│   ├── pptx-creation.md
│   ├── xlsx-processing.md
│   ├── frontend-design.md
│   ├── file-reading.md
│   └── product-self-knowledge.md
├── tool/
│   ├── n8n-mcp.md
│   ├── n8n-as-code.md
│   ├── graphify.md
│   └── ...
└── website/
    └── awesome-design-md.md

## 拡張ポイント

### エージェント連携（Phase 5完了）
- LightRAG APIはREST。OpenClawや他のエージェントから直接叩ける
- 認証はJWTトークン。エージェント用のサービスアカウントを別途作成可能

### graphify連携（将来）
- graphify GRAPH_REPORT.md → LightRAG投入スクリプトの整備
- プロジェクト内部構造を外部知識DBにも蓄積する仕組み

### 自己進化サイクル（将来）
- 開発完了時に「何を学んだか」をLLMで要約
- 要約をLightRAGにフィードバック投入
- これは手動トリガー → 半自動 → 自動 の段階で成熟させる
