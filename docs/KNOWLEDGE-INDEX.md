# KNOWLEDGE-INDEX.md — LightRAGナレッジベース インデックス

> 最終更新: 2026-04-15（セッション16.0）
> 総数: 69件（全processed）
> 最適レンジ: 80-120件

## レイヤー構成サマリー

| レイヤー | 件数 | 割合 | 目標 |
|---------|------|------|------|
| L3（実装） | 47件 | 68% | 50-60% |
| L2（パターン） | 11件 | 16% | 20-25% |
| L1（コンテキスト） | 7件 | 10% | 15-25% |
| 旧形式（グラフ残骸） | 4件 | 6% | 0% |

---

## L3: 実装ナレッジ（47件）

### フレームワーク・ライブラリ（19件）
| # | ドキュメント | カテゴリ | 主要用途 |
|---|------------|---------|---------|
| 1 | Next.js — フルスタックReactフレームワーク | framework | Webアプリ・LP |
| 2 | Stripe SDK — 決済・サブスクリプション API | framework | 決済 |
| 3 | Resend + React Email — トランザクショナルメールAPI | tool | メール送信 |
| 4 | inngest — Durable Workflow Orchestration | framework | ワークフロー |
| 5 | tweepy — X (Twitter) API Python SDK | framework | SNS連携 |
| 6 | instagrapi — Instagram Private API Python SDK | framework | SNS連携 |
| 7 | ccxt — 仮想通貨取引所API | framework | 取引 |
| 8 | freqtrade — 自動取引・バックテスト | framework | 取引 |
| 9 | langgraph — グラフベースエージェント | framework | エージェント |
| 10 | crewai — マルチエージェントオーケストレーション | framework | エージェント |
| 11 | mastra — TypeScript LLMエージェント | framework | エージェント |
| 12 | ai (Vercel AI SDK) — マルチプロバイダーLLM | framework | LLM統合 |
| 13 | motion (framer-motion) — Reactアニメーション | framework | UI |
| 14 | LightRAG — グラフRAGフレームワーク | framework | ナレッジ管理 |
| 15 | n8n — ワークフロー自動化 | workflow | 自動化 |
| 16 | ComfyUI API/サーバー | framework | 画像生成 |
| 17 | ComfyUI グラフ実行エンジン | framework | 画像生成 |
| 18 | RAG-Anything — マルチモーダルRAG（LightRAG拡張） | framework | マルチモーダルRAG |
| 19 | NeMo-Agent-Toolkit — NVIDIA エージェント | framework | エージェント |

### ツール・CLI（12件）
| # | ドキュメント | カテゴリ | 主要用途 |
|---|------------|---------|---------|
| 20 | MCP Servers — MCPサーバー開発リファレンス | framework | MCP開発 |
| 21 | graphify — ナレッジグラフビルダー | tool | コード解析 |
| 22 | playwright-cli — ブラウザ自動化CLI | tool | ブラウザ自動化 |
| 23 | firecrawl — Webスクレイピング | tool | データ収集 |
| 24 | ui (shadcn-ui) — UIコンポーネント | tool | UI |
| 25 | awesome-design-md — デザインシステム | website | デザイン |
| 26 | notebooklm-py — NotebookLM CLI（完全版） | tool | リサーチ |
| 27 | cli (GitHub CLI) — gh コマンド | tool | GitHub操作 |
| 28 | stripe-cli — Stripe CLI | tool | 決済開発 |
| 29 | vercel — Vercel CLI | tool | デプロイ |
| 30 | n8n-as-code — n8n GitOps | tool | ワークフロー |
| 31 | supabase — BaaS/ドキュメントサイト | website | データベース |

### Claude Code SKILL（9件）
| # | ドキュメント | カテゴリ | 主要用途 |
|---|------------|---------|---------|
| 32 | skill-docx | skill | Word文書 |
| 33 | skill-pdf | skill | PDF作成 |
| 34 | skill-pdf-reading | skill | PDF読取 |
| 35 | skill-pptx | skill | プレゼン |
| 36 | skill-xlsx | skill | スプレッドシート |
| 37 | skill-frontend-design | skill | フロントエンド |
| 38 | skill-file-reading | skill | ファイル読取 |
| 39 | skill-product-self-knowledge | skill | Anthropic製品情報 |
| 40 | skill-creator | skill | スキル作成 |

### スキルパック・コミュニティスキル（7件）
| # | ドキュメント | カテゴリ | 主要用途 |
|---|------------|---------|---------|
| 41 | deep-research — 並列リサーチ | skill | リサーチ |
| 42 | content-cascade — マルチプラットフォーム生成 | skill | コンテンツ |
| 43 | yt-pipeline — YouTube自動リサーチ | skill | リサーチ |
| 44 | hooks (Kallaway) — フック生成 | skill | コピーライティング |
| 45 | site-teardown — Webサイト逆解析 | skill | 分析 |
| 46 | dream — メモリ整理 | skill | メンテナンス |
| 47 | page-cro — CRO最適化 | skill | マーケティング |

---

## L2: パターンナレッジ（11件）

| # | ドキュメント | カテゴリ | 主要用途 |
|---|------------|---------|---------|
| 1 | スキル設計パターン集 — 検証済みアーキタイプ4種 | pattern | スキル設計 |
| 2 | SNSプラットフォーム別ライティングルール | pattern | コンテンツ |
| 3 | ai-seo — AI検索最適化（AEO/GEO/LLMO） | skill | SEO |
| 4 | スキル最適化手法 — 診断・改善 | pattern | スキル改善 |
| 5 | mcollina/skills — Node.js ベストプラクティス | pattern | Node.js |
| 6 | Building LLM-Powered Applications with Claude | pattern | LLMアプリ |
| 7 | anthropic-cookbook — Claude APIクックブック | pattern | API活用 |
| 8 | superpowers — エージェント開発ワークフロー&スキルフレームワーク | pattern | スキル開発 |
| 9 | GSD — スペック駆動開発 & コンテキストエンジニアリング | pattern | プロジェクト管理 |
| 10 | browser-use — LLMブラウザ自動化エージェント | agent | ブラウザ操作 |
| 11 | awesome-compose — Docker Composeリファレンス | infra | コンテナ |

---

## L1: コンテキストナレッジ（7件）

| # | ドキュメント | カテゴリ | 備考 |
|---|------------|---------|------|
| 1 | note.com Claude Code記事収益化パイプライン | context | L2→L1再分類済 |
| 2 | きよびん — note.com著者キャラクター設定 | persona | pattern→L1再分類済 |
| 3 | note.com 自動投稿 技術要件まとめ | context | タグ修正・再投入済 |
| 4 | Claude Code Masterclass カリキュラム構造分析 | research | pattern→L1再分類済 |
| 5 | git-art — 記事自動生成パターン | context | pattern→L1再分類済 |
| 6 | GitHub Actions × Claude Code 記事生成パターン集 | research | タグ修正・再投入済 |
| 7 | OpenClaw — 仮想通貨自動取引エージェントプロジェクト | context | agent→L1再構成済 |

---

## 旧形式（グラフ残骸のみ）（4件）

doc_statusから旧版ドキュメントは削除済み。グラフテーブル（entities/relations）に残骸が残存するためlist_knowledgeでタグ空として表示される。検索に実害なし。

| # | 旧ドキュメント名 | 置換先 |
|---|-----------------|--------|
| 1 | note.com 自動投稿 技術要件まとめ | note-autopost-requirements-l1_lightrag.txt |
| 2 | playwright-cli | playwright-cli-l3_lightrag.txt |
| 3 | MCP Servers | mcp-servers-l3_lightrag.txt |
| 4 | GitHub Actions記事生成パターン集 | github-actions-article-patterns-l1_lightrag.txt |

> クリーンアップ: グラフテーブルから該当チャンクIDを削除、または全グラフ再構築。低優先。

---

## 未分類の既存ドキュメント（L3化 or L2化検討）

以下は旧形式のままだがドキュメント本体は存在。必要に応じてL3/L2品質に再投入。

| # | ドキュメント | 現カテゴリ | 検討 |
|---|------------|----------|------|
| 1 | codex-plugin-cc | agent | 自動開発参考。L3化検討 |
| 2 | agency-agents | agent | エージェント初期設定参考。L2化検討 |
| 3 | obsidian-skills | agent | MD連動用。L3化検討 |
| 4 | cli (Google Workspace) | tool | GWS自動化用。L3化検討 |

---

## 移行ログ

### 2026-04-15 セッション15.0
- Phase 1: 8件削除（FFmpeg, OpenSpace, claude-peers-mcp, ruflo, n8n-mcp, ComfyUI-to-Python-Extension, comfyui-api-wrapper, comfy_api_simplified）
- Phase 2: 6件L1再分類（note.com収益化, きよびん, note.com自動投稿, Masterclass, git-art, GitHub Actions記事生成）
- Phase 3: 4件L3昇格/L1再構成（MCP Servers, graphify, playwright-cli, OpenClaw）
- 新規投入: superpowers(L2), RAG-Anything(L3), GSD(L2)

### 2026-04-15 セッション16.0
- KNOWLEDGE-INDEX.md を69件の現状に更新
- combination-architect / knowledge-navigator スキルを3レイヤー体系に修正

---

## 次のアクション

1. **APIキーローテーション**（最優先・セキュリティ）
2. **GSD-PLAN / RESUME更新**
3. **未分類4件のL3/L2化検討**（codex-plugin-cc, agency-agents, obsidian-skills, cli GWS）
4. **L2パターン拡充**（現11件 → 目標15-20件）
5. **グラフ残骸クリーンアップ**（低優先）
