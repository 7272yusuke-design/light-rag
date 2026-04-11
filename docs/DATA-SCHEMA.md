# データスキーマ設計: ナレッジ構造化ルール

## 設計方針

1. 検索精度 > 網羅性 — 曖昧な情報より、正確で再利用可能な単位を優先
2. メタデータは投入時に付与 — 後から付けるのはコストが高い
3. 1ドキュメント = 1関心事 — 巨大なドキュメントは分割して投入
4. 鮮度は明示的に管理 — 投入日とソースの更新日を記録
5. カテゴリは固定、タグはLLM自由判定 — 大分類は人間が管理、小分類はLLMが付けて後から正規化

---

## ナレッジカテゴリ（固定・大分類）

LLMが自動判定する際、以下から1つ選択する。

### ドメインカテゴリ

| カテゴリ | 説明 | 例 |
|---|---|---|
| framework | フレームワーク・ライブラリの設計思想と使い方 | CrewAI, LangChain, FastAPI, Next.js |
| pattern | 実装パターン・アーキテクチャパターン | マルチエージェント, Pub/Sub, RAG, MVC |
| tool | ツール・CLI・開発支援の使い方 | Docker, git, Claude Code SKILL, Repomix |
| protocol | プロトコル・API仕様 | Virtual Protocol, OpenRouter API, MCP |
| infra | インフラ・デプロイ・運用 | VPS設定, PostgreSQL, Nginx, CI/CD |
| crypto | 仮想通貨・DeFi固有の知識 | DEX, トークン発行, ウォレット連携 |

### 開発領域カテゴリ

| カテゴリ | 説明 | 例 |
|---|---|---|
| website | Webサイト構築（静的・動的・デザイン） | LP, アニメーション, レスポンシブ |
| webapp | Webアプリケーション開発 | 認証, DB設計, API設計, ダッシュボード |
| agent | AI エージェント・自律システム | マルチエージェント, ツール連携, 推論ループ |
| workflow | ワークフロー自動化 | n8n, Make, 自動化パイプライン |

注: 1つのリポジトリが複数カテゴリに該当する場合、最も主要な1つをcategoryに、残りをsub_categoriesに入れる。

---

## タグ運用ルール

### LLM自動タグ付けの指針

LLMは要約時に3〜8個のタグを自由に付与する。ただし以下のルールに従う：

必須タグ:
- 言語タグ（python, typescript, rust など）

推奨タグ:
- ドメインタグ（trading, agent, web3, animation など）
- パターンタグ（multi-agent, rag, pipeline, scroll-effect など）
- 技術タグ（react, nextjs, fastapi, framer-motion など）

禁止:
- 汎用的すぎるタグ（code, development, programming）
- 3単語以上のタグ（multi-agent-orchestration-pattern → multi-agent）
- カテゴリ名と同一のタグ（frameworkをタグとして使わない）

### タグ正規化ルール（normalize_tags.py で自動適用）

全タグは小文字に統一。以下のエイリアスは正規形にマージ：

| 正規化前 | 正規化後 |
|---|---|
| nextjs, next.js, Next | nextjs |
| react, React.js, reactjs | react |
| multi-agent, multiagent | multi-agent |
| TypeScript, Typescript | typescript |
| MCP, model-context-protocol | mcp |
| RAG | rag |
| LLM | llm |
| FastAPI | fastapi |
| Docker | docker |
| SQLite | sqlite |

---

## LightRAG投入テキストのテンプレート

### GitHub リポジトリ用

  # [リポジトリ名]
  ## 基本情報
  - リポジトリ: [GitHub URL]
  - 言語: [主要言語]
  - カテゴリ: [自動判定結果]
  - サブカテゴリ: [自動判定結果]
  - タグ: [自動生成タグ]
  - 最終確認日: [YYYY-MM-DD]
  ## 概要
  [1-3文でリポジトリの目的を説明]
  ## 設計思想
  [アーキテクチャや設計哲学]
  ## 主要コンポーネント
  - [コンポーネント名]: [役割と責務]
  ## 実装パターン
  - [パターン名]: [どういう場面でどう使っているか]
  ## 適用シーン
  [どういうプロジェクトや課題にこの知識が役立つか]
  ## 注意点・制約
  [既知の制限、非推奨事項、ハマりポイント]

### Claude Code SKILL用

  # SKILL: [スキル名]
  ## 基本情報
  - ソース: [公式 / ユーザー作成 / コミュニティ]
  - カテゴリ: tool
  - 対象技術: [docx / pdf / pptx / etc]
  - 最終確認日: [YYYY-MM-DD]
  ## 概要
  [このSKILLが何をするか]
  ## 使用トリガー
  [どういう指示でこのSKILLが発動するか]
  ## 主要手順
  [SKILLの核心的な手順を要約]
  ## ベストプラクティス
  [このSKILLを使う上でのコツ、注意点]
  ## 関連技術
  [このSKILLと組み合わせて使える他の技術やツール]

---

## Obsidian MD出力テンプレート

  ---
  source: [URL or filepath]
  category: [自動判定カテゴリ]
  sub_categories: [サブカテゴリリスト]
  tags: [tag1, tag2, tag3]
  language: [python, typescript, etc]
  ingested: [YYYY-MM-DD]
  source_updated: [YYYY-MM-DD or unknown]
  status: [active / outdated / review-needed]
  ---
  # [タイトル]
  [本文]
  ## 関連ナレッジ
  - [[関連ドキュメント1]]

---

## 鮮度管理ルール

| status | 意味 | アクション |
|---|---|---|
| active | 最新で正確 | そのまま利用可 |
| review-needed | 180日以上更新なし | 再取得・再要約を検討 |
| outdated | 明確に古い情報 | 検索結果に含めるが警告を表示 |

自動チェック: check_freshness.py で投入日から180日経過を検出。--fixで自動的に review-needed へ遷移。

---

## ドキュメント分割ルール

LightRAGのエンティティ抽出精度を保つため：

- 1ドキュメント 3000文字目安以下（日本語の場合）
- 巨大リポジトリは「概要」「主要コンポーネント詳細」「実装パターン集」に分割
- 分割時はドキュメント名にサフィックスを付与（例: crewai-overview, crewai-patterns）

---

## 注意事項

- agency-agentsのようなYAML形式のエージェント定義ファイルはLightRAGのテンプレートに沿わないため投入しない
- 巨大リポジトリ（10M tokens超）はrepomixで0.2%程度しか使えないため、graphifyで事前に構造把握してから重要部分を特定する
- LightRAGは重複排除の自動検知機能あり（同一内容の再投入はスキップされる）

---

## バグ修正パターンテンプレート

投入時は以下の形式に従う。

    ## バグ: <タイトル>（<修正日> 修正）
    - 症状: <ユーザーから見た現象>
    - 原因: <技術的な根本原因>
    - 修正: commit <hash> / <ファイル名・関数名>
    - 再発防止: <テスト方法・チェック観点>
    - 関連モジュール: <ファイル / クラス / メソッド>
