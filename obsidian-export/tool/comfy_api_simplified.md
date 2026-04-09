---
source: https://github.com/deimos-deimos/comfy_api_simplified
category: tool
sub_categories: [agent, workflow]
tags: [python, comfyui, mcp, websocket, image-generation, stable-diffusion, api-wrapper]
language: 
ingested: 2026-04-09
source_updated: unknown
status: active
---

# comfy_api_simplified

# comfy_api_simplified

## 基本情報
- リポジトリ: https://github.com/deimos-deimos/comfy_api_simplified
- カテゴリ: tool
- サブカテゴリ: agent, workflow
- タグ: python, comfyui, mcp, websocket, image-generation, stable-diffusion, api-wrapper
- 最終確認日: 2026-04-09

## 概要
ComfyUI APIのPythonラッパーライブラリ。APIフォーマットのワークフローをプログラム的に編集・キューイングし、画像生成結果を取得できる。MCPサーバー機能も搭載し、AIエージェントからComfyUIを操作可能にする。

## 設計思想
薄いラッパー設計を採用し、ComfyUI APIの構造をそのまま扱いつつノードタイトルベースの直感的な操作インターフェースを提供。MCPサーバーはステートレス設計でワークフローdictを入出力に用いることでAIエージェントとの親和性を高めている。

## 主要コンポーネント
- ComfyApiWrapper: ComfyUI HTTPエンドポイントとWebSocket通信を抽象化するクライアント。プロンプトのキューイング、画像取得、履歴参照などを担う
- ComfyWorkflowWrapper: APIフォーマットのワークフローJSONをdictとして継承し、ノードタイトルベースでパラメータ読み書きを行うラッパー
- mcp_server: FastMCPを用いてComfyUI操作をAIエージェント向けツール群として公開するMCPサーバー
- exceptions: ComfyApiErrorとNodeNotFoundErrorの独自例外定義

## 実装パターン
- WebSocket polling: queue_prompt_and_waitでUUID client_idを発行しWebSocket経由で実行完了を待機。crystoolsなど無関係なメッセージをスキップする
- Stateless workflow mutation: MCPツールはワークフローdictを引数に受け取り変更後のdictを返す。状態をサーバー側に持たず複数のset_node_paramをチェーンしてrun_workflowに渡す
- Title-based node addressing: ノードIDではなくノードタイトル(_meta.title)でノードを参照し、同名ノードが複数ある場合はUserWarningを発行

## 適用シーン
ComfyUIを使った画像生成パイプラインの自動化、大量プロンプトのバッチ処理、AIエージェント(Claude等)からのComfyUI操作、i2i/t2iワークフローのプログラム制御

## 注意点・制約
Basic認証とno-auth(ローカル)のみサポート。async環境でqueue_and_wait_imagesを呼ぶ場合nest_asyncioが必要。同名ノードが複数存在する場合の動作は最初のノードのみ参照または全ノード変更となる。


## 関連ナレッジ
- (なし)
