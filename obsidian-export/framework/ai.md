---
source: https://github.com/vercel/ai
category: framework
sub_categories: [agent, webapp]
tags: [TypeScript, AI-SDK, LLM, streaming, multi-provider, tool-calling, Next.js, MCP]
language: 
ingested: 2026-04-09
source_updated: unknown
status: active
---

# ai

# ai

## 基本情報
- リポジトリ: https://github.com/vercel/ai
- カテゴリ: framework
- サブカテゴリ: agent, webapp
- タグ: TypeScript, AI-SDK, LLM, streaming, multi-provider, tool-calling, Next.js, MCP
- 最終確認日: 2026-04-09

## 概要
Vercel AI SDKは、TypeScript/JavaScript向けのAIアプリケーション構築フレームワークで、OpenAI・Anthropic・Google等の多数のLLMプロバイダーを統一APIで扱える。テキスト生成・ストリーミング・構造化オブジェクト生成・ツール呼び出し・エージェントループ・埋め込み・画像/音声/動画生成など幅広いAI機能を提供する。Next.js/Express/Hono/Fastify/NestJS等のフレームワークおよびReact/Angular/SvelteなどのUIフレームワークとシームレスに統合できる。

## 設計思想
プロバイダー抽象化レイヤーを中核に置き、異なるLLMプロバイダーを交換可能にする。UI層（useChat/useCompletion等のReactフック）・コア層（generateText/streamText等）・プロバイダー層の3層アーキテクチャを採用。ストリーミングファーストで設計され、UIメッセージストリームプロトコルによりサーバーからクライアントへのリアルタイム更新を実現する。ミドルウェアパターンでキャッシュ・ログ・RAG等の横断的関心事を注入可能。

## 主要コンポーネント
- AI SDK Core: generateText/streamText/generateObject等の基本AI操作API、ツール呼び出し、エージェントループ、埋め込み、マルチモーダル対応
- AI SDK UI: useChat/useCompletion/useObjectのReactフック群、UIメッセージストリームのクライアント側処理
- Provider Abstraction: OpenAI・Anthropic・Google・Bedrock等30以上のプロバイダーへの統一インターフェース
- MCP Client: Model Context Protocolクライアント実装、外部ツールサーバーとの統合
- Middleware System: キャッシュ・RAG・ロギング・ガードレール等をモデル呼び出しにラップするミドルウェア機構
- AI SDK RSC: React Server ComponentsでのAI生成UIのストリーミングレンダリング

## 実装パターン
- Streaming Tool Calling: streamTextでツール呼び出しをストリーミングしながら実行し、maxStepsによる多段エージェントループを実現する
- UIメッセージストリームプロトコル: サーバーからクライアントへの型付きストリームイベント（テキスト・ツール・データパーツ等）を統一フォーマットで転送する
- Provider Middleware: wrapLanguageModelでプロバイダーをラップし、キャッシュ・ロギング・RAG・デフォルト設定を横断的に適用する
- Structured Output: zodスキーマを用いてLLMの出力をタイプセーフな構造化オブジェクトとして生成・ストリーミングする
- Human-in-the-loop: ツール承認フロー、中断・再開可能なストリームによって人間の介入ポイントをエージェントループに組み込む
- Resumable Streams: チャットセッションのストリームを永続化・再接続可能にし、ネットワーク断やサーバー再起動に対応する

## 適用シーン
LLMを使ったチャットボット・AIエージェント・RAGシステム・マルチモーダルアプリケーションを構築するプロジェクト全般。特にNext.js等のReactエコシステム上でストリーミングUIを伴うAIアプリを開発する場合、複数のAIプロバイダーを切り替えて使いたい場合、MCPサーバーと連携したツール拡張エージェントを構築したい場合に最適。

## 注意点・制約
AI SDK RSC（React Server Components向け）はNext.js App Routerに強く依存しており他環境への移植は困難。プロバイダーごとに対応機能（推論・ツール・マルチモーダル等）に差異があり、抽象化が完全ではないケースがある。v7系でbreaking changesが多くマイグレーションコストが発生する。ストリーミングはVercel等のサーバーレス環境のタイムアウト制限に注意が必要。


## 関連ナレッジ
- (なし)
