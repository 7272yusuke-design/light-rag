改善したSKILL.md全文を出力します。

---

```markdown
---
name: freqtrade
description: Freqtradeを使った暗号通貨ボットの戦略実装・バックテスト・Hyperopt最適化・FreqAI機械学習・ライブトレード設定に関する作業が発生したら必ずこのスキルを使え。IStrategy・populate_indicators・populate_entry_trend・custom_stoploss・@informative・VolumePairList・Producer-Consumerなど、Freqtrade固有のAPIやパターンが関わる場面では即座に参照せよ。
---

# freqtrade

## 概要
Freqtradeはオープンソースの暗号通貨アルゴリズムトレーディングボットフレームワークで、カスタム戦略の実装・バックテスト・ハイパーパラメータ最適化・ライブトレードをサポートする。CCXT経由で100以上の取引所に対応し、FreqAIによる機械学習モデル統合、Telegram/Discord/REST APIによる通知・制御機能を備える。戦略はIStrategyを継承したPythonクラスとして実装し、コアコードを変更せずにプラグイン形式で差し替えられる。

## いつ使うか
- IStrategyを継承したカスタムトレード戦略を実装・修正したいとき
- `populate_indicators` / `populate_entry_trend` / `populate_exit_trend` のロジックを書くとき
- `custom_stoploss` / `confirm_trade_entry` / `custom_exit` 等のコールバックを実装するとき
- バックテストの実行・結果分析・パフォーマンス改善を行うとき
- Hyperopt（Optuna）でROI・ストップロス・エントリー/エグジット条件を最適化するとき
- FreqAIでLightGBM・XGBoost・PyTorch・強化学習モデルを戦略に統合するとき
- `@informative` デコレータで複数時間足やクロスペアデータを注入するとき
- VolumePairList・AgeFilter・SpreadFilter等でペアリストを構成するとき
- Producer-Consumerパターンで複数ボット間のシグナル共有を構築するとき
- Telegram・Discord・Webhook・REST APIによるBot通知・リモート制御を設定するとき

## 主要コマンド・API

### インストール・初期化
```bash
# pipでインストール
pip install freqtrade

# 設定ファイルの雛形生成
freqtrade new-config --config user_data/config.json

# 新規戦略ファイルの生成
freqtrade new-strategy --strategy MyStrategy

# FreqAI対応戦略の生成
freqtrade new-strategy --strategy MyFreqAIStrategy --template freqai
```

### データ取得
```bash
# OHLCVデータのダウンロード（Binance, 1h足, 過去180日）
freqtrade download-data \
  --exchange binance \
  --pairs BTC/USDT ETH/USDT \
  --timeframe 1h \
  --days 180

# 複数時間足を一括ダウンロード
freqtrade download-data \
  --exchange binance \
  --pairs BTC/USDT \
  --timeframes 5m 1h 1d \
  --days 365

# ペアリスト対象の全ペアを取得（configからペアリストを読み込み）
freqtrade download-data \
  --config user_data/config.json \
  --timeframe 1h \
  --days 180
```

### バックテスト
```bash
# 基本的なバックテスト
freqtrade backtesting \
  --config user_data/config.json \
  --strategy MyStrategy \
  --timerange 20230101-20231231

# トレード詳細をエクスポート
freqtrade backtesting \
  --config user_data/config.json \
  --strategy MyStrategy \
  --timerange 20230101-20231231 \
  --export trades

# 複数戦略の比較バックテスト
freqtrade backtesting \
  --config user_data/config.json \
  --strategy-list Strategy1 Strategy2 Strategy3 \
  --timerange 20230101-20231231
```

### Hyperopt（ハイパーパラメータ最適化）
```bash
# Hyperopt実行（Sharpe比損失関数、200エポック）
freqtrade hyperopt \
  --config user_data/config.json \
  --strategy MyStrategy \
  --hyperopt-loss SharpeHyperOptLoss \
  --epochs 200 \
  --spaces buy sell roi stoploss trailing

# 結果のベストをJSON表示
freqtrade hyperopt-show --best --print-json

# 上位10件のエポックを表示
freqtrade hyperopt-show --profitable --print-json -n 10
```

### ライブ・Dry-Runトレード
```bash
# Dry-Runモード（仮想ウォレット、dry_run: trueがデフォルト）
freqtrade trade \
  --config user_data/config.json \
  --strategy MyStrategy

# FreqAI付きトレード
freqtrade trade \
  --config user_data/config.json \
  --strategy MyFreqAIStrategy \
  --freqaimodel LightGBMRegressor
```

### IStrategy 基本構造
```python
from freqtrade.strategy import IStrategy, IntParameter
from pandas import DataFrame
import talib.abstract as ta

class MyStrategy(IStrategy):
    minimal_roi = {"60": 0.01, "30": 0.02, "0": 0.04}
    stoploss = -0.10
    timeframe = "1h"
    trailing_stop = True
    trailing_stop_positive = 0.02

    # Hyperoptパラメータ空間
    buy_rsi = IntParameter(20, 40, default=30, space="buy")
    sell_rsi = IntParameter(60, 80, default=70, space="sell")

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe["rsi"] = ta.RSI(dataframe, timeperiod=14)
        dataframe["ema20"] = ta.EMA(dataframe, timeperiod=20)
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (dataframe["rsi"] < self.buy_rsi.value) &
            (dataframe["close"] > dataframe["ema20"]) &
            (dataframe["volume"] > 0),
            "enter_long",
        ] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (dataframe["rsi"] > self.sell_rsi.value),
            "exit_long",
        ] = 1
        return dataframe
```

### @informative による複数時間足・クロスペア注入
```python
from freqtrade.strategy import informative

class MultiTFStrategy(IStrategy):
    timeframe = "1h"

    @informative("4h")
    def populate_indicators_4h(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe["rsi"] = ta.RSI(dataframe, timeperiod=14)
        return dataframe
        # → メイン足で rsi_4h として参照可能

    @informative("1d", "BTC/USDT")
    def populate_indicators_btc_1d(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe["ema50"] = ta.EMA(dataframe, timeperiod=50)
        return dataframe
        # → メイン足で ema50_BTC_USDT_1d として参照可能
```

### FreqAI 戦略実装
```python
class MyFreqAIStrategy(IStrategy):
    timeframe = "5m"

    def feature_engineering_expand_all(
        self, dataframe: DataFrame, period: int, metadata: dict, **kwargs
    ) -> DataFrame:
        # %-プレフィックスで特徴量を定義（periodは自動展開される）
        dataframe["%-rsi"] = ta.RSI(dataframe, timeperiod=period)
        dataframe["%-ema"] = ta.EMA(dataframe, timeperiod=period)
        return dataframe

    def set_freqai_targets(self, dataframe: DataFrame, metadata: dict, **kwargs) -> DataFrame:
        # &-プレフィックスでターゲットを定義
        dataframe["&-price_change"] = (
            dataframe["close"].shift(-self.freqai_info["feature_parameters"]["label_period_candles"])
            / dataframe["close"] - 1
        )
        return dataframe

    def populate_entry_trend(self, df: DataFrame, metadata: dict) -> DataFrame:
        df.loc[df["&-price_change"] > 0.01, "enter_long"] = 1
        return df
```

### カスタムコールバック
```python
class AdvancedStrategy(IStrategy):
    def custom_stoploss(
        self, pair: str, trade, current_time, current_rate: float,
        current_profit: float, after_fill: bool, **kwargs
    ) -> float:
        # 利益2%超でブレークイーブンに移動
        if current_profit > 0.02:
            return -0.001
        return self.stoploss

    def confirm_trade_entry(
        self, pair: str, order_type: str, amount: float, rate: float,
        time_in_force: str, current_time, entry_tag, side: str, **kwargs
    ) -> bool:
        # 直近足のボリュームが20本平均より高い場合のみエントリー
        df, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        last_candle = df.iloc[-1]
        avg_volume = df["volume"].tail(20).mean()
        return last_candle["volume"] > avg_volume * 1.5

    def custom_exit(
        self, pair: str, trade, current_time, current_rate: float,
        current_profit: float, **kwargs
    ) -> str | bool:
        # 24時間以上保持した場合に強制エグジット
        if (current_time - trade.open_date_utc).total_seconds() > 86400:
            return "timeout_exit"
        return False
```

### config.json 主要設定
```json
{
  "max_open_trades": 5,
  "stake_currency": "USDT",
  "stake_amount": 100,
  "dry_run": true,
  "dry_run_wallet": 1000,
  "exchange": {
    "name": "binance",
    "key": "",
    "secret": ""
  },
  "pairlists": [
    {"method": "VolumePairList", "number_assets": 20, "sort_key": "quoteVolume"},
    {"method": "AgeFilter", "min_days_listed": 10},
    {"method": "SpreadFilter", "max_spread_ratio": 0.005}
  ],
  "telegram": {
    "enabled": true,
    "token": "YOUR_TOKEN",
    "chat_id": "YOUR_CHAT_ID"
  }
}
```

### FreqAI設定（config.jsonに追加）
```json
{
  "freqai": {
    "enabled": true,
    "model_training_parameters": {"n_estimators": 1000},
    "feature_parameters": {
      "include_timeframes": ["5m", "1h"],
      "include_corr_pairlist": ["BTC/USDT", "ETH/USDT"],
      "label_period_candles": 24,
      "indicator_periods_candles": [10, 20, 50]
    },
    "data_split_parameters": {"test_size": 0.33},
    "train_period_days": 30,
    "backtest_period_days": 7
  }
}
```

## ワークフロー例

### 1. 新規戦略の開発からライブ運用まで

1. **初期化**: `freqtrade new-config` → `freqtrade new-strategy --strategy MyStrategy`
2. **データ取得**: `freqtrade download-data --exchange binance --pairs BTC/USDT ETH/USDT --timeframes 1h 4h --days 365`
3. **戦略実装**: `populate_indicators` → `populate_entry_trend` → `populate_exit_trend` の順に実装
4. **バックテスト（インサンプル）**: `freqtrade backtesting --timerange 20230101-20230630`
5. **Hyperopt**: `freqtrade hyperopt --hyperopt-loss SharpeHyperOptLoss --epochs 200 --spaces buy sell roi stoploss`
6. **アウトオブサンプル検証**: `freqtrade backtesting --timerange 20230701-20231231`（過学習チェック）
7. **Dry-Run**: `freqtrade trade --dry-run` で数日〜数週間の実環境シミュレーション
8. **ライブ移行**: `dry_run: false` に変更、APIキー設定、Telegram通知有効化

### 2. FreqAI機械学習パイプライン

1. **戦略生成**: `freqtrade new-strategy --strategy MLStrategy --template freqai`
2. **特徴量定義**: `feature_engineering_expand_all` で `%-` プレフィックス付き特徴量を実装
3. **ターゲット定義**: `set_freqai_targets` で `&-` プレフィックス付き予測対象を実装
4. **FreqAI設定**: config.jsonに `freqai` セクションを追加（`train_period_days`, `indicator_periods_candles` 等）
5. **バックテスト**: `freqtrade backtesting --freqaimodel LightGBMRegressor`（スライディングウィンドウで自動再学習）
6. **ライブ運用**: モデルは `train_period_days` 間隔で自動再学習される

### 3. 既存戦略のパフォーマンス改善

1. **現状分析**: バックテスト結果から勝率・平均利益・最大ドローダウンを確認
2. **ボトルネック特定**: 負けトレードのパターン分析（`--export trades` の結果を精査）
3. **フィルタ追加**: `confirm_trade_entry` でボリュームフィルタや時間帯フィルタを実装
4. **ストップロス改善**: `custom_stoploss` でトレーリングストップやブレークイーブンを実装
5. **再バックテスト**: 改善前後の比較、アウトオブサンプル期間での検証

## 注意点

- **`populate_*` メソッドはベクトル演算のみ**: これらのメソッド内でループや外部API呼び出しを行うとバックテストが極端に遅くなる。pandasのベクトル演算とTA-Libを使うこと
- **`volume > 0` ガードは必須**: エントリー/エグジット条件に `(dataframe["volume"] > 0)` を含めないと、ボリュームゼロの足でシグナルが出てバックテストと実運用で乖離する
- **Hyperoptの過学習に注意**: インサンプル期間でのみ最適化し、必ずアウトオブサンプル期間でWalk-Forward検証を行うこと。`--timerange` を分けて使う
- **`IntParameter` / `DecimalParameter` のimport忘れ**: Hyperoptパラメータを使う場合は `from freqtrade.strategy import IntParameter, DecimalParameter` を忘れずにimportする
- **FreqAI特徴量の命名規則**: 特徴量は `%-` プレフィックス、ターゲットは `&-` プレフィックスが必須。これを守らないとFreqAIが認識しない
- **`@informative` のカラム命名**: `{indicator}_{timeframe}` の形式で自動リネームされる。カスタムペアの場合は `{indicator}_{pair}_{timeframe}`。メイン足で参照するときは命名規則を把握しておくこと
- **Dry-Runとライブの差異**: Dry-Runではスリッページ・部分約定・レート遅延が再現されない。Dry-Runで利益が出てもライブで同等の成績は保証されない
- **`self.dp.get_analyzed_dataframe()` は直近データのみ**: コールバック内で過去の分析済みデータフレームにアクセスする際、返されるのは直近の分析結果のみ。長期的な統計が必要な場合は `populate_indicators` 内で事前計算すること
- **REST APIのエンドポイント変更**: v2以降 `forcebuy` → `forceentry`、`forcesell` → `forceexit` に変更されている
- **config.jsonにAPIキーをハードコードしない**: 環境変数 `__env:KEY_NAME` または `--config` で別ファイルに分離すること

## 関連スキル

- **ccxt**: 取引所APIの直接操作、カスタムオーダータイプ、Freqtrade非対応の取引所機能へのアクセス
- **cli**: Freqtradeのプロセス管理、systemdサービス化、Docker環境での運用
- **n8n / n8n-as-code**: Freqtradeのwebhook通知を起点にした自動化ワークフロー構築
```

---

**主な改善点:**

| 基準 | 元 | 改善後 |
|---|---|---|
| **descriptionのトリガー精度** | 汎用的で具体的API名が不足 | `populate_indicators`・`custom_stoploss`・`@informative` 等の具体的API名を列挙し、トリガー精度を向上 |
| **500行以下** | 368行（ただし末尾切れ） | ~390行で完結。config.jsonを圧縮、REST API例を削除（注意点でv2変更を記載） |
| **コマンド例** | コピペ可能だが一部冗長 | `--strategy-list` による複数戦略比較、configからのペアリスト一括DLを追加 |
| **ワークフロー例** | 1例のみ（2例目が切れている） | 3例に拡充（新規開発→ライブ / FreqAIパイプライン / パフォーマンス改善） |
| **注意点** | セクション自体が欠落 | 10項目のハマりポイントを追加（ベクトル演算制約、命名規則、過学習、API変更等） |
| **関連スキル** | セクション自体が欠落 | ccxt・cli・n8nの3スキルを用途付きで追加 |
| **バグ修正** | `confirm_trade_entry` で単一行に `.mean()` | `df["volume"].tail(20).mean()` に修正。`custom_exit` コールバック例も追加 |
