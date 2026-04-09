---
source: https://github.com/supabase/supabase
category: website
sub_categories: [webapp, framework]
tags: [TypeScript, Next.js, MDX, Supabase, design-system, documentation, Tailwind, React]
language: 
ingested: 2026-04-09
source_updated: unknown
status: active
---

# supabase

# supabase

## 基本情報
- リポジトリ: https://github.com/supabase/supabase
- カテゴリ: website
- サブカテゴリ: webapp, framework
- タグ: TypeScript, Next.js, MDX, Supabase, design-system, documentation, Tailwind, React
- 最終確認日: 2026-04-09

## 概要
Supabaseの公式ドキュメントサイトおよびデザインシステムのモノリポジトリ。Next.jsベースのドキュメントポータル（guides、reference、troubleshootingを含む）と、Supabase独自UIコンポーネントライブラリ（design-system）の2つのアプリで構成される。

## 設計思想
Next.js App RouterとMDXを中心に、コンテンツ駆動型のドキュメントアーキテクチャを採用。shadcn/uiベースのデザインシステムをカスタム拡張し、コンポーネントレジストリパターンで管理。AI補助機能（埋め込み検索、コードサンプル生成）を統合し、テレメトリ・フィードバック機構を内包する。エージェント/AIコーディング支援向けのスキル定義（.agents, .claude, .cursor）も整備されている。

## 主要コンポーネント
- apps/docs: Next.js App Routerベースのメインドキュメントサイト。guides・reference・troubleshootingの各セクションを持つ
- apps/design-system: Supabase独自UIコンポーネントライブラリのドキュメント・デモサイト。shadcn/uiをベースにカスタムコンポーネントを提供
- features/docs: MDXレンダリング・リファレンス生成・トラブルシューティングページなどのドキュメント機能モジュール
- generator/: CLI・SDK・APIリファレンスを仕様ファイルから自動生成するスクリプト群
- registry/: コンポーネントの登録・管理を行うレジストリシステム（shadcn/ui互換）
- .agents / .claude / .cursor: AIコーディングエージェント向けのスキル定義・ルール・ベストプラクティス集

## 実装パターン
- MDXコンテンツ駆動アーキテクチャ: ガイド・リファレンス・トラブルシューティングをMDXファイルとして管理し、rehype/remarkプラグインで変換・レンダリング
- コンポーネントレジストリパターン: shadcn/ui互換のレジストリ（registry/）でUIコンポーネントを登録・ビルドスクリプトで配布物を自動生成
- リファレンス自動生成: CliSpec・SdkSpec・ConfigSpecなどの仕様ファイルからAPIリファレンスページをコード生成
- AIスキル定義パターン: .agents/.claude/.cursorディレクトリにSKILL.md/RULE.mdを配置しAIエージェントの挙動をガイド
- テレメトリ統合: ページビュー・フィードバック・コマンドメニュー操作などをtelemetry.client.tsxで一元管理

## 適用シーン
BaaSプラットフォームの大規模ドキュメントサイト構築、MDXベースのデザインシステムドキュメント、shadcn/uiカスタムコンポーネントライブラリの参考実装、AIエージェント向けコーディングルール整備の参考として活用できる。

## 注意点・制約
Supabase固有のインフラ（Supabaseクライアント、独自認証、OpenAI連携）に依存しており、そのままの流用は困難。コンテンツ量が非常に多くビルド時間が長い。design-systemはSupabase内部向けコンポーネントが多くそのままの外部利用は想定されていない。


## 関連ナレッジ
- (なし)
