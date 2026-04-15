# GSD計画書: LightRAG ナレッジパイプライン

## プロジェクト概要

LightRAGを「外部脳」として活用し、GitHub OSS・Claude Code SKILL・技術ドキュメントから知識を構造化・蓄積し、複数プロジェクトの開発に横断的に活用するナレッジパイプラインを構築する。

## 前提条件

- LightRAG基盤構築済み（VPS: 76.13.187.66:9621）
- MCP: Named Tunnel経由（https://mcp.7272yusuke.cloud/mcp）
- OpenRouter + Ollama (nomic-embed-text 768dim) で動作中
- 利用者: 1名（開発者本人）
- 主要プロジェクト: OpenClaw（仮想通貨自動取引）、note.com収益化パイプライン、その他開発案件
- 開発領域: Website, Webアプリ, AIエージェント, n8nワークフロー

---

## ナレッジ3レイヤー構成

詳細は DATA-SCHEMA.md 参照。

| レイヤー | 定義 | 投入基準 |
|---------|------|---------|
| L3（実装） | 「作り方を知る」 | ドキュメントなしで実装開始できるレベル |
| L2（パターン） | 「組み合わせ方を知る」 | 検証済みのパターンのみ |
| L1（コンテキスト） | 「状況を知る」 | 意思決定に影響する情報のみ |

最適比率: L3 50-60% / L2 20-25% / L1 15-25%

投入ルール:
- リポジトリ/ツールは最初からL3品質で投入（L0-L1からの段階的昇格は禁止）
- 削除はDELETE API禁止（全消しバグ）。psql直接操作 + pg_dump必須
- 未検証のアイデアは入れない

---

## Phase 1-6: 基盤構築（2026-04-09〜04-10）✅

| Phase | 内容 | 状態 |
|---|---|---|
| 1 | GitHub Ingestion Pipeline | ✅ |
| 2 | SKILL Ingestion Pipeline | ✅ |
| 3 | ナレッジ活用SKILL | ✅ |
| 4 | データ管理・鮮度管理 | ✅ |
| 5 | Cross-Project & Agent共有 | ✅ |
| 6 | ナレッジ拡充（42件） | ✅ |

---

## Phase 7: バージョンアップ（2026-04-11）✅

- [x] DATA-SCHEMA.mdにバグパターンテンプレート追加
- [x] KNOWLEDGE-INDEX.md自動生成スクリプト
- [x] ccxt/freqtrade/n8n/openclaw レベル3化
- [x] ARCHITECTURE.md投入
- [x] 新規9リポジトリ投入（51件に拡大）
- [x] summarize_repo.pyリトライ+フォールバック+コード例自動生成

---

## Phase 8: MCP安定化 + セキュリティ（2026-04-12）✅

- [x] ドメイン取得（7272yusuke.cloud）
- [x] Cloudflare Named Tunnel構築
- [x] MCP固定URL化（https://mcp.7272yusuke.cloud/mcp）
- [x] mcp-lightrag.service + cloudflared-mcp.service（systemd）
- [x] Claude.aiからのMCPセッション安定動作確認
- [x] 重複SKILL v1/v2の削除（62件→52件）
- [x] DELETE APIバグ発見・pg_dumpからの復旧成功
- [x] SKILL 9件をL3品質で再投入

---

## Phase 9: ナレッジ拡充 第2波（2026-04-13〜04-14）✅

- [x] ComfyUI×2, tweepy, instagrapi, inngest投入
- [x] スキルパック3つ処理（research/content/community）
- [x] deep-research, yt-pipeline, content-cascade, hooks, site-teardown, dream, page-cro投入
- [x] SNSライティングルール（L2）抽出・投入
- [x] ai-seo, notebooklm-py完全版投入
- [x] skill-verifier作成（Claudeception方式）
- [x] 52件→74件に拡大

---

## Phase 10: 3レイヤー移行（2026-04-15）✅

- [x] knowledge-layer-rules.md策定
- [x] migration-plan.md策定（74件→65件計画）
- [x] 不要8件削除（FFmpeg, OpenSpace, claude-peers-mcp, ruflo, n8n-mcp, ComfyUI重複3件）
- [x] L1再分類6件（note.com系, きよびん, Masterclass, git-art, GitHub Actions）
- [x] L3昇格3件（MCP Servers, graphify, playwright-cli）+ OpenClaw L1再構成
- [x] 新規投入3件（superpowers L2, RAG-Anything L3, GSD L2）
- [x] 検索テスト合格 + KNOWLEDGE-INDEX.md更新 + git push

---

## Phase 11: スキル・ドキュメント整備（2026-04-15）✅

- [x] combination-architect スキルを3レイヤー体系に修正
- [x] knowledge-navigator スキルを3レイヤー体系に修正
- [x] KNOWLEDGE-INDEX.md を69件の現状に更新
- [x] Claude.aiプロジェクトファイル整理（VPS正運用に移行）
  - project-instructions-v2.md: 不変情報+セッション開始手順のみに簡素化
  - knowledge-layer-rules.md: 削除（DATA-SCHEMA.mdに統合）
  - migration-plan.md: 削除（移行完了、ログはKNOWLEDGE-INDEX.mdに記録）
- [x] RESUME.md / GSD-PLAN.md 更新

---

## 現在の状態（2026-04-15）

ナレッジベース: 69件（全processed）
- L3（実装）: 47件（68%）
- L2（パターン）: 11件（16%）
- L1（コンテキスト）: 7件（10%）
- グラフ残骸: 4件（タグ空表示、ドキュメント本体は削除済み）

## 残タスク（優先順）

1. [ ] OpenRouter APIキーローテーション（最優先・セキュリティ）
2. [ ] 未分類4件のL3/L2化検討（codex-plugin-cc, agency-agents, obsidian-skills, cli GWS）
3. [ ] L2パターン拡充（現11件→目標15-20件）
4. [ ] 旧版グラフデータクリーンアップ（低優先）
