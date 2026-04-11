---
source: https://github.com/stripe/stripe-cli
category: tool
sub_categories: [workflow, infra]
tags: [golang, stripe-api, webhook, cli, grpc, openapi, plugin-system, websocket]
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
- タグ: golang, stripe-api, webhook, cli, grpc, openapi, plugin-system, websocket
- 最終確認日: 2026-04-11

## 概要
Stripe CLIは、Stripe APIとのローカル開発・テストを支援するコマンドラインツールです。Webhookのローカルフォワーディング、APIリクエストの送信、イベントのトリガー、ログのテーリング、サンプルプロジェクトの生成などの機能を提供します。gRPCベースのRPCサービスを内蔵し、IDEプラグインや外部ツールとの連携も可能です。

## 設計思想
OpenAPI仕様から自動生成されたCLIコマンド群を核とし、gRPCによるRPCサービス層でプラグインやIDEとのインテグレーションを実現。WebSocketを用いたリアルタイムイベントストリーミング、プロファイルベースの設定管理、プラットフォーム別ビルドを考慮した設計。コード生成（gen/）により仕様変更への追従を自動化している。

## 主要コンポーネント
- pkg/proxy: StripeサーバーからローカルエンドポイントへのWebhookイベントフォワーディング
- pkg/rpcservice: gRPCベースのRPCサービス。IDE・プラグインとのIPC通信を担当
- pkg/plugins: サードパーティプラグインの管理・実行ランタイム（gRPCプロトコル）
- pkg/logtailing: Stripe APIリクエストログのリアルタイムストリーミング
- pkg/login: OAuth/APIキーベースの認証フロー（ポーリング・インタラクティブ）
- gen/: OpenAPI仕様からCLIコマンドおよびリソーススペックを自動生成
- pkg/websocket: StripeダッシュボードとのWebSocket接続管理
- rpc/: Protocol BuffersによるgRPCサービス定義

## 実装パターン
- OpenAPI駆動コード生成: gen/配下のテンプレートとOpenAPIスペックからCLIコマンド・リソーススペックを自動生成し、API仕様との同期を維持
- gRPC Plugin Interface: プラグインとのプロセス間通信にgRPCを採用し、バージョン互換性のある拡張可能なインターフェースを提供
- WebSocket Event Streaming: WebSocketを介してStripeのリアルタイムイベント・ログをサブスクライブし、ローカルにフォワード
- Profile-based Config: 複数のStripeアカウント・環境をプロファイルで管理し、設定の切り替えを容易にする
- Fixture-based Testing: JSONフィクスチャを用いたAPIレスポンスのモック・再現によるカナリアテスト

## 適用シーン
Stripe決済を統合するWebアプリ・バックエンドの開発者がローカル環境でWebhookをテストする場合、Stripe APIを素早く探索・呼び出したい場合、CI/CDパイプラインでのStripe連携テスト自動化、IDEプラグイン開発でStripe機能を組み込む場合に有用。

## 注意点・制約
Stripe固有のツールであり汎用性はない。OpenAPI仕様の自動生成部分はStripe内部プロセスに依存するため外部からの更新は困難。プラグインシステムはgRPCバージョン互換性に注意が必要。Windowsサポートは一部機能（ANSI、uname等）で別実装が必要。


## 関連ナレッジ
- (なし)
