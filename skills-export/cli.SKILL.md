```markdown
---
name: cli
description: "gws"コマンドでGoogle Workspace API（Gmail, Drive, Calendar, Sheets, Docs, Chat）をCLI操作する必要があるとき、またはAIエージェント・シェルスクリプトからWorkspace自動化を実行するときに必ずこのスキルを使え。`gws gmail`・`gws drive`・`gws calendar`・`gws sheets`等のコマンド構築、`--page-all`によるページネーション処理、`--dry-run`による書き込みプレビューが関わる場面では即座に参照せよ。
---

# cli (gws)

## 概要
gwsはRust製CLIツールで、Google APIのDiscovery Documentをランタイムに取得し、全Google Workspace APIのサブコマンドを動的に生成する。Gmail・Drive・Calendar・Sheets・Docs・Chatを単一バイナリで統一的に操作でき、NDJSON自動ページネーション・型安全スキーマ検証・dry-runプレビュー・マルチAPIワークフローをサポートする。AIエージェントからの呼び出しを前提に設計されており、全入力値に対する敵対的入力バリデーションが組み込まれている。

## いつ使うか
- Gmail・Drive・Calendar・Sheets・Docs・ChatなどGoogle Workspace APIをCLIから呼び出す指示を受けたとき
- メールトリアージ・会議準備・週次レポートなどWorkspace定型業務を自動化するとき
- AIエージェントとしてWorkspaceデータの読み書き・集計・通知を実行するとき
- CI/CDパイプラインやシェルスクリプトにWorkspace操作を組み込むとき
- `--page-all`の出力を`jq`でパイプライン処理するとき
- 書き込み操作を`--dry-run`でスキーマ検証してから実行したいとき

## 主要コマンド・API

### 認証・サービス確認

```bash
# OAuth2認証（ブラウザが開く）
gws auth login

# 認証状態とスコープの確認
gws auth status

# 利用可能なAPIサービス一覧
gws services list
```

### Gmail

```bash
# 未読メール一覧（自動ページネーション、上限50件）
gws gmail users.messages.list --userId me --q "is:unread" \
  --maxResults 50 --page-all | jq '.messages[]'

# メール詳細取得
gws gmail users.messages.get --userId me --id "<MSG_ID>" \
  | jq '{subject: .payload.headers[] | select(.name=="Subject") | .value, from: .payload.headers[] | select(.name=="From") | .value}'

# ラベル付与（dry-runで確認→本番実行）
gws gmail users.messages.modify --userId me --id "<MSG_ID>" --dry-run \
  --body '{"addLabelIds": ["IMPORTANT"]}'
gws gmail users.messages.modify --userId me --id "<MSG_ID>" \
  --body '{"addLabelIds": ["IMPORTANT"]}'

# ヘルパー: メールトリアージ（内部で複数API呼び出し）
gws gmail +triage --max-messages 20
```

### Calendar

```bash
# 今日のアジェンダ（ヘルパーコマンド）
gws calendar +agenda --date today

# 期間指定でイベント一覧
gws calendar events.list \
  --calendarId primary \
  --timeMin "2024-01-15T00:00:00Z" \
  --timeMax "2024-01-21T23:59:59Z" \
  --maxResults 100 \
  --page-all | jq '[.items[] | {summary, start: .start.dateTime}]'

# イベント作成（dry-runでプレビュー）
gws calendar events.insert --calendarId primary --dry-run \
  --body '{"summary":"Weekly Sync","start":{"dateTime":"2024-01-22T10:00:00+09:00"},"end":{"dateTime":"2024-01-22T11:00:00+09:00"}}'
```

### Drive

```bash
# PDF検索
gws drive files.list \
  --q "name contains 'report' and mimeType='application/pdf'" \
  --maxResults 20 --page-all | jq '.files[] | {id, name, webViewLink}'

# フォルダ内のファイル一覧
gws drive files.list \
  --q "'<FOLDER_ID>' in parents" \
  --page-all | jq '.files[] | {name, mimeType}'
```

### Sheets

```bash
# セル範囲の読み取り
gws sheets spreadsheets.values.get \
  --spreadsheetId "<SHEET_ID>" \
  --range "Sheet1!A1:D10" | jq '.values[]'

# セル範囲への書き込み（dry-run→本番）
gws sheets spreadsheets.values.update \
  --spreadsheetId "<SHEET_ID>" \
  --range "Sheet1!A1" \
  --valueInputOption USER_ENTERED \
  --dry-run \
  --body '{"values": [["Name","Score","Date"],["Alice",95,"2024-01-20"]]}'
```

### Docs

```bash
# ドキュメント本文取得
gws docs documents.get --documentId "<DOC_ID>" \
  | jq '.body.content'
```

### ワークフロー・ペルソナ

```bash
# 組み込みワークフロー
gws workflow standup-report
gws workflow meeting-prep --event-id "<EVENT_ID>"
gws workflow weekly-digest --week 2024-W03

# スキル・ペルソナ一覧
gws skills list
gws personas list

# レシピ実行
gws recipe run executive-assistant-morning
```

## ワークフロー例

### 典型例1: 受信メールのトリアージとラベリング

```bash
# 1. 認証確認
gws auth status

# 2. 未読メールIDを取得（上限100件）
gws gmail users.messages.list --userId me --q "is:unread" \
  --maxResults 100 --page-all | jq -r '.messages[].id' > unread_ids.txt

# 3. ヘルパーでトリアージ（優先度判定・分類）
gws gmail +triage --max-messages 50

# 4. 特定メールにラベル付与（dry-run確認後に実行）
MSG_ID="18d5a3b2c4e6f789"
gws gmail users.messages.modify --userId me --id "$MSG_ID" --dry-run \
  --body '{"addLabelIds": ["IMPORTANT"]}'
# 確認後、--dry-runを外して実行
gws gmail users.messages.modify --userId me --id "$MSG_ID" \
  --body '{"addLabelIds": ["IMPORTANT"]}'
```

### 典型例2: 週次レポート生成とSheets書き込み

```bash
# 1. ワークフローでデータ収集
gws workflow weekly-digest --week 2024-W03 > digest.json

# 2. Calendarから週のイベント数を集計
EVENT_COUNT=$(gws calendar events.list --calendarId primary \
  --timeMin "2024-01-15T00:00:00Z" \
  --timeMax "2024-01-21T23:59:59Z" \
  --page-all | jq '[.items[]] | length')

# 3. Gmailから週の受信数を集計
EMAIL_COUNT=$(gws gmail users.messages.list --userId me \
  --q "after:2024/01/15 before:2024/01/21" \
  --page-all | jq '.messages | length')

# 4. Sheetsに書き込み（dry-run→本番）
gws sheets spreadsheets.values.update \
  --spreadsheetId "<SHEET_ID>" \
  --range "WeeklyReport!A2" \
  --valueInputOption USER_ENTERED \
  --dry-run \
  --body "{\"values\": [[\"2024-W03\", $EVENT_COUNT, $EMAIL_COUNT]]}"

# 5. dry-run結果を確認後、本番実行
gws sheets spreadsheets.values.update \
  --spreadsheetId "<SHEET_ID>" \
  --range "WeeklyReport!A2" \
  --valueInputOption USER_ENTERED \
  --body "{\"values\": [[\"2024-W03\", $EVENT_COUNT, $EMAIL_COUNT]]}"
```

### 典型例3: AIエージェントによる会議準備

```bash
# 1. 明日のイベントからIDとタイトルを取得
gws calendar +agenda --date tomorrow \
  | jq '.events[] | {id, summary, start: .start.dateTime}'

# 2. 特定イベントの会議準備ワークフロー実行
gws workflow meeting-prep --event-id "<EVENT_ID>"

# 3. 会議トピックに関連するDriveファイルを検索
gws drive files.list \
  --q "name contains 'Q1 Planning' and modifiedTime > '2024-01-01T00:00:00'" \
  --maxResults 10 --page-all \
  | jq '.files[] | {name, webViewLink}'

# 4. 議事録用の新規Docsを用意（既存テンプレートをコピー）
gws drive files.copy --fileId "<TEMPLATE_DOC_ID>" \
  --body '{"name": "Meeting Notes - Q1 Planning 2024-01-22"}'
```

## 注意点
- **初回起動の遅延**: Discovery Documentのフェッチに数秒かかる。キャッシュは24時間有効で、自動リフレッシュされる。`gws services list`で事前にキャッシュを温められる
- **書き込みは必ず`--dry-run`→本番の2段階**: dry-runはスキーマ検証のみでAPIを呼ばない。特にSheets/Calendar/Gmailの変更操作は必ずプレビューしてから実行すること
- **`--page-all`と`--maxResults`の併用**: `--page-all`は全ページをNDJSONでストリームするため、大量データでは`--maxResults`で上限を設定するか、`jq`で逐次処理すること。上限なしで数万件をメモリに載せるとOOMリスクがある
- **ヘルパーコマンド（`+verb`）の制約**: 内部で複数APIを呼び出すため、`--dry-run`が使えない場合がある。副作用の有無はヘルパーごとに確認すること
- **OAuth2スコープ不足は403**: 操作に必要なスコープが認証時に付与されていないと403になる。`gws auth status`でスコープを確認し、不足時は`gws auth login`で再認証する
- **レート制限（429）は自動リトライ**: 指数バックオフで自動リトライされるが、バッチ処理でループ内から大量呼び出しする場合は`sleep 1`を挟むことを推奨
- **入力バリデーション**: パストラバーサル・制御文字・Bidi Unicode・ゼロ幅文字・URLインジェクションは自動拒否される。「不正な入力」エラーが出たら引数の特殊文字を確認すること。なお環境変数は信頼済みとして扱われバリデーション対象外
- **ペルソナ/レシピの追加**: カスタム定義はTOML/Markdownのレジストリファイル形式に従う。`gws skills list`で既存フォーマットを参考にすること

## 関連スキル
- **jq**: `--page-all`のNDJSON出力のフィルタリング・集計・変換に必須。gwsのほぼ全コマンドの出力パイプ先
- **cli-anything**: GUIアプリをCLIハーネスでラップする手法。gwsと同じくAIエージェントからのCLI制御パターンを共有
- **n8n / n8n-as-code**: gwsコマンドをノードとして組み込んだビジュアルワークフロー自動化
- **crewai / langgraph**: gwsをツールとして呼び出すマルチエージェントフレームワーク（function calling経由）
```
