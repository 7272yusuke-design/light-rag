---
source: https://github.com/ccxt/ccxt
category: framework
sub_categories: [protocol, tool]
tags: [typescript, python, csharp, golang, cryptocurrency, exchange-api, websocket, trading]
language: 
ingested: 2026-04-09
source_updated: unknown
status: active
---

# ccxt

# ccxt

## 基本情報
- リポジトリ: https://github.com/ccxt/ccxt
- カテゴリ: framework
- サブカテゴリ: protocol, tool
- タグ: typescript, python, csharp, golang, cryptocurrency, exchange-api, websocket, trading
- 最終確認日: 2026-04-09

## 概要
CCXTは100以上の暗号通貨取引所に対応した統一APIライブラリで、TypeScript/JavaScript、Python、C#、Go言語向けに実装されています。REST APIとWebSocket（ccxt.pro）の両方をサポートし、取引所ごとの差異を抽象化した共通インターフェースを提供します。

## 設計思想
取引所ごとに異なるAPIを統一インターフェースで抽象化するラッパーパターンを採用。各取引所クラスは基底Exchangeクラスを継承し、fetchTicker/fetchOrderBook/createOrder等の標準メソッドを実装する。TypeScriptをマスター実装として、Python・C#・Goへのトランスパイルで多言語対応を実現。WebSocket向けにはPromise/Future、OrderBook差分更新等の非同期パターンを統一化。

## 主要コンポーネント
- Exchange基底クラス: 全取引所共通の認証・署名・レート制限・エラーハンドリングロジックを提供するベースクラス
- 取引所実装クラス群: 100以上の各取引所固有APIをラップし、標準インターフェースにマッピング
- ccxt.pro (WebSocket層): watchTicker/watchOrderBook/watchTrades等のストリーミングAPIをWebSocketで実装
- Precise: 浮動小数点誤差を回避するための高精度数値演算クラス
- OrderBook/OrderBookSide: 増分更新対応のオーダーブック管理データ構造
- 静的暗号ライブラリ: ECDSA(secp256k1)、EIP712、StarkCurve等の署名処理をネイティブ実装

## 実装パターン
- 取引所ラッパーパターン: 各取引所をabstract/api/exchanges/wrappers層に分割し、メタデータ定義とロジック実装を分離
- トランスパイル多言語対応: TypeScriptをマスターソースとしてPython・C#・Goへ自動変換することで保守コストを削減
- レート制限スロットリング: 取引所ごとのレート制限をThrottlerクラスでローリングウィンドウ管理
- 増分オーダーブック更新: WebSocketで受信した差分データをローカルオーダーブックに適用するキャッシュ管理パターン
- 統一エラー階層: NetworkError/AuthenticationError/InsufficientFunds等の標準例外クラス体系で取引所非依存なエラーハンドリング

## 適用シーン
暗号通貨取引ボット・アービトラージシステム・ポートフォリオ管理ツール・市場データ収集パイプライン・マルチ取引所対応のトレーディングプラットフォーム構築に最適。特に複数取引所を横断して操作したい場合や、取引所APIの差異を意識せずに開発したいプロジェクトに有用。

## 注意点・制約
各取引所のAPI仕様変更に追従する必要があり、実装の完全性は取引所によって異なる。WebSocket機能(ccxt.pro)は別ライセンス(有償)の場合がある。トランスパイル生成コードのため、言語固有の最適化は限定的。分散型取引所(DEX)のサポートは一部のみ。


## 関連ナレッジ
- (なし)
