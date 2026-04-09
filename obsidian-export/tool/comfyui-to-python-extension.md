---
source: https://github.com/pydn/ComfyUI-to-Python-Extension
category: tool
sub_categories: [workflow, framework]
tags: [python, comfyui, code-generation, stable-diffusion, ast-generation, cli, custom-nodes, workflow-export]
language: 
ingested: 2026-04-09
source_updated: unknown
status: active
---

# comfyui-to-python-extension

# ComfyUI-to-Python-Extension

## 基本情報
- リポジトリ: https://github.com/pydn/ComfyUI-to-Python-Extension
- カテゴリ: tool
- サブカテゴリ: workflow, framework
- タグ: python, comfyui, code-generation, stable-diffusion, ast-generation, cli, custom-nodes, workflow-export
- 最終確認日: 2026-04-09

## 概要
ComfyUI-to-Python-Extension はComfyUIのビジュアルワークフローを実行可能なPythonスクリプトに変換するツールです。Web UIの「Save As Script」ボタンからのエクスポートと、CLIによるAPI形式ワークフローJSONの変換の両方をサポートします。

## 設計思想
Planner/Renderer分離パターンを採用し、ワークフローノードの依存関係解析（LoadOrderDeterminer）、コード生成計画（WorkflowPlanner→GenerationPlan）、最終レンダリング（WorkflowRenderer）を明確に分離。ComfyUIランタイムとの疎結合を維持しつつ、生成スクリプトが単体実行可能な自己完結型コードになるよう設計されている。

## 主要コンポーネント
- WorkflowPlanner: ワークフローノードを解析し、変数名生成・依存解決・インポート文収集を行いGenerationPlanを構築する
- WorkflowRenderer: GenerationPlanを受け取り、最終的なスタンドアロンPythonソースコードを文字列として出力する
- LoadOrderDeterminer: DFSによりノード間依存関係を解決し、ローダー系ノードを優先した実行順序を決定する
- ExportApplication: ワークフロー読み込み・計画・レンダリングを統合するオーケストレーター
- node_runtime: ComfyUIパスの解決・sys.path追加・カスタムノード初期化・モデルクリーンアップなどのランタイム環境構築を担当する
- save-as-script.js: ComfyUI Web UIに「Save As Script」メニュー項目を追加するフロントエンド拡張

## 実装パターン
- Planner-Renderer分離: ワークフロー解析・計画フェーズ（WorkflowPlanner）と出力生成フェーズ（WorkflowRenderer）を独立したクラスに分離し、中間表現（GenerationPlan dataclass）で接続するパターン
- Frozen Dataclassによる中間表現: GenerationPlanをfrozen=TrueのDataclassとして定義し、Planner→Rendererへの不変なデータ受け渡しを保証する
- DFS依存解決: LoadOrderDeterminerがDFSでノードグラフを走査し、依存ノードを先行実行順に並べることでトポロジカルソートを実現する
- ファサードパターン: ComfyUItoPythonクラスが後方互換性のある公開APIファサードとして機能し、内部リファクタリングから利用者を保護する
- 環境変数によるパス解決: COMFYUI_PATH環境変数を優先し、未設定時は親ディレクトリを再帰検索するフォールバック戦略でComfyUIランタイムを動的に探索する

## 適用シーン
ComfyUIで構築した画像生成ワークフローをCI/CDパイプラインや自動化スクリプトに組み込みたい場合、Web UIを使わずにバッチ生成を繰り返し実行したい場合、またはワークフローをコードとしてバージョン管理・共有したいプロジェクトに有用。

## 注意点・制約
Python 3.12以上が必須。生成スクリプトの実行には別途ComfyUIのインストールが必要であり、COMFYUI_PATH環境変数または親ディレクトリ探索でComfyUIが見つかる必要がある。生成スクリプトはシングルショット実行を想定しており、長期稼働のプロンプトサーバーとしては設計されていない。ワークフロー入力の自動CLI引数化は行われないため、パラメータ変更はスクリプト手動編集が必要。


## 関連ナレッジ
- (なし)
