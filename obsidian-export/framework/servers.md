---
source: https://github.com/modelcontextprotocol/servers
category: framework
sub_categories: [tool, protocol]
tags: [TypeScript, Python, MCP, model-context-protocol, LLM-integration, SSE, stdio-transport, multi-transport]
language: 
ingested: 2026-04-09
source_updated: unknown
status: active
---

# servers

# servers

## 基本情報
- リポジトリ: https://github.com/modelcontextprotocol/servers
- カテゴリ: framework
- サブカテゴリ: tool, protocol
- タグ: TypeScript, Python, MCP, model-context-protocol, LLM-integration, SSE, stdio-transport, multi-transport
- 最終確認日: 2026-04-09

## 概要
公式のModel Context Protocol (MCP) リファレンスサーバー実装集。filesystem、git、fetch、memory、sequentialthinking、timeなどの実用サーバーと、MCPの全機能を網羅したデモサーバー『everything』を含む。LLMクライアントとのツール・リソース・プロンプト連携を実証するための包括的なリファレンス実装。

## 設計思想
各サーバーはMCP SDKの上に構築されたモジュラー設計を採用。ツール・プロンプト・リソースを独立したサブモジュールに分離し、サーバーファクトリパターンで組み立てる。STDIO・SSE・Streamable HTTPの複数トランスポートをサポートし、マルチクライアント対応のセッション管理を実現。クライアントケーパビリティに基づく条件付きツール登録でプロトコルの適応性を示す。

## 主要コンポーネント
- everything server: MCP全機能（ツール、プロンプト、リソース、サブスクリプション、ロギング、タスク）を実証するリファレンスサーバー
- filesystem server: ファイルシステム操作をMCPツールとして公開するサーバー
- git server: Gitリポジトリ操作をMCPツールとして提供するPythonサーバー
- fetch server: HTTP取得機能をMCPツールとして公開するPythonサーバー
- memory server: セッション横断のメモリ永続化機能を提供するサーバー
- sequentialthinking server: 段階的思考プロセスをサポートするサーバー
- transport layer: STDIO・SSE・Streamable HTTPの3トランスポートを管理するモジュール群
- InMemoryTaskStore: MCP Tasks (SEP-1686)のタスクライフサイクルを管理する実験的コンポーネント

## 実装パターン
- Server Factory Pattern: createServer()でMcpServerインスタンスを生成し、ツール・リソース・プロンプトを一括登録。cleanup関数とともに返却する
- Conditional Tool Registration: oninitialized ハンドラ内でクライアントケーパビリティを確認後、elicitation/samplingなどの機能に依存するツールを遅延登録する
- Session-scoped Resources: セッションIDをキーにリソースを管理し、セッション終了時に自動クリーンアップ。gzip圧縮などの一時的な成果物に使用
- Bidirectional Tasks: SEP-1686に基づくタスクシステム。クライアント→サーバー方向とサーバー→クライアント方向の両方向でタスク実行をサポート
- Multi-transport Support: 同一のサーバーロジックをSTDIO/SSE/Streamable HTTPの各トランスポートに接続可能にする抽象化
- Simulated Notifications: セッションごとにインターバルを管理し、リソース更新通知やログメッセージを定期的にクライアントへ送信するデモ機能

## 適用シーン
MCPクライアント（Claude Desktop等）の開発・テスト時のリファレンス実装として活用。新規MCPサーバー開発の出発点、プロトコル機能の動作確認、LLMエージェントへのファイルシステム/Git/Web取得機能付与など。

## 注意点・制約
everythingサーバーのelicitation機能はSTDIOトランスポートのみ完全動作し、HTTPトランスポートでは制限あり。gzip-file-as-resourceはGZIP_MAX_FETCH_SIZE(デフォルト10MB)等の環境変数で制約。タスクAPIは実験的(experimental)パッケージに依存。新規サーバーのREADME追加PRは受け付けず、MCP Server Registryへの登録を推奨。


## 関連ナレッジ
- (なし)
