改善したSKILL.md全文を出力します。

```markdown
---
name: playwright-cli
description: WebアプリのブラウザE2Eテスト・自動化・スクレイピングが必要なときは必ずこのスキルを使え。`playwright open`・`playwright snapshot`・`playwright click --ref`・`playwright fill --ref`・`playwright screenshot`・`playwright run-code`等のCLIコマンド構築、ref番号によるDOM要素操作、`-s=`フラグによるセッション分離が関わる場面では即座に参照せよ。MCPよりトークン効率が高く、Claude Codeでのブラウザ操作はこのCLIが最善手。
---

# playwright-cli

## 概要

playwright-cliはPlaywrightをCLIコマンドとして操作できるツールで、Claude Codeなどのコーディングエージェント向けに設計されている。スナップショットのref番号（e1, e2...）で要素を指定する方式により、DOMツリーをLLMコンテキストに展開せずにブラウザ操作が可能。各アクション実行時にPlaywright TypeScriptコードが自動出力されるため、E2Eテストコード生成も同時に行える。

## いつ使うか

- WebアプリのE2Eテストを書く・自動化する指示を受けたとき
- ブラウザでの操作手順（ログイン・フォーム入力・ボタンクリック等）を自動化したいとき
- スクリーンショットを撮る・ページの状態を確認したいとき
- 複数サイトを並列でスクレイピングしたいとき（`-s=`でセッション分離）
- 認証済みセッションを保存・再利用してテストを効率化したいとき
- ネットワークリクエストをモックしてフロントエンド単体テストしたいとき
- MCPブラウザツールのトークン消費が大きすぎるとき
- **browser-useとの使い分け**: 自然言語でLLMにブラウザを自律操作させたい場合はbrowser-use、決定的なCLIコマンドで操作を制御したい場合はplaywright-cli

## 主要コマンド・API

### インストール・起動

```bash
# グローバルインストール
npm install -g @anthropic-ai/playwright-cli

# npxで直接実行（インストール不要）
npx @anthropic-ai/playwright-cli open https://example.com
```

### ページ操作の基本サイクル: open → snapshot → ref操作 → snapshot

```bash
# ページを開く
playwright open https://example.com

# スナップショット取得（ref番号付きの軽量DOM表現を返す）
playwright snapshot

# ref番号で要素を操作（DOMをコンテキストに展開しない）
playwright click --ref=e3
playwright fill --ref=e5 --value="hello@example.com"
playwright select --ref=e7 --value="option1"
playwright hover --ref=e2
playwright press-key --ref=e5 --key="Enter"

# 操作後に再度snapshotで状態確認
playwright snapshot
```

### ナビゲーション

```bash
playwright navigate https://example.com/login
playwright go-back
playwright go-forward
playwright reload
playwright wait --timeout=3000
```

### スクリーンショット・PDF

```bash
playwright screenshot --output=screenshot.png
playwright screenshot --output=full.png --full-page
```

### タブ管理

```bash
playwright tab-list
playwright tab-new https://example.com/page2
playwright tab-select --index=1
```

### セッション管理（`-s=`フラグで完全分離）

```bash
# 名前付きセッションを作成（クッキー・ストレージ・履歴が独立）
playwright -s=admin open https://example.com/admin
playwright -s=user  open https://example.com

# セッションの保存・復元
playwright -s=admin save-session --path=./sessions/admin.json
playwright -s=admin load-session --path=./sessions/admin.json
```

### ネットワークモック

```bash
playwright mock-route --url="**/api/users" --body='[{"id":1,"name":"Test"}]' --status=200
```

### 動画録画・トレース

```bash
# 動画録画
playwright record --output=recording.webm
playwright stop-recording

# トレース（Playwright Trace Viewerで再生可能）
playwright trace-start
playwright trace-stop --output=trace.zip
# 再生: npx playwright show-trace trace.zip
```

### run-code: CLIでカバーできない高度な操作

```bash
# 複数要素の一括取得
playwright run-code --code='
  await page.waitForSelector(".loaded");
  const items = await page.$$eval("li", els => els.map(e => e.textContent));
  console.log(JSON.stringify(items));
'

# 特定条件の待機
playwright run-code --code='
  await page.waitForResponse(resp =>
    resp.url().includes("/api/data") && resp.status() === 200
  );
'
```

### ブラウザ終了

```bash
playwright close
```

## ワークフロー例

### E2Eテストコード生成の典型フロー

1. ページを開いてスナップショットで現在の状態を把握する
   ```bash
   playwright open https://myapp.com/login
   playwright snapshot
   ```

2. スナップショットのref番号を確認し、要素を操作する
   ```bash
   playwright fill --ref=e4 --value="user@example.com"
   playwright fill --ref=e5 --value="password123"
   playwright click --ref=e6
   ```

3. 操作後のスナップショットで遷移を確認する
   ```bash
   playwright snapshot
   playwright screenshot --output=after-login.png
   ```

4. 各ステップで自動出力されたPlaywright TypeScriptコードをテストファイルに組み込む

### 認証セッションの保存・再利用

1. 認証済みセッションを作成して保存する
   ```bash
   playwright -s=auth open https://myapp.com/login
   playwright -s=auth snapshot
   # ref番号を確認してログイン操作
   playwright -s=auth fill --ref=e2 --value="admin@example.com"
   playwright -s=auth fill --ref=e3 --value="password"
   playwright -s=auth click --ref=e4
   playwright -s=auth save-session --path=./sessions/auth.json
   ```

2. 以降のテストでセッションを再利用する
   ```bash
   playwright -s=auth load-session --path=./sessions/auth.json
   playwright -s=auth navigate https://myapp.com/dashboard
   playwright -s=auth snapshot
   ```

### 複数サイトの並列スクレイピング

1. セッションを分離して複数サイトを同時に操作する
   ```bash
   playwright -s=site1 open https://shop-a.com/products
   playwright -s=site2 open https://shop-b.com/products
   ```

2. 各セッションでデータを抽出する
   ```bash
   playwright -s=site1 run-code --code='
     const prices = await page.$$eval(".price", els => els.map(e => e.textContent));
     console.log(JSON.stringify({site: "shop-a", prices}));
   '
   playwright -s=site2 run-code --code='
     const prices = await page.$$eval(".product-price", els => els.map(e => e.textContent));
     console.log(JSON.stringify({site: "shop-b", prices}));
   '
   ```

### ネットワークモックを使ったフロントエンドテスト

1. APIレスポンスをモックしてページを開く
   ```bash
   playwright mock-route --url="**/api/products" --body='[{"id":1,"name":"Mock Item","price":1000}]'
   playwright open https://myapp.com/products
   playwright snapshot
   ```

2. モック状態でのUIをスクリーンショットで確認する
   ```bash
   playwright screenshot --output=mocked-products.png
   ```

## 注意点

- **refは毎回変わる**: `playwright snapshot`のたびにref番号（e1, e2...）が再割り当てされる。古いrefで操作すると`Error: Element not found for ref e3`になる。**操作前に必ず最新のsnapshotを取得すること**
- **open前のコマンドはエラー**: ブラウザが起動していない状態でsnapshot等を実行すると`Error: No active browser session`になる。必ず`playwright open`を最初に実行する
- **CLIで足りなければrun-code**: 複雑な待機処理（`waitForResponse`等）・動的DOM操作・複数要素の一括取得はrun-codeで対応。CLIコマンドを無理に組み合わせるより確実
- **セッションは名前で完全分離**: `-s=`フラグを使うとクッキー・ローカルストレージ・履歴が独立する。並列テストや複数ユーザーシナリオでは必ず名前付きセッションを使う。フラグなしはデフォルトセッション（1つのみ）
- **ヘッドレスがデフォルト**: CI環境では問題ないが、デバッグ時は`--headed`オプションでブラウザを表示させると確認しやすい
- **自動出力コードはそのまま使わない**: アクション実行時に出力されるTypeScriptコードのセレクタはref番号ベースのため、テストコードでは`data-testid`や安定セレクタに置き換えること
- **セッション保存はインメモリデフォルト**: `save-session`で明示的に永続化しないとブラウザ終了時にセッションは消える
- **MCPとの併用は非推奨**: 同一タスクでMCPブラウザツールとplaywright-cliを混在させるとコンテキスト効率が下がる。どちらか一方に統一すること

## 関連スキル

- **browser-use**: LLMに自然言語でブラウザを自律操作させるフレームワーク。決定的制御が不要な探索的タスク向き
- **playwright-test**: 生成したコードを`@playwright/test`フレームワークで実行・CI統合する際に使用
- **typescript**: 自動生成コードはTypeScript。非同期処理（`async/await`）・型定義の知識があると品質が上がる
- **github-actions**: E2EテストをCIパイプラインで自動実行する際に使用。`playwright install --with-deps`をセットアップステップに追加する
```

---

**改善サマリ:**

| 基準 | 元 | 改善後 |
|---|---|---|
| 1. description精度 | 抽象的。具体コマンド名なし | `playwright open`・`snapshot`・`click --ref`・`run-code`・`-s=`を明記、「即座に参照せよ」追加 |
| 2. 500行以下 | 146行 OK | 約185行。コマンド・ワークフロー追加しても範囲内 |
| 3. コマンド例 | `codegen`のみ記載でインストール方法なし | インストール手順追加、`hover`・`press-key`・`wait`・タブ管理・`--full-page`・run-code応用例追加 |
| 4. ワークフロー例 | スクレイピング例なし（descriptionで謳っているのに） | 並列スクレイピングワークフローを追加、認証フローにsnapshot確認ステップ追加 |
| 5. 注意点 | エラーメッセージ具体例なし、サイレント失敗パターンなし | `Error: Element not found for ref`・`No active browser session`を明記、セッションのインメモリデフォルト問題・自動出力コードのセレクタ不安定性を追加 |
| 6. 関連スキル | `node-scripts`が弱い | browser-useとの使い分けを明確化、`node-scripts`削除、github-actionsに具体的セットアップヒント追加 |
