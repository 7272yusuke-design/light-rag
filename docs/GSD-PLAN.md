# GSD計画書: LightRAG ナレッジパイプライン

## プロジェクト概要

LightRAGを「外部脳」として活用し、GitHub OSS・Claude Code SKILL・技術ドキュメントから知識を構造化・蓄積し、複数プロジェクトの開発に横断的に活用するための情報収集パイプラインを構築する。

## 前提条件

- LightRAG基盤構築済み（VPS: 76.13.187.66:9621）
- OpenRouter + Ollama (nomic-embed-text) で動作確認済み
- 利用者: 1名（開発者本人）
- 主要プロジェクト: OpenClaw（仮想通貨自動取引）、Virtual Protocol関連、その他開発案件
- 開発領域: Website, Webアプリ, エージェント, n8nワークフロー

---

## 知識の3層構造

| 層 | 内容 | 保存先 | 消費者 |
|---|---|---|---|
| 外部知識 | GitHub OSS, 公開SKILL, 技術ドキュメント | LightRAG + Obsidian(MD) | 開発者 + エージェント |
| 開発知見 | トラブルシュート, 設計判断, 成功/失敗パターン | プロジェクト内SKILL | Claude Code（プロジェクト単位） |
| プロジェクト実態 | 現在のコード, 構成, 規約 | Git | Claude Code |

**原則:** 外部知識と開発知見は混ぜない。外部知識はプロジェクト横断で再利用可能な汎用性を持ち、開発知見はプロジェクト固有の文脈に依存する。

---

## 採用技術スタック

### リポジトリ → テキスト化
- **Repomix** (npm) — リポジトリをAIフレンドリーなテキストに変換。--remoteでclone不要、--compressでTree-sitter圧縮（トークン約70%削減）。MCP対応、Claude Code SKILL生成機能あり。

### 構造分析（設計レベルの理解）
- **DeepWiki公式MCP** (https://mcp.deepwiki.com/mcp) — 無料・認証不要。リポジトリの設計構造・コンポーネント関係をWiki形式で提供。Claude CodeからMCP経由で利用。
- **制約:** MCPプロトコル経由のみ（curlで直接叩けない）。VPSのbashパイプラインでは使えないため、Claude Code経由またはスクリプトでのMCPクライアント実装が必要。

### コード構造解析
- **graphify** (pip: graphifyy) — Claude Code SKILL。/graphify <dir> でコード・ドキュメント・PDFを知識グラフに変換。Tree-sitter ASTで20言語対応、71.5倍のトークン削減。LightRAGとの補完関係: LightRAGが外部知識、graphifyがプロジェクト内部構造理解。

### LLM要約・分類
- **OpenRouter** (既存) — Repomix出力をDATA-SCHEMAテンプレートに整形。カテゴリ・タグの自動判定を含む。

### 知識DB
- **LightRAG** (既存) — エンティティ抽出・知識グラフ・ハイブリッド検索。

### 学習ノート出力
- **Obsidian** — YAML frontmatter付きMDファイル。VPS上に生成、GitHubで閲覧。

### エージェント連携
- **mcp_lightrag.py** — Claude CodeからLightRAG APIを検索するMCPサーバー。MCP SDK (FastMCP) ベース、stdioトランスポート。

---

## Phase 1: GitHub Ingestion Pipeline ✅

### 目標
GitHub URLを入力すると、リポジトリの技術知見を構造化してLightRAGに投入し、同時に学習用MDをObsidian向けに出力するスクリプトを作る。

### 成果物
- scripts/ingest_github.sh — メインスクリプト（URL入力 → 全自動）
- scripts/summarize_repo.py — Repomix出力 → OpenRouter LLM要約 → 構造化テキスト生成
- scripts/submit_to_lightrag.py — LightRAG APIへの投入ラッパー
- scripts/export_obsidian.py — Obsidian用MDファイル生成
- obsidian-export/ — 学習用MD出力先

### タスク
- [x] VPSにRepomixをインストール
- [x] summarize_repo.py: Repomix出力をOpenRouterに送り構造化要約を生成
- [x] submit_to_lightrag.py: LightRAG APIへの投入ラッパー
- [x] export_obsidian.py: Obsidian用MD生成（frontmatter付き）
- [x] ingest_github.sh: 上記を統合するメインスクリプト
- [x] CrewAIリポジトリで動作検証

---

## Phase 2: SKILL Ingestion Pipeline ✅

### 目標
Claude Code SKILLファイル（公式 + 公開コミュニティ製）をLightRAGに投入する。

### 成果物
- skill_data/ — SKILL構造化テキスト + メタデータJSON

### タスク
- [x] SKILLファイルの収集と分類（/mnt/skills/public/ + skill-creator）
- [x] SKILL固有のメタデータ付与（カテゴリ、対象技術、利用シーン）
- [x] LightRAGへ投入（9スキル）
- [x] Obsidian用MD出力

---

## Phase 3: ナレッジ活用SKILL ✅

### 目標
Claude.aiプロジェクトからLightRAG APIを検索し、現在のプロジェクトに適応した提案を生成できるようにする。

### 成果物
- scripts/search_knowledge.sh — LightRAG検索ラッパー
- プロジェクト手順にナレッジ検索セクション追加

### タスク
- [x] LightRAG検索APIのラッパー作成
- [x] プロジェクト手順にナレッジ検索の使い方を追加
- [x] 検索テスト（SKILL作成方法の検索で有意な結果確認）

---

## Phase 4: データ管理・鮮度管理 ✅

### タスク
- [x] タグ正規化スクリプト（normalize_tags.py — 大文字小文字統一、エイリアス解決）
- [x] 重複・矛盾検知スクリプト（check_duplicates.py — タグ頻度、カテゴリ分布、ソースURL重複）
- [x] 鮮度チェックスクリプト（check_freshness.py — 180日超過で警告、--fixでstatus更新）
- [ ] Obsidian Vault構成の最適化（運用しながら必要に応じて）

---

## Phase 5: Cross-Project & Agent共有 ✅

### 目標
複数プロジェクト・複数エージェント間でナレッジを共有する仕組み。

### タスク
- [x] Claude Code用MCPサーバー作成（mcp_lightrag.py — search_knowledge + list_knowledge + list_projects）
- [x] Claude CodeからのLightRAG検索動作確認（MCP経由でナレッジ横断検索成功）
- [x] プロジェクトタグによるフィルタリング（config/project_profiles.json + クエリ拡張）
- [x] エージェントからのAPI利用ガイドライン（docs/AGENT-API-GUIDE.md）
- [ ] 知見フィードバックの半自動化（手動運用で開始、必要に応じて自動化）
- [x] ingest後のGit自動push（ingest_github.sh末尾に追加）

---

## Phase 6: ナレッジ拡充 ✅

### 目標
42件のナレッジを蓄積し、主要ドメイン（agent, framework, tool, website）をカバーする。

### タスク
- [x] GitHub OSS 32件投入（agent, framework, tool, website, patternカテゴリ）
- [x] Claude Code SKILL 9件投入
- [x] ドキュメント1件投入
- [x] 不正ドキュメント10件削除（agency-agentsのYAMLファイルが混入）
- [x] graphifyインストール・Claude Code SKILL登録

---

## スケジュール

| Phase | 期間 | 優先度 | 状態 |
|---|---|---|---|
| Phase 1 | 2026-04-09 | 最高 | ✅ 完了 |
| Phase 2 | 2026-04-09 | 高 | ✅ 完了 |
| Phase 3 | 2026-04-09 | 高 | ✅ 完了 |
| Phase 4 | 2026-04-09 | 中 | ✅ 完了 |
| Phase 5 | 2026-04-09 | 中 | ✅ 完了 |
| Phase 6 | 2026-04-10 | 中 | ✅ 完了 |
