改善版SKILL.md全文:

```markdown
---
name: ccxt
description: ccxtライブラリを使った暗号通貨取引所APIの統合・マルチ取引所対応・市場データ取得・注文操作の実装を求められたら必ずこのスキルを使え。取引所APIの直接呼び出しやWebSocketストリーミングが絡む場合は特に優先すること。Freqtrade等の上位フレームワークではなく、取引所API層を直接操作する場合に適用。
---

# ccxt

## 概要
CCXTは100以上の暗号通貨取引所に対応した統一APIライブラリで、TypeScript/JavaScript・Python・C#・Go向けに実装されている。REST APIとWebSocket（ccxt.pro）の両方をサポートし、取引所ごとのAPI差異を抽象化した共通インターフェースを提供する。取引所の認証・署名・レート制限・シンボル正規化を内部で処理するため、マルチ取引所対応システムを効率的に構築できる。

## いつ使うか
- 暗号通貨取引所のAPIを叩いて価格・板情報・残高・注文を操作したいとき
- 複数取引所を横断してアービトラージや価格比較を行いたいとき
- WebSocketでリアルタイムのティッカー・オーダーブック・約定をストリーミングしたいとき
- 市場データ収集パイプラインやバックテスト用OHLCV取得を実装するとき
- 取引所APIの認証・署名・レート制限を自前実装せずに済ませたいとき
- ポートフォリオ管理・残高集約ツールを構築するとき

## 主要コマンド・API

### インストール
```bash
# Python（proも含む）
pip install ccxt

# TypeScript/JavaScript（proも含む）
npm install ccxt
```

### 基本的なREST API（Python）
```python
import ccxt

# 取引所インスタンス生成
exchange = ccxt.binance({
    'apiKey': 'YOUR_API_KEY',
    'secret': 'YOUR_SECRET',
    'enableRateLimit': True,  # 必須: レート制限を有効化
})

# 対応取引所一覧
print(ccxt.exchanges)  # ['ace', 'alpaca', 'binance', ...]

# マーケット情報のロード（起動時に一度だけ呼ぶ）
markets = exchange.load_markets()

# ティッカー取得
ticker = exchange.fetch_ticker('BTC/USDT')
print(ticker['last'], ticker['bid'], ticker['ask'])

# オーダーブック取得
orderbook = exchange.fetch_order_book('BTC/USDT', limit=20)
print(orderbook['bids'][:5])  # [[price, amount], ...]

# OHLCVデータ取得
ohlcv = exchange.fetch_ohlcv('BTC/USDT', timeframe='1h', limit=100)
# [[timestamp, open, high, low, close, volume], ...]

# 残高確認（認証必須）
balance = exchange.fetch_balance()
print(balance['BTC']['free'], balance['USDT']['total'])

# 注文量・価格を取引所の精度に丸める（必須）
amount = exchange.amount_to_precision('BTC/USDT', 0.00123456)
price = exchange.price_to_precision('BTC/USDT', 50123.456789)

# 成行注文
order = exchange.create_order('BTC/USDT', 'market', 'buy', amount)

# 指値注文
order = exchange.create_order('BTC/USDT', 'limit', 'sell', amount, price)

# 注文キャンセル
exchange.cancel_order(order['id'], 'BTC/USDT')

# 未決済注文一覧
open_orders = exchange.fetch_open_orders('BTC/USDT')

# 約定履歴
trades = exchange.fetch_my_trades('BTC/USDT', limit=50)
```

### TypeScript/JavaScript
```typescript
import ccxt from 'ccxt';

const exchange = new ccxt.bybit({
    apiKey: process.env.API_KEY,
    secret: process.env.SECRET,
    enableRateLimit: true,
});

await exchange.loadMarkets();
const ticker = await exchange.fetchTicker('ETH/USDT');
const balance = await exchange.fetchBalance();

// 精度を丸めてから注文
const amount = exchange.amountToPrecision('ETH/USDT', 1.23456);
const order = await exchange.createOrder('ETH/USDT', 'limit', 'buy', amount, 2000);
```

### 取引所の機能チェック
```python
# 取引所がサポートする機能を事前確認
if exchange.has['fetchOHLCV']:
    ohlcv = exchange.fetch_ohlcv('BTC/USDT', '1h')

if exchange.has['createMarketOrder']:
    order = exchange.create_order('BTC/USDT', 'market', 'buy', 0.001)

if exchange.has['watchTicker']:  # WebSocket対応チェック
    print('WebSocket ticker supported')

# 対応タイムフレーム一覧
print(exchange.timeframes)  # {'1m': '1m', '5m': '5m', '1h': '1h', ...}
```

### ccxt.pro WebSocket（Python）
```python
import ccxt.pro as ccxtpro
import asyncio

async def watch_ticker(exchange, symbol):
    while True:
        ticker = await exchange.watch_ticker(symbol)
        print(f"{symbol}: {ticker['last']}")

async def watch_orderbook(exchange, symbol):
    while True:
        ob = await exchange.watch_order_book(symbol)
        print(f"best bid: {ob['bids'][0]}, best ask: {ob['asks'][0]}")

async def main():
    exchange = ccxtpro.binance({'enableRateLimit': True})
    try:
        # 複数ストリームを並列起動
        await asyncio.gather(
            watch_ticker(exchange, 'BTC/USDT'),
            watch_orderbook(exchange, 'ETH/USDT'),
        )
    finally:
        await exchange.close()

asyncio.run(main())
```

### ccxt.pro WebSocket（TypeScript）
```typescript
import ccxt from 'ccxt';

async function watchMultipleExchanges() {
    const exchanges = [new ccxt.pro.binance(), new ccxt.pro.bybit()];
    try {
        await Promise.all(
            exchanges.map(async (ex) => {
                while (true) {
                    const ticker = await ex.watchTicker('BTC/USDT');
                    console.log(ex.id, ticker['last']);
                }
            })
        );
    } finally {
        await Promise.all(exchanges.map(ex => ex.close()));
    }
}
```

### エラーハンドリング
```python
try:
    order = exchange.create_order('BTC/USDT', 'limit', 'buy', 0.001, 50000)
except ccxt.InsufficientFunds as e:
    print('残高不足:', e)
except ccxt.InvalidOrder as e:
    print('不正な注文（最小数量未満等）:', e)
except ccxt.AuthenticationError as e:
    print('認証エラー: APIキー/権限を確認:', e)
except ccxt.RateLimitExceeded as e:
    print('レート制限超過: 待機後リトライ:', e)
except ccxt.NetworkError as e:
    # タイムアウト・接続断 → リトライ可能
    print('ネットワークエラー:', e)
except ccxt.ExchangeError as e:
    # 取引所側のエラー → リトライ不可の場合が多い
    print('取引所エラー:', e)
```

### 高精度数値演算（Precise）
```python
from ccxt.base.precise import Precise

a = Precise('0.1')
b = Precise('0.2')
print(str(a + b))  # '0.3'（浮動小数点誤差なし）
```

### サンドボックス・テストネット
```python
exchange = ccxt.binance({
    'apiKey': 'TESTNET_KEY',
    'secret': 'TESTNET_SECRET',
})
exchange.set_sandbox_mode(True)  # テストネットに切り替え
# 注意: 全取引所がサンドボックスに対応しているわけではない
```

### OHLCVのページネーション取得
```python
all_ohlcv = []
since = exchange.parse8601('2024-01-01T00:00:00Z')

while True:
    ohlcv = exchange.fetch_ohlcv('BTC/USDT', '1h', since=since, limit=1000)
    if not ohlcv:
        break
    all_ohlcv.extend(ohlcv)
    since = ohlcv[-1][0] + 1  # 最後のタイムスタンプ+1ms
    # enableRateLimitが有効なら明示的なsleep不要
```

## ワークフロー例

### 1. マルチ取引所アービトラージ監視
```python
import ccxt
import asyncio

async def fetch_prices(exchange_ids, symbol):
    exchanges = [getattr(ccxt, eid)({'enableRateLimit': True}) for eid in exchange_ids]
    for ex in exchanges:
        await ex.load_markets()

    while True:
        tasks = [ex.fetch_ticker(symbol) for ex in exchanges]
        tickers = await asyncio.gather(*tasks, return_exceptions=True)

        prices = {}
        for ex, t in zip(exchanges, tickers):
            if not isinstance(t, Exception):
                prices[ex.id] = {'bid': t['bid'], 'ask': t['ask']}

        # スプレッド検出
        if len(prices) >= 2:
            best_bid = max(prices.items(), key=lambda x: x[1]['bid'])
            best_ask = min(prices.items(), key=lambda x: x[1]['ask'])
            spread = best_bid[1]['bid'] - best_ask[1]['ask']
            if spread > 0:
                print(f"機会: {best_ask[0]}で買い→{best_bid[0]}で売り, 差額={spread}")

        await asyncio.sleep(5)
```

### 2. WebSocketリアルタイムデータ収集
1. `ccxt.pro`で取引所インスタンスを生成（`enableRateLimit: True`）
2. `asyncio.gather()`で複数シンボルの`watch_order_book()`を並列起動
3. 受信データをRedis/PostgreSQL/Kafkaへ書き込み（ccxtがオーダーブック差分を自動適用）
4. `try/finally`で`exchange.close()`を確実に実行

### 3. 取引ボットの基本構造
1. 設定ファイルからAPIキー・取引所・シンボル・戦略パラメータを読み込み
2. `load_markets()`でマーケット情報をキャッシュ、`exchange.markets[symbol]`で最小注文量等を確認
3. メインループで`fetch_ohlcv()`（REST）または`watch_ohlcv()`（WebSocket）でデータ取得
4. 戦略ロジックでシグナル判定 → `amount_to_precision()`で精度調整 → `create_order()`で発注
5. `ccxt.NetworkError`はリトライ、`ccxt.ExchangeError`はアラート通知
6. 高度なボットフレームワークが必要な場合はFreqtrade（ccxtを内部利用）を検討

## 注意点
- **`enableRateLimit: True`は必須**: 省略すると取引所BANのリスクがある。本番では必ず有効化
- **注文量・価格の精度**: `amount_to_precision()` / `price_to_precision()`で丸めてから発注。未丸めだと`InvalidOrder`エラー
- **浮動小数点演算の回避**: 注文金額の計算には`Precise`クラスまたは`Decimal`を使用。`float`演算は誤差が蓄積する
- **`has`プロパティで機能確認**: 全取引所が全メソッドに対応しているわけではない。`exchange.has['fetchOHLCV']`等で事前チェック
- **シンボル表記**: ccxtは`BTC/USDT`形式。先物は`BTC/USDT:USDT`、オプションは`BTC/USD:BTC-240101-50000-C`形式
- **`load_markets()`のキャッシュ**: 起動時に一度だけ呼ぶ。長時間運用では`exchange.load_markets(True)`で明示的リロード
- **OHLCVのページネーション**: `limit`は一度に取得できる本数の上限。大量取得時は`since`でループが必要
- **WebSocketの再接続**: ccxt.proは自動再接続するが、長時間運用では`try/except`でラップしてループ継続させること
- **APIキーの権限管理**: 読み取り専用・取引許可・出金許可を用途に応じて最小権限で設定
- **テストネット**: `set_sandbox_mode(True)`で切り替え可能だが、対応取引所は限られる
- **マスターソースはTypeScript**: コントリビュート時はTS側を編集し、トランスパイラで他言語変換（Python等を直接編集しない）
- **非同期の統一**: Python版はasyncio、JS版はPromise/async-await。同期メソッドはイベントループ内で使うとブロックするため避ける
- **取引所固有パラメータ**: `params`引数で取引所固有オプションを渡せるが、移植性が下がるため最小限に

## 関連スキル
- **freqtrade**: ccxtを内部利用する取引ボットフレームワーク。IStrategy・バックテスト・Hyperoptが必要ならこちら
- **pandas / numpy**: OHLCVデータの分析・テクニカル指標計算
- **asyncio**: ccxt.proのWebSocket処理やREST並列リクエストの非同期基盤
- **Redis**: リアルタイム市場データのキャッシュ・Pub/Subによるプロセス間データ共有
- **PostgreSQL / TimescaleDB**: 時系列市場データの永続化・バックテスト用データストア
- **Docker**: 取引ボットのコンテナ化・マルチ取引所ボットの並列デプロイ
- **TA-Lib / pandas-ta**: テクニカル指標（MA・RSI・MACD等）の計算ライブラリ
```

---

**改善点のサマリ:**

| 基準 | 元 | 改善後 |
|------|-----|--------|
| 1. descriptionのトリガー精度 | freqtradeとの境界が曖昧 | 「取引所API層を直接操作する場合」「Freqtrade等の上位フレームワークではなく」と明確に差別化 |
| 2. 500行以下 | 238行 (OK) | ~250行 (OK) |
| 3. コマンド例の具体性 | `amount_to_precision`欠落、`has`チェック欠落 | 精度丸め・機能チェック・ページネーション取得を追加 |
| 4. ワークフロー例 | テキストのみの箇条書き | ワークフロー1にコピペ可能な実装コードを追加 |
| 5. 注意点 | 主要なハマりポイント3つ欠落 | `amount_to_precision`必須、`has`チェック、先物/オプションのシンボル形式、OHLCVページネーションを追加 |
| 6. 関連スキル | freqtrade欠落 | freqtradeを筆頭に追加し、棲み分けを明記 |

**最大の修正**: WebSocket Python例の致命的バグ（複数の`while True`が直列で書かれ、2つ目以降到達不可能）を`asyncio.gather`による並列起動パターンに修正。
