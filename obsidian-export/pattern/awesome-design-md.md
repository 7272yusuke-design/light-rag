---
source: https://github.com/VoltAgent/awesome-design-md
category: pattern
sub_categories: [website, tool]
tags: [markdown, design-system, design-tokens, UI-components, AI-agent, LLM-context, style-guide]
language: 
ingested: 2026-04-10
source_updated: unknown
status: active
---

# awesome-design-md

# awesome-design-md

## 基本情報
- リポジトリ: https://github.com/VoltAgent/awesome-design-md
- カテゴリ: pattern
- サブカテゴリ: website, tool
- タグ: markdown, design-system, design-tokens, UI-components, AI-agent, LLM-context, style-guide
- 最終確認日: 2026-04-10

## 概要
著名なWebサイト・プロダクトのビジュアルデザインシステムをMarkdown形式（DESIGN.md）で収集したキュレーションリポジトリ。AIエージェントが読み取り可能な形式で、カラーパレット・タイポグラフィ・コンポーネントスタイルを定義している。Google Stitchが提唱するDESIGN.mdフォーマットに準拠し、60近くの有名サービスのデザイン言語を提供する。

## 設計思想
LLMが最も読みやすいMarkdown形式を採用し、特別なツールやスキーマなしにAIコーディングエージェントがUIを生成できることを目指す。Figmaエクスポートやカスタムトークンファイル不要で、プロジェクトルートに置くだけで即座に利用可能な「プレーンテキストデザインシステム」を実現。

## 主要コンポーネント
- DESIGN.md: 各ブランドのビジュアル言語を定義するメインドキュメント（カラー・タイポグラフィ・コンポーネント・レイアウト原則を含む）
- preview.html / preview-dark.html: デザイントークンの視覚的カタログ（カラースウォッチ・タイプスケール・ボタン・カードを表示）
- design-md/ ディレクトリ: ブランド別にREADMEとDESIGN.mdを整理したコレクション構造

## 実装パターン
- Brand-per-directory構造: 各ブランドを独立したディレクトリに格納し、README.mdでgetdesign.mdへの正規URLを提供するリダイレクト方式
- Stitch DESIGN.mdフォーマット: Visual Theme・Color Palette・Typography・Components・Layout・Elevation・Do's/Don'ts・Responsive・Agent Prompt Guideの9セクション構成の標準フォーマット準拠

## 適用シーン
AI（LLM）エージェントを使ってUIを生成する際に、特定ブランドのデザイン言語を忠実に再現したいプロジェクト。デザインシステムの参考資料として、または「Vercelっぽいページを作って」のようなプロンプトに具体的なデザイン根拠を与えたい場合に有用。

## 注意点・制約
実際のDESIGN.mdファイルの内容はgetdesign.mdホスティングサービスに移行済みで、リポジトリ内には参照READMEのみ存在する。抽出されたデザイントークンは公開CSSから取得したものであり、各ブランドのビジュアルアイデンティティの所有権を主張するものではない。PR受付は既存ファイルの修正のみで、新規DESIGN.md追加は受け付けていない。


## 関連ナレッジ
- (なし)
