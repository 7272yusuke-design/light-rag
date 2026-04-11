---
source: https://github.com/stripe/stripe-cli
category: tool
sub_categories: [workflow, infra]
tags: [golang, stripe-api, cli, webhook, grpc, openapi, plugin-system, payment]
language: 
ingested: 2026-04-11
source_updated: unknown
status: active
---

# stripe-cli

# stripe-cli

## 基本情報
- リポジトリ: https://github.com/stripe/stripe-cli
- カテゴリ: tool
- サブカテゴリ: workflow, infra
- タグ: golang, stripe-api, cli, webhook, grpc, openapi, plugin-system, payment
- 最終確認日: 2026-04-11

## 概要
Stripe CLIは、StripeのAPIとWebhookをローカル開発環境でテスト・操作するための公式コマンドラインツールです。Webhookのリアルタイムリスニング、APIリクエストの送信、イベントのトリガー、ログのテーリングなどの機能を提供します。gRPCベースのRPCサービスレイヤーを持ち、プラグインシステムによって機能を拡張できます。

## 設計思想
Go言語で実装されたCLIツールで、cobra/cobraベースのコマンド構造を採用。OpenAPI仕様から自動生成されたリソースコマンド群を持ち、gRPCを介したRPCサービスレイヤーでUI/デーモン分離を実現。プラグインはgRPCプロトコルで通信する独立プロセスとして実装され、WebSocketを使ったWebhookプロキシが開発時のイベント受信を担う。

## 主要コンポーネント
- proxy/proxy.go: WebSocketを通じてStripeサーバーからWebhookイベントをローカルエンドポイントに転送するプロキシ
- rpcservice/: gRPCベースのサービス層。listen、login、trigger、fixtures等の機能をRPCとして公開
- rpc/*.proto: CLI機能のgRPCインターフェース定義（listen、login、trigger、logs等）
- pkg/cmd/resources/resources_gen.go: OpenAPI仕様から自動生成されたStripe APIリソースコマンド群
- plugins/: gRPCプロトコルを使ったサードパーティプラグインのランタイム管理
- logtailing/tailer.go: StripeダッシュボードのAPIログをリアルタイムでストリーミングするテーラー
- stripeauth/client.go: デバイス認証フローを処理するStripe認証クライアント
- gen/: OpenAPI仕様からリソースコマンドやイベントリストを自動生成するコードジェネレーター

## 実装パターン
- OpenAPI Code Generation: spec3.cli.jsonのOpenAPI定義からGoのリソースコマンドを自動生成。gen/gen_resources_cmds.goがテンプレートベースでresources_gen.goを生成する
- gRPC Plugin System: プラグインを独立したgRPCサーバープロセスとして実行し、CLIがクライアントとして通信。バージョン管理・自動更新機能付き
- WebSocket Webhook Proxy: StripeサーバーとのWebSocket接続を維持し、受信したWebhookイベントをローカルHTTPエンドポイントに転送
- Fixture-based Testing: JSONフィクスチャファイルを使いStripe APIリソースの作成・操作シナリオを定義し再現可能なテスト環境を構築
- Profile-based Config: 複数のStripeアカウント/環境をプロファイルとして管理し、APIキーや設定を切り替え可能

## 適用シーン
Stripe決済を統合するWebアプリ・バックエンドの開発者が、ローカル環境でWebhookをテストしたり、APIリクエストをCLIから直接実行したり、Stripeイベントをシミュレートしたりする際に使用。CI/CDパイプラインでのStripeインテグレーションテストにも活用できる。

## 注意点・制約
Stripe固有のツールであり他の決済サービスには使用不可。WebhookリスニングはStripeサーバーへのWebSocket接続を必要とするためオフライン環境では動作しない。プラグインはgRPCプロトコルの特定バージョンに依存するため互換性管理が必要。OpenAPI仕様からの自動生成コードは手動編集不可。


## 関連ナレッジ
- (なし)
