---
source: https://github.com/mastra-ai/mastra
category: framework
sub_categories: [agent, workflow]
tags: [typescript, llm, multi-agent, rag, mcp, ai-sdk, monorepo, observability]
language: 
ingested: 2026-04-09
source_updated: unknown
status: active
---

# mastra

# mastra

## 基本情報
- リポジトリ: https://github.com/mastra-ai/mastra
- カテゴリ: framework
- サブカテゴリ: agent, workflow
- タグ: TypeScript, LLM, multi-agent, RAG, MCP, AI-SDK, monorepo, observability
- 最終確認日: 2026-04-09

## 概要
Mastraは、TypeScriptで構築されたAIエージェント・ワークフロー開発フレームワークです。LLMエージェント、マルチエージェントシステム、RAGパイプライン、音声機能、MCPサーバー統合などを統合的に提供します。Vercel・Cloudflare・Netlifyなど複数のデプロイ先に対応し、包括的な認証・観測可能性・メモリ管理機能を備えています。

## 設計思想
モジュール式モノレポ構成を採用し、コア機能（エージェント・ワークフロー・メモリ・RAG）と周辺機能（認証・デプロイヤー・ブラウザ自動化・音声）を独立パッケージとして分離。AI SDK互換のストリーミングAPI、プラグイン可能なストレージ・ベクターDB・LLMプロバイダーをサポートするアダプターパターンを基盤とし、型安全なワークフロー定義とステップベースの制御フローを中心に設計されている。

## 主要コンポーネント
- Agent: LLMを用いてツール・メモリ・音声を組み合わせて推論・実行するエージェント本体
- Workflow: ステップ・並列・分岐・ループ・サスペンド/レジュームをサポートする型安全なワークフローエンジン
- Memory: 会話履歴・セマンティック検索・ワーキングメモリを統合したメモリ管理システム
- RAG Pipeline: ドキュメントチャンキング・埋め込み・ベクター検索・リランクを統合した検索拡張生成
- MCP Integration: Model Context Protocolサーバー・クライアントの構築と接続
- Deployers: Cloudflare Workers・Vercel・Netlify向けのデプロイアダプター
- Auth Providers: Auth0・Clerk・Supabase・WorkOS等の認証プロバイダー統合
- Mastra Client (JS/React): サーバーサイドMastraインスタンスへのタイプセーフなクライアントSDK

## 実装パターン
- Step-based Workflow: then/parallel/branch/foreach/dowhile/dountilによる宣言的ワークフロー定義とサスペンド・レジュームによる人間介在フロー
- Adapter Pattern: ストレージ・ベクターDB・LLMプロバイダー・認証・デプロイ先をすべてアダプターとして差し替え可能な設計
- Processor Pipeline: メッセージのPII検出・トークン制限・モデレーション・ツール検索などをチェーンとして構成するメッセージ処理パイプライン
- Streaming-first: AI SDK互換のストリーミングAPIでエージェント・ワークフロー双方の応答をリアルタイム配信
- Multi-agent Supervision: スーパーバイザーエージェントがサブエージェントをオーケストレーションするヒエラルキカルマルチエージェントパターン
- Tool-as-Workflow: ワークフローをエージェントのツールとして公開し、エージェントとワークフローを相互に組み合わせる統合パターン

## 適用シーン
LLMベースのAIアシスタント・カスタマーサポートBot・RAG検索システム・マルチエージェント自動化パイプライン・音声対話アプリケーション・ブラウザ自動化エージェント・CI/CD組み込み評価システムを構築するTypeScriptプロジェクト。特にNext.js・Express・Hono等のWebフレームワークとの統合や、Cloudflare/Vercel上へのエッジデプロイを想定したプロジェクトに適している。

## 注意点・制約
エンタープライズ機能（EEライセンス）は別ライセンス管理。Cloudflare Workersデプロイ時はPostgreSQL等のNode.js依存ストアに制約あり（Babelプラグインで自動検出）。ワークフローのサスペンド・タイムトラベル機能は永続化ストレージが必須。音声・ブラウザ機能は各プロバイダーAPIキーが別途必要。モノレポ構成のため個別パッケージのバージョン管理にChangesetsを使用しており、アップグレード時は移行ガイドの確認が必要。


## 関連ナレッジ
- (なし)
