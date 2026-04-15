# KNOWLEDGE-INDEX.md — LightRAGナレッジベース インデックス

> 最終更新: 2026-04-15（移行完了後）
> 総数: 65件（移行前74件 → 8件削除 + 10件再構成）
> 最適レンジ: 80-120件

## レイヤー構成サマリー

| レイヤー | 件数 | 割合 | 目標 |
|---------|------|------|------|
| L3（実装） | 45件 | 69% | 50-60% |
| L2（パターン） | 9件 | 14% | 20-25% |
| L1（コンテキスト） | 7件 | 11% | 15-25% |
| 旧形式（未分類） | 4件 | 6% | 0% |

---

## L3: 実装ナレッジ（45件）

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
| 18 | supabase — BaaS/データベース | website | データベース |
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
| 31 | servers (MCP公式リファレンス) | tool | MCP参照 |

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

### スキルパック・コミュニティスキル（5件）
| # | ドキュメント | カテゴリ | 主要用途 |
|---|------------|---------|---------|
| 41 | deep-research — 並列リサーチ | skill | リサーチ |
| 42 | content-cascade — マルチプラットフォーム生成 | skill | コンテンツ |
| 43 | yt-pipeline — YouTube自動リサーチ | skill | リサーチ |
| 44 | hooks (Kallaway) — フック生成 | skill | コピーライティング |
| 45 | site-teardown — Webサイト逆解析 | skill | 分析 |
| 46 | dream — メモリ整理 | skill | メンテナンス |
| 47 | page-cro — CRO最適化 | skill | マーケティング |
| 48 | ai-seo — AI検索最適化 | skill | SEO |

---

## L2: パターンナレッジ（9件）

| # | ドキュメント | カテゴリ | 主要用途 |
|---|------------|---------|---------|
| 1 | スキル設計パターン集 — 検証済みアーキタイプ4種 | pattern | スキル設計 |
| 2 | SNSプラットフォーム別ライティングルール | pattern | コンテンツ |
| 3 | スキル最適化手法 — 診断・改善 | pattern | スキル改善 |
| 4 | mcollina/skills — Node.js ベストプラクティス | pattern | Node.js |
| 5 | Building LLM-Powered Applications with Claude | pattern | LLMアプリ |
| 6 | anthropic-cookbook — Claude APIクックブック | pattern | API活用 |

---

## L1: コンテキストナレッジ（7件）

| # | ドキュメント | カテゴリ | 変更 |
|---|------------|---------|------|
| 1 | note.com Claude Code記事収益化パイプライン | context | L2→L1 |
| 2 | きよびん — note.com著者キャラクター設定 | persona | pattern→L1 |
| 3 | note.com 自動投稿 技術要件まとめ | context | タグ修正 |
| 4 | Claude Code Masterclass カリキュラム構造分析 | research | pattern→L1 |
| 5 | git-art — 記事自動生成パターン | context | pattern→L1 |
| 6 | GitHub Actions × Claude Code 記事生成パターン集 | research | タグ修正 |
| 7 | OpenClaw — 仮想通貨自動取引エージェントプロジェクト | context | agent→L1 |

---

## 旧形式（未分類・要整理）（6件）

| # | ドキュメント | カテゴリ | 備考 |
|---|------------|---------|------|
| 1 | browser-use | agent | L3化検討 |
| 2 | codex-plugin-cc | agent | 自動開発参考 |
| 3 | agency-agents | agent | エージェント初期設定参考 |
| 4 | obsidian-skills | agent | MD連動用 |
| 5 | awesome-compose | infra | Docker Compose参照 |
| 6 | cli (Google Workspace) | tool | GWS自動化用 |

---

## 移行ログ（2026-04-15）

### Phase 1: 削除（8件）
FFmpeg, OpenSpace, claude-peers-mcp, ruflo, n8n-mcp, ComfyUI-to-Python-Extension, comfyui-api-wrapper, comfy_api_simplified

### Phase 2: L1再分類（6件）
note.com収益化パイプライン(L2→L1), きよびん(pattern→L1), note.com自動投稿技術要件(タグ修正), Masterclass(pattern→L1), git-art(pattern→L1), GitHub Actions記事生成(タグ修正)

### Phase 3: L3昇格 + L1再構成（4件）
MCP Servers(L1→L3), graphify(L1→L3), playwright-cli(L1→L3), OpenClaw(agent→L1)

### 旧版グラフデータ
doc_statusから削除した旧ドキュメントのグラフ埋め込みは残存。検索結果に旧版チャンクが表示されることがあるが実害なし。完全クリーンアップにはLightRAGのグラフ再構築が必要（低優先）。

---

## 次のアクション

1. APIキーローテーション（最優先・セキュリティ）
2. GSD-PLAN / RESUME更新
3. 旧形式6件のL3化検討（browser-use等）
4. L2パターン拡充（現9件→目標15-20件）
5. グラフ再構築（旧版データクリーンアップ、低優先）
