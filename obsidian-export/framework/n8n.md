---
source: https://github.com/n8n-io/n8n
category: framework
sub_categories: [agent, workflow, tool]
tags: [TypeScript, n8n, LangChain, MCP, LangGraph, automation, multi-agent, low-code]
language: 
ingested: 2026-04-09
source_updated: unknown
status: active
---

# n8n

# n8n

## 基本情報
- リポジトリ: https://github.com/n8n-io/n8n
- カテゴリ: framework
- サブカテゴリ: agent, workflow, tool
- タグ: TypeScript, n8n, LangChain, MCP, LangGraph, automation, multi-agent, low-code
- 最終確認日: 2026-04-09

## 概要
n8nはノードベースのワークフロー自動化プラットフォームであり、AIエージェント・マルチエージェントシステム・外部サービス連携を統合的に構築できるフレームワークです。LangChain/LangGraphを活用したAIワークフロービルダー、MCP（Model Context Protocol）統合、コード実行サンドボックスなどを含む包括的なオートメーション基盤を提供します。

## 設計思想
モノレポ構造（packages/@n8n/）でフロントエンド・バックエンド・AIレイヤーを分離し、依存性注入（DI）とデコレータパターンで疎結合を実現。AIエージェントはLangGraphのステートマシンとして実装され、ツール・メモリ・MCPサーバーを抽象化したSDKを通じて拡張可能な設計。ワークフローはYjs CRDTによるリアルタイム協調編集に対応し、TypeORMによるDB抽象化と多数のマイグレーションで長期的な後方互換性を維持する。

## 主要コンポーネント
- @n8n/agents: AIエージェントランタイム・SDK・MCPクライアント・評価フレームワーク・ワークスペースツール群
- @n8n/ai-workflow-builder.ee: LangGraphベースのマルチエージェントワークフロービルダー（プランナー・スーパーバイザー・レスポンダー構成）
- @n8n/instance-ai: n8nインスタンス全体を操作するAIエージェント（ワークフロー・クレデンシャル・実行・データテーブル管理ツール群）
- @n8n/db: TypeORMエンティティ・リポジトリ・マイグレーション管理（SQLite/PostgreSQL対応）
- @n8n/ai-utilities: LangChain連携アダプター・ベクターストア・トークナイザー・ログラッパー
- @n8n/crdt: Yjsベースのリアルタイム協調編集（WebSocket/BroadcastChannel/MessagePortトランスポート）
- @n8n/mcp-browser: Playwright経由のブラウザ操作MCPサーバー（ナビゲーション・インタラクション・タブ管理）
- @n8n/expression-runtime: isolated-vmを使ったサンドボックス内での式評価・LRUキャッシュ・遅延プロキシ

## 実装パターン
- マルチエージェント・スーパーバイザーパターン: LangGraphのStateGraphでプランナー・スーパーバイザー・コードビルダー・レスポンダーエージェントを組み合わせ、タスクを分担・調整するマルチエージェントアーキテクチャ
- ツールとしてのMCP統合: MCPサーバーを動的に接続し、そのツールをエージェントのネイティブツールとして透過的に利用するアダプターパターン
- スペック駆動開発（SDD）: SkillファイルとClaudeプラグインを使い、AIがコードを生成・検証するプロセスをドキュメント化したワークフロー
- CRDTによる協調編集: Yjsドキュメントを複数トランスポート層で同期し、Undo/Redoとawareness（カーソル共有）を提供
- デコレータベースDI: @Module/@Controller/@OnLifecycleEventなどのデコレータでメタデータを付与し、DIコンテナがライフサイクルを管理
- プログラマティック評価ハーネス: LLMが生成したワークフローをバイナリチェック・LLMジャッジ・ペアワイズ評価の複数軸で自動スコアリング
- サンドボックスワークスペース: コード実行用のサンドボックス（Daytona/n8n独自）でファイルシステム・プロセスをカプセル化し、エージェントがファイル操作・コマンド実行を安全に行う

## 適用シーン
SaaS・社内システム・AIとのインテグレーションを自動化するワークフロー基盤が必要なプロジェクト。LLMを活用した自然言語によるワークフロー生成・編集機能（AIビルダー）を実装したいケース。MCPプロトコルで外部ツールをエージェントに統合したいケース。TypeORMベースのマルチテナント型SaaSバックエンドのリファレンス実装として活用したいケース。

## 注意点・制約
Enterprise Edition（.ee.ts）機能は別ライセンスが必要。AIワークフロービルダーはLangSmith等の外部トレーシング前提の設計部分がある。マイグレーション数が200超と多く、既存DBスキーマへの適用には慎重なテストが必要。MCP BrowserはPlaywright依存でブラウザ環境が必須。モノレポのビルド順序依存が複雑で、個別パッケージの切り出しには追加作業が発生する。


## 関連ナレッジ
- (なし)
