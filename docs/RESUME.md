# 再開手順書

## このドキュメントについて

LightRAGナレッジパイプラインの作業を、新しいチャットセッションで再開する際の手順。Claude.aiまたはClaude Codeに渡す。

---

## 即座に伝えること

LightRAGナレッジパイプラインの続きをやります。

VPS: 76.13.187.66
作業ディレクトリ: /docker/lightrag/
Git: https://github.com/7272yusuke-design/light-rag

プロジェクトの計画書を読んでください:
- docs/GSD-PLAN.md（全体計画とフェーズ）
- docs/ARCHITECTURE.md（システム設計）
- docs/DATA-SCHEMA.md（データ構造ルール）

現在のフェーズ: Phase 1-5完了
直近の作業状態: 42ドキュメント投入済み、検索稼働中、Claude Code MCP連携済み、graphify導入済み

---

## 環境確認コマンド

  cd /docker/lightrag && docker compose ps
  systemctl status ollama --no-pager
  curl -s http://localhost:9621/health || echo "LightRAG is down"
  docker exec lightrag-postgres pg_isready -U lightrag
  repomix --version

## 環境復旧（止まっていた場合）

  sudo systemctl start ollama
  cd /docker/lightrag && docker compose up -d

---

## 現在のインフラ構成

VPS (76.13.187.66)
├── Ollama (systemd, port 11434)
│   └── nomic-embed-text (embedding, 768dim)
├── Docker
│   ├── lightrag-postgres (pgvector:pg16, port 5433)
│   └── lightrag-server (port 9621, network_mode: host)
│       ├── LLM: OpenRouter → anthropic/claude-sonnet-4.6
│       ├── Embedding: Ollama → nomic-embed-text
│       └── Storage: PostgreSQL + NetworkX
├── Repomix (npm global, Node.js 20)
├── Claude Code (npm global, VPS上で実行)
│   └── MCP: lightrag → mcp_lightrag.py（search_knowledge + list_knowledge + list_projects）
├── graphify (pip global, Claude Code SKILL)
└── OpenClaw (Docker, port 46819) ※別プロジェクト

## 採用ツール

| ツール | 用途 | 利用方法 |
|---|---|---|
| Repomix | リポジトリ → テキスト化 | VPS CLI (repomix --remote) |
| DeepWiki MCP | リポジトリ構造分析 | Claude Code MCP |
| OpenRouter | LLM要約・自動分類 | VPS API（既存） |
| LightRAG | 知識グラフDB | VPS Docker（既存） |
| mcp_lightrag.py | Claude Code → LightRAG検索 | Claude Code MCP（stdio） |
| graphify | コード構造解析 | Claude Code内で /graphify <dir> |

## 認証情報

重要: .envファイルはgitに含まれていない。VPS上の /docker/lightrag/.env を参照。

- WebUI: http://76.13.187.66:9621 → admin / LightRag@2026!
- LightRAG API: Bearer token（login APIで取得）
- OpenRouter: .env内の LLM_BINDING_API_KEY

## API利用の定型パターン

トークン取得:
  curl -s -X POST "http://localhost:9621/login" -d "username=admin&password=LightRag@2026!" | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])"

ドキュメント投入:
  curl -s -X POST "http://localhost:9621/documents/upload" -H "Authorization: Bearer $TOKEN" -F "file=@target.txt"

ドキュメント削除:
  curl -s -X DELETE "http://localhost:9621/documents/delete_document" -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '{"doc_ids": ["doc-xxx"]}'

検索:
  curl -s -X POST "http://localhost:9621/query" -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '{"query":"検索クエリ", "mode":"hybrid"}'

ドキュメント一覧:
  curl -s "http://localhost:9621/documents" -H "Authorization: Bearer $TOKEN"

---

## 進捗管理

### 完了済み
- [x] LightRAG基盤構築（Docker + PostgreSQL + Ollama + OpenRouter）
- [x] WebUI動作確認
- [x] ドキュメント投入・検索の動作確認
- [x] Gitリポジトリ初期push
- [x] GSD計画書・アーキテクチャ・データスキーマ策定
- [x] ツール選定（Repomix + DeepWiki MCP + OpenRouter）
- [x] Phase 1: GitHub Ingestion Pipeline（ingest_github.sh完成）
- [x] Phase 2: SKILL Ingestion（9スキル投入）
- [x] Phase 3: ナレッジ活用SKILL（search_knowledge.sh + プロジェクト手順設定）
- [x] Phase 4: データ管理（タグ正規化・重複検知・鮮度チェック）
- [x] Phase 5: Cross-Project & Agent共有（MCP連携・プロジェクトフィルタリング・API利用ガイド・Git自動push）
- [x] graphifyインストール・Claude Code SKILL登録
- [x] ナレッジ42件投入（不正ドキュメント10件削除済み）

### 残タスク
- [ ] 知見フィードバックの半自動化（手動運用で開始、必要に応じて自動化）
- [ ] Obsidian Vault構成の最適化（運用しながら必要に応じて）

---

## 蓄積済みナレッジ（42件）

### GitHub OSS (32)
| 名前 | カテゴリ | 説明 |
|---|---|---|
| CrewAI | framework | マルチエージェントフレームワーク |
| LightRAG | framework | 知識グラフRAG |
| n8n | framework | ワークフロー自動化 |
| ComfyUI | framework | 画像生成パイプライン |
| ComfyUI-to-Python-Extension | tool | ComfyUIワークフロー→Pythonコード変換 |
| comfyui-api-wrapper | tool | ComfyUI APIラッパー |
| comfy_api_simplified | tool | ComfyUI API簡易クライアント |
| Mastra | framework | TypeScriptエージェントフレームワーク |
| MCP servers | framework | Model Context Protocolサーバー集 |
| OpenClaw公式 | agent | AIアシスタントフレームワーク |
| ruflo | agent | Claude Code用マルチエージェントスワームオーケストレーター |
| agency-agents | agent | 144専門エージェント定義集（12部門） |
| graphify | tool | コード・ドキュメントを知識グラフに変換するClaude Code SKILL |
| n8n-mcp | tool | n8n用MCPサーバー |
| n8n-as-code | tool | n8nワークフローのGitOps管理 |
| notebooklm-py | tool | NotebookLM非公式Python API + Agent Skill |
| obsidian-skills | agent | Obsidian Vault操作用Agent Skills |
| anthropic-cookbook | pattern | Claude API活用パターン集 |
| langgraph | framework | エージェントステートマシンフレームワーク |
| supabase | framework | BaaS（認証・DB・リアルタイム） |
| shadcn-ui | framework | UIコンポーネントライブラリ |
| vercel-ai | framework | Vercel AI SDK（Webアプリ×AI連携） |
| ccxt | framework | 仮想通貨取引所API統合ライブラリ |
| awesome-compose | pattern | Docker Composeパターン集 |
| gws-cli | tool | Google Workspace CLI + 100+ Agent Skills |
| cli-anything | tool | ソフトウェアCLI化フレームワーク |
| browser-use | tool | LLMブラウザ自動操作 |
| freqtrade | agent | 暗号通貨自動売買botフレームワーク |
| playwright-cli | tool | Agent Skills対応ブラウザ操作CLI |
| framer-motion | framework | Reactアニメーションライブラリ |
| NeMo-Agent-Toolkit | agent | NVIDIAマルチエージェントツールキット |
| awesome-design-md | website | 人気サイトのDESIGN.mdコレクション |

### ドキュメント (1)
| 名前 | カテゴリ | 説明 |
|---|---|---|
| Building LLM-Powered Applications with Claude | pattern | LLMアプリ構築ガイド |

### Claude Code SKILL (9)
| 名前 | 対象技術 |
|---|---|
| skill-creator | SKILL作成メタスキル |
| docx-creation | Word文書 |
| pdf-processing | PDF処理 |
| pdf-reading | PDF読み取り |
| pptx-creation | PowerPoint |
| xlsx-processing | Excel |
| frontend-design | フロントエンドUI |
| file-reading | ファイル読み取りルーター |
| product-self-knowledge | Anthropic製品情報 |

### MCP連携
| コンポーネント | 説明 |
|---|---|
| mcp_lightrag.py | Claude CodeからLightRAG検索を可能にするMCPサーバー（search_knowledge + list_knowledge + list_projects） |

---

## パイプラインコマンド

リポジトリ投入（Git自動push付き）:
  cd /docker/lightrag && ./scripts/ingest_github.sh <GitHub URL>

ナレッジ検索（ターミナル）:
  ./scripts/search_knowledge.sh "検索クエリ" [mode] [project]
  # project: openclaw, virtual-protocol, website, webapp, workflow

ナレッジ検索（Claude Code MCP）:
  Claude Code内でsearch_knowledgeツールを使用（project引数でフィルタリング可能）

タグ正規化（dry run / 実行）:
  python3 scripts/normalize_tags.py
  python3 scripts/normalize_tags.py --fix

重複チェック:
  python3 scripts/check_duplicates.py

鮮度チェック（確認 / 修正）:
  python3 scripts/check_freshness.py
  python3 scripts/check_freshness.py --fix

---

## ファイル構成

/docker/lightrag/
├── .env                    # 環境変数（git外）
├── .gitignore
├── docker-compose.yml
├── config/
│   └── project_profiles.json  # プロジェクト別フィルタ定義
├── docs/
│   └── AGENT-API-GUIDE.md  # エージェントAPI利用ガイド
├── scripts/
│   ├── ingest_github.sh    # GitHub投入パイプライン（Git自動push付き）
│   ├── summarize_repo.py   # LLM構造化要約（--graph-reportオプション対応）
│   ├── submit_to_lightrag.py # LightRAG API投入
│   ├── export_obsidian.py  # Obsidian MD生成
│   ├── search_knowledge.sh # ナレッジ検索（プロジェクトフィルタ対応）
│   ├── mcp_lightrag.py     # Claude Code用MCPサーバー（3ツール）
│   ├── normalize_tags.py   # タグ正規化
│   ├── check_duplicates.py # 重複検知
│   └── check_freshness.py  # 鮮度チェック
├── skill_data/             # SKILL構造化テキスト
├── obsidian-export/        # Obsidian Vault（GitHub閲覧）
│   ├── agent/
│   ├── framework/
│   ├── skills/
│   └── tool/
└── .git/

## 注意事項

- .envはgitに含めない。VPS上でのみ管理
- コンテナは restart: unless-stopped なのでVPS再起動後は自動復帰
- Ollamaは systemctl enable ollama 済み
- Claude CodeはVPS上にインストール済み（npm global）
- MCP lightragはプロジェクトスコープ（/docker/lightrag）で登録済み
- graphifyはpip global（graphifyy）でインストール済み。Claude Code内で /graphify として使用
- 計画ファイル（GSD-PLAN.md, ARCHITECTURE.md, DATA-SCHEMA.md, RESUME.md）はClaude.aiプロジェクトファイルで管理
- 開発環境はHostingerのWebターミナル（SSH不要）。コマンドはsshプレフィックスなし
