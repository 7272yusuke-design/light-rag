---
source: https://github.com/crewaiinc/crewai
category: framework
sub_categories: [agent, workflow]
tags: [python, multi-agent, LLM, RAG, MCP, crewai, orchestration, autonomous-agents]
language: 
ingested: 2026-04-09
source_updated: unknown
status: active
---

# crewai

# crewai

## 基本情報
- リポジトリ: https://github.com/crewaiinc/crewai
- カテゴリ: framework
- サブカテゴリ: agent, workflow
- タグ: python, multi-agent, LLM, RAG, MCP, crewai, orchestration, autonomous-agents
- 最終確認日: 2026-04-09

## 概要
CrewAIはLLMを活用した自律型マルチエージェントシステムを構築するためのPythonフレームワークです。エージェント・タスク・クルー・フローという概念を中心に、複数のAIエージェントが協調して複雑なワークフローを実行できる仕組みを提供します。RAG、MCP統合、人間参加型ループ、観測機能など企業利用に対応した豊富な機能を備えています。

## 設計思想
Role-based agentアーキテクチャを採用し、エージェントに役割・目標・バックストーリーを定義することで専門性を持たせる。Crew（順次・階層プロセス）とFlow（イベント駆動ステートマシン）の2つの実行モデルを提供し、シンプルなタスクから複雑なオーケストレーションまで対応。イベントバスによる疎結合な観測・フック機構、プラグイン可能なLLMプロバイダー・ストレージ・エンベディングレイヤーにより高い拡張性を実現。

## 主要コンポーネント
- Crew: 複数エージェントとタスクをまとめて実行するオーケストレーター。順次・階層プロセスをサポート
- Agent: 役割・目標・ツールを持つLLM駆動の自律的実行単位
- Task: エージェントに割り当てる作業単位。条件付きタスク・ガードレール・出力フォーマット指定が可能
- Flow: イベント駆動のステートマシンで複雑なマルチクルーワークフローを定義
- LLM: OpenAI・Anthropic・Gemini・Bedrock・Azureなど複数プロバイダーを抽象化するLLMレイヤー
- Knowledge: PDF・CSV・JSON等のドキュメントをRAGで検索可能にするナレッジソース
- Memory: ChromaDB・Qdrant・LanceDB等を用いたエージェントの短期・長期記憶管理
- MCP Client: stdio・SSE・StreamableHTTPでMCPサーバーに接続し外部ツールを取得
- EventBus: エージェント・タスク・LLM・ツールのライフサイクルイベントを配信する観測基盤
- A2A: Agent-to-Agentプロトコル実装。外部エージェントへの委譲とUI拡張をサポート

## 実装パターン
- Decorator-based Crew定義: @CrewBase・@agent・@task・@crewアノテーションでYAML設定とPythonコードを宣言的に結合
- Flow State Machine: @start・@listen・@router・@and_・@or_デコレータでイベント駆動の非同期ワークフローを構築
- Native Tool Calling: OpenAI・Anthropic・Gemini・BedrockのネイティブFunction Calling APIを活用し、ReActループ不要でツール実行
- Hierarchical Process: マネージャーエージェントがサブエージェントにタスクを委譲する階層型実行モデル
- LLM Hook Pipeline: before/afterフックでLLM呼び出しをインターセプトし、ロギング・認証・変換を注入
- Checkpointing: SQLiteベースの状態永続化でFlowの中断・再開とHuman-in-the-Loopを実現
- VCR Cassette Testing: LLM APIレスポンスをYAMLカセットに録画・再生することで決定論的なインテグレーションテストを実施

## 適用シーン
研究・コンテンツ生成・データ分析・コーディング支援などの複雑なマルチステップタスクを自動化したいプロジェクト。複数のAIエージェントを役割分担させてパイプライン処理したいエンタープライズシステム。Slack・Zapier・Google Workspaceなどの外部サービスとLLMを統合した業務自動化ワークフロー。RAGやMCPツールを組み合わせた知識ベース駆動のエージェントアプリケーション。

## 注意点・制約
LLMプロバイダーごとにFunction Calling挙動が異なるため、モデル切替時に動作検証が必要。Flowの状態管理はSQLite前提のため大規模分散環境では別途設計が必要。テレメトリはデフォルトで有効のためプライバシー要件に応じてオプトアウト設定が必要。知識ソースのChromaDB依存はローカルファイルシステムを使用するためサーバーレス環境では制約あり。litellm依存が除去される移行期にあるため古いコードとの互換性に注意。


## 関連ナレッジ
- (なし)
