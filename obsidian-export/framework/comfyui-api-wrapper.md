---
source: https://github.com/ai-dock/comfyui-api-wrapper
category: framework
sub_categories: [workflow, tool]
tags: [python, fastapi, comfyui, stable-diffusion, image-generation, websocket, async-queue, s3-upload]
language: 
ingested: 2026-04-09
source_updated: unknown
status: active
---

# comfyui-api-wrapper

# comfyui-api-wrapper

## 基本情報
- リポジトリ: https://github.com/ai-dock/comfyui-api-wrapper
- カテゴリ: framework
- サブカテゴリ: workflow, tool
- タグ: python, fastapi, comfyui, stable-diffusion, image-generation, websocket, async-queue, s3-upload
- 最終確認日: 2026-04-09

## 概要
ComfyUI APIラッパーで、FastAPIベースのプロダクション向けインターフェースを提供する。非同期・同期・SSEストリーミングの3種類のエンドポイントを持ち、前処理・生成・後処理の3ステージワーカーパイプラインでComfyUIワークフローを実行する。S3アップロード、Webhook通知、Redis/インメモリキャッシュをサポートする。

## 設計思想
3ステージパイプライン（Preprocess→Generation→Postprocess）をAsyncio Queueで疎結合に接続するワーカープール設計。ワークフロー変換をModifierパターンで抽象化し、静的JSONワークフローと動的修飾クラスの両方に対応する。設定は環境変数とペイロード直接指定のダブルフォールバック方式を採用。

## 主要コンポーネント
- PreprocessWorker: URLダウンロード・ワークフロー変換を担当する前処理ワーカー
- GenerationWorker: ComfyUI APIへのジョブ投入とWebSocket監視で生成完了を待機するワーカー
- PostprocessWorker: 生成ファイルの移動・S3アップロード・Webhook通知を行う後処理ワーカー
- BaseModifier: ワークフローJSON読み込み・URL置換・ランダムシード生成の基底クラス
- main.py (FastAPI): 非同期・同期・SSEストリーミングの3エンドポイントとキュー管理を提供するAPIサーバー

## 実装パターン
- Pipeline Worker Queue: asyncio.Queueで繋がれた3ステージワーカーパイプライン。各ステージのワーカー数を独立してスケール可能
- Modifier Pattern: BaseModifierを継承してapply_modifications()をオーバーライドすることで、特定ワークフローへの変換ロジックをカプセル化
- URL Content Caching: ダウンロード済みURLをMD5ハッシュファイル名でComfyUI inputディレクトリにキャッシュし、重複ダウンロードを防止
- SSE Streaming: Server-Sent Eventsでキュー位置・進捗・最終結果をリアルタイム配信
- Dual Config Fallback: リクエストペイロードのS3/Webhook設定を優先し、未設定時は環境変数の集中設定にフォールバック

## 適用シーン
ComfyUIをバックエンドとする画像・動画・音声生成サービスのAPI層として活用できる。RunPod等のGPUインスタンスでComfyUIと同居させてセルフホスト生成APIを構築するユースケース、またはフロントエンドアプリケーションへのSSEストリーミングで生成進捗をリアルタイム表示するケースに適している。

## 注意点・制約
ComfyUIインスタンスが同一ホストまたはアクセス可能なURLで稼働していることが前提。GenerationWorkerはWebSocket接続でジョブを監視するため、ComfyUIのWebSocket APIが有効である必要がある。水平スケール時はRedisキャッシュが必須で、複数インスタンス間でリクエストストアを共有しなければならない。python-magicはlibmagic1のネイティブライブラリ依存があり、Dockerイメージへの追加インストールが必要。


## 関連ナレッジ
- (なし)
