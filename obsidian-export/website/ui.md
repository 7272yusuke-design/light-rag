---
source: https://github.com/shadcn-ui/ui
category: website
sub_categories: [framework, tool]
tags: [TypeScript, React, Next.js, Tailwind-CSS, shadcn-ui, component-library, design-system, RTL-support]
language: 
ingested: 2026-04-09
source_updated: unknown
status: active
---

# ui

# ui

## 基本情報
- リポジトリ: https://github.com/shadcn-ui/ui
- カテゴリ: website
- サブカテゴリ: framework, tool
- タグ: TypeScript, React, Next.js, Tailwind-CSS, shadcn-ui, component-library, design-system, RTL-support
- 最終確認日: 2026-04-09

## 概要
shadcn/uiの公式ドキュメントサイト兼コンポーネントレジストリ（v4）。50以上のReactコンポーネントをTailwind CSS v4ベースで提供し、複数のデザインベース（luma、lyra、maia、mira、nova、vega）とテーマカスタマイザーを備える。CLIによるコンポーネントインストール、MCP連携、v0統合などのエコシステムを構築している。

## 設計思想
コンポーネントをコピー&ペーストで所有するという哲学を維持しつつ、レジストリシステムを通じた配布を実現。複数のUIベース（Radix UI、Base UI等）をサポートするクロスフレームワーク設計。デザインシステムはCSS変数とTailwind v4トークンで管理され、ライト/ダークモード・RTLを標準サポート。

## 主要コンポーネント
- Registry System: コンポーネントをJSON形式で管理・配布するレジストリ基盤（/public/r/styles/配下）
- Theme Customizer: カラー・フォント・ラジウス・アクセントをインタラクティブに調整するUIビルダー
- Block System: ダッシュボード・認証・サイドバー等の複合UIブロックをプレビュー・配布
- Design System Provider: 複数ベース（luma/lyra/maia/mira/nova/vega）のデザイントークンを切り替えるプロバイダー
- LLM Route: AIアシスタント向けにコンポーネントドキュメントをLLM最適化形式で配信
- MCP Integration: Model Context Protocolを通じたAIツールとの連携エンドポイント
- Examples App: Dashboard・Tasks・Playground・Authentication等のフルページデモ実装

## 実装パターン
- Multi-Base Registry: 同一コンポーネントをRadix UI・Base UI等の複数プリミティブベース向けに並行管理するパターン
- Copy-Owned Components: 依存パッケージではなくソースコードをプロジェクトにコピーして所有するshadcnの核心パターン
- CSS Variable Theming: Tailwind v4のCSS変数ベースのデザイントークンシステムでライト/ダーク/カスタムテーマを管理
- Registry JSON Schema: コンポーネント・ブロック・フォント・スタイルをJSONスキーマで定義しCLI配布するレジストリプロトコル
- Iframe Preview: ブロックやコンポーネントをiframe内で独立プレビューするサンドボックスパターン

## 適用シーン
React/Next.js製アプリのUIコンポーネント導入、デザインシステム構築、カスタムコンポーネントレジストリの公開、AI（v0/MCP）連携UIジェネレーションワークフローの構築に適している。

## 注意点・制約
Tailwind CSS v4必須でv3との互換性は限定的。コンポーネントはコピー所有のためアップストリームの変更を手動で追跡する必要がある。複数ベース（Radix/Base UI）でファイルが重複管理されメンテナンスコストが高い。


## 関連ナレッジ
- (なし)
