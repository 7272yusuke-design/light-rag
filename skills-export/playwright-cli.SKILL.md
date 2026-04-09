---
name: playwright-cli
description: WebアプリのE2Eテスト・ブラウザ自動化・スクレイピングが必要なときは必ずこのスキルを使え。MCPよりトークン効率が高く、Claude Codeでのブラウザ操作はplaywrigh-cli経由が第一選択肢。
---

# playwright-cli

## 概要

playwright-cliはPlaywrightをCLIコマンドとして操作できるツールで、Claude Codeなどのコーディングエージェント向けに設計されている。ブラウザ自動化・テスト生成・ネットワークモック・セッション管理・動画録画などの豊富な操作を、MCPと比較してコンテキストウィンドウを大幅に節約しながら実行できる。各操作に対応するPlaywright TypeScriptコードが自動出力されるため、テストコードの生成も同時に行える。

## いつ使うか

- WebアプリのE2Eテストを書きたい・自動化したいと言われたとき
- ブラウザでの操作手順を記録してテストコードに変換したいとき
- ログイン状態を保存して再利用するテストシナリオが必要なとき
- 複数サイトを並列でスクレイピング・操作したいとき
- ネットワークリクエストをモックしてフロントエンドをテストしたいとき
- 「ブラウザで〇〇を確認して」「このページをスクリーンショットして」と言われたとき
- Playwrightのテストコードを一から書くより先に、動作確認しながら生成したいとき

## 主要コマンド・API

```bash
# インストール
npm install -g @playwright-cli/cli

# ページを開いてスナップショット取得（要素のrefを確認）
playwright-cli open https://example.com
playwright-cli snapshot

# refを使って要素を操作（DOM全体をコンテキストに展開しない）
playwright-cli click --ref=e1
playwright-cli fill --ref=e3 --value="hello@example.com"
playwright-cli select --ref=e5 --value="option1"

# スクリーンショット
playwright-cli screenshot --path=./screenshot.png

# 名前付きセッションで独立したブラウザコンテキストを使う
playwright-cli -s=admin open https://example.com/admin
playwright-cli -s=user  open https://example.com

# 認証状態の保存・復元
playwright-cli -s=myapp save-session --path=./session.json
playwright-cli -s=myapp load-session --path=./session.json

# ネットワークモック
playwright-cli mock-route --url="**/api/users" --body='[{"id":1}]' --status=200

# 任意のPlaywright TypeScriptコードを実行（escape hatch）
playwright-cli run-code --file=./custom.ts

# 動画録画
playwright-cli -s=rec record --path=./video.webm
playwright-cli -s=rec stop-record

# トレース取得
playwright-cli trace start
playwright-cli trace stop --path=./trace.zip

# テストコード生成（実行済みアクションから）
playwright-cli codegen --output=./tests/e2e.spec.ts
```

## ワークフロー例

### E2Eテストコードを生成する

1. セッションを開始してターゲットページを開く
   ```bash
   playwright-cli -s=mytest open https://myapp.example.com/login
   ```
2. スナップショットで操作対象のrefを確認する
   ```bash
   playwright-cli -s=mytest snapshot
   # → e1: input[name=email], e2: input[name=password], e3: button[type=submit]
   ```
3. refを使って操作を実行（各操作のTypeScriptコードが自動出力される）
   ```bash
   playwright-cli -s=mytest fill --ref=e1 --value="user@example.com"
   playwright-cli -s=mytest fill --ref=e2 --value="password123"
   playwright-cli -s=mytest click --ref=e3
   ```
4. ログイン後の状態をセッションに保存する
   ```bash
   playwright-cli -s=mytest save-session --path=./auth.json
   ```
5. 自動出力されたコードをテストファイルに書き出す
   ```bash
   playwright-cli -s=mytest codegen --output=./tests/login.spec.ts
   ```

### 並列スクレイピング

1. 複数の名前付きセッションで同時にページを開く
   ```bash
   playwright-cli -s=site1 open https://site1.example.com &
   playwright-cli -s=site2 open https://site2.example.com &
   ```
2. 各セッションで独立してスナップショット・操作を行う
   ```bash
   playwright-cli -s=site1 snapshot
   playwright-cli -s=site2 snapshot
   ```

### APIモックを使ったフロントエンドテスト

1. モックルートを設定してからページを開く
   ```bash
   playwright-cli -s=mock mock-route --url="**/api/products" \
     --body='[{"id":1,"name":"Mock Product"}]' --status=200
   playwright-cli -s=mock open https://myapp.example.com/products
   ```
2. モックデータで描画されたUIをスナップショット・操作する
   ```bash
   playwright-cli -s=mock snapshot
   playwright-cli -s=mock screenshot --path=./products-mocked.png
   ```

## 注意点

- **refは揮発性**: スナップショット取得のたびにrefが変わる可能性がある。操作直前に必ずsnapshotを取り直してrefを確認すること
- **セッション名の衝突**: `-s=`を省略するとデフォルトセッションが使われる。並列操作時は必ず異なるセッション名を付けること
- **run-codeは最終手段**: CLIコマンドで対応できない高度なシナリオのみrun-codeを使う。通常操作はCLIコマンドで行いトークン効率を維持すること
- **save-sessionの機密情報**: セッションファイルにはCookieや認証トークンが含まれる。`.gitignore`に追加し、リポジトリにコミットしないこと
- **headlessモードのデフォルト**: デフォルトはheadlessで動作する。デバッグ時は`--headed`フラグを付けること
- **Playwright依存バージョン**: `scripts/update.js`でSKILL.mdとREADMEが同期される。手動でSKILL.mdを編集した場合はスクリプトを再実行すること

## 関連スキル

- **playwright** (公式ライブラリ): run-codeで任意のPlaywright APIを直接呼び出す際に参照する
- **typescript**: codegenで生成されたテストコードの編集・カスタマイズに使用
- **jest / vitest**: 生成したPlaywrightテストコードを組み込むテストランナー
- **github-actions**: 生成したE2EテストをCI/CDパイプラインで自動実行する際に組み合わせる
- **mcp-browser**: playwright-cliでカバーできない場合の代替手段（ただしトークン消費が多い）