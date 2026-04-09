---
source: https://github.com/freqtrade/freqtrade
category: framework
sub_categories: [tool, workflow]
tags: [python, algorithmic-trading, backtesting, hyperopt, freqai, ccxt, machine-learning, cryptocurrency]
language: 
ingested: 2026-04-09
source_updated: unknown
status: active
---

# freqtrade

# freqtrade

## 基本情報
- リポジトリ: https://github.com/freqtrade/freqtrade
- カテゴリ: framework
- サブカテゴリ: tool, workflow
- タグ: python, algorithmic-trading, backtesting, hyperopt, freqai, ccxt, machine-learning, cryptocurrency
- 最終確認日: 2026-04-09

## 概要
Freqtradeはオープンソースの暗号通貨アルゴリズムトレーディングボットフレームワークで、カスタム戦略の実装・バックテスト・ハイパーパラメータ最適化・ライブトレードをサポートする。CCXT経由で多数の取引所に対応し、FreqAIによる機械学習モデル統合も提供する。Telegram・Discord・REST APIによる通知・制御機能を備える。

## 設計思想
戦略をクラスベースのインターフェース（IStrategy）として定義し、シグナル生成・リスク管理・注文管理の関心を分離する。プラグインアーキテクチャにより、ペアリスト・プロテクション・FreqAIモデルを差し替え可能にし、設定ファイルとJSONスキーマで動作を制御する。バックテストとライブ取引で同一の戦略コードが動作するrunmode抽象化を採用している。

## 主要コンポーネント
- IStrategy: ユーザーがトレード戦略を実装するための基底インターフェース。エントリー・エグジットシグナル・コールバックを定義する
- FreqtradeBot: メインのボットループ。ウォレット管理・注文処理・取引ライフサイクルを統括する
- Exchange: CCXTラッパー。各取引所固有の差異を吸収し、統一されたAPIを提供する
- Backtesting: 過去データを用いた戦略シミュレーションエンジン。トレード並列処理とキャッシュ機能を備える
- Hyperopt: Optunaベースのハイパーパラメータ最適化エンジン。複数の損失関数から選択可能
- FreqAI: 機械学習モデル統合モジュール。LightGBM・XGBoost・PyTorch・強化学習をサポートし、スライディングウィンドウ学習を実装する
- PairlistManager: 動的ペアリスト管理。VolumePairList・MarketCapPairList等のフィルタをチェーン形式で適用する
- RPC / API Server: FastAPIベースのREST API・WebSocket・Telegram・Discord・Webhookによる通知と制御を提供する
- DataProvider: OHLCVデータ・オーダーフローデータの取得と提供。複数の時間足・ペアのデータを戦略に供給する
- ProtectionManager: ストップロスガード・クールダウン・最大ドローダウン保護などのリスク管理プラグインを管理する

## 実装パターン
- Strategy Plugin Pattern: IStrategyを継承したクラスとして戦略を実装し、resolverが動的にロードする。コアコードを変更せずに戦略を差し替えられる
- Pairlist Chain Filter: 複数のペアリストフィルタをパイプライン形式で適用し、取引対象ペアを動的に絞り込む
- Sliding Window Training: FreqAIがtrain_period_days/backtest_period_daysで定義されたウィンドウをスライドさせながらモデルを再訓練する
- Producer-Consumer Pattern: external_message_consumerにより、別ボットインスタンスからシグナルや分析済みデータフレームをWebSocket経由で受信する
- Dry-Run Simulation: 実際の注文を出さずに仮想ウォレットでライブ相場に対してトレードをシミュレートする
- Hyperopt Space Declaration: 戦略クラス内にDecimalParameter等でハイパーパラメータ空間を宣言し、Optunaが最適値を探索する
- Informative Decorator: @informativeデコレータで複数時間足・ペアのデータを宣言的に戦略へ注入する

## 適用シーン
暗号通貨の自動売買戦略を開発・検証・運用したいトレーダーや開発者に適する。バックテストによる戦略検証、ハイパーパラメータ最適化、FreqAIを用いたML駆動の予測モデル構築、スポット・先物・レバレッジ取引の自動化、複数ボット間でのシグナル共有システムの構築に役立つ。

## 注意点・制約
FreqAI・強化学習・PyTorch機能は追加の依存関係が必要で、ARM環境ではWHLファイルを手動で扱う必要がある。バックテスト結果はルックアヘッドバイアスに注意が必要（lookahead-analysis toolで検証可能）。取引所APIのレート制限やCCXT非対応取引所では機能制限が生じる。本番運用前に十分なドライラン検証が必要。


## 関連ナレッジ
- (なし)
