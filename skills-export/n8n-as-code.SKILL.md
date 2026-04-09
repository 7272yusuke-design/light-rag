改善版SKILL.md全文を出力します。

---

```markdown
---
name: n8n-as-code
description: n8nワークフローをコード（TypeScript/JSON）でGit管理するとき、`n8nac` CLI（init/pull/push/sync/diff）を使うとき、`@Workflow`/`@Node`デコレータでワークフローを記述・生成するとき、ローカルとn8nインスタンスを3-wayマージ同期するとき、AIエージェントからMCPサーバー経由でn8nノードスキーマを検索・ワークフローを生成するときに必ず使用すること。
---

# n8n-as-code

## 概要
n8n-as-code（n8nac）は、n8nワークフローをTypeScript/JSONとしてバージョン管理し、ローカルとn8nインスタンス間で3-wayマージ同期を行うツールキット。CLI・VSCode拡張・MCPサーバー・AIスキルライブラリのモノレポ構成で、GitOpsとAI支援開発の両方をサポートする。

## いつ使うか
- `n8nac` コマンド（init/pull/push/sync/diff/list/reset）の使い方を聞かれたとき
- `@Workflow`/`@Node` デコレータでワークフローをTypeScriptで記述・生成するとき
- ローカルとリモートのワークフローを同期・マージするとき
- CI/CDパイプラインにn8nワークフローのデプロイを組み込みたいとき
- AIエージェントからMCPサーバー経由でn8nノードスキーマを検索するとき
- `@n8n-as-code/transformer` でTS→JSON変換するとき

## 主要コマンド・API

### インストール
```bash
npm install -g @n8n-as-code/cli
# または npx で直接実行
npx @n8n-as-code/cli init
```

### CLIコマンド（n8nac）
```bash
# プロジェクト初期化（n8nac.config.json + .n8n-state.json を生成）
n8nac init

# リモートのワークフロー一覧を表示
n8nac list

# リモート → ローカルへ全ワークフローを取得
n8nac pull

# 特定ワークフローのみ取得
n8nac pull abc123

# ローカル → リモートへ送信
n8nac push

# 3-wayマージによる双方向同期（競合を自動検出）
n8nac sync

# 競合解決後に同期を完了
n8nac sync --resolved

# ワークフローの差分を確認
n8nac diff abc123

# 状態ファイルのリセット（同期状態を初期化）
n8nac reset
```

### 設定ファイル（n8nac.config.json）
```json
{
  "instanceUrl": "https://your-n8n.example.com",
  "apiKey": "${N8N_API_KEY}",
  "workflowDir": "./workflows",
  "stateFile": ".n8n-state.json"
}
```

### TypeScriptデコレータによるワークフロー定義
```typescript
import { Workflow, Node, NodeOutput } from '@n8n-as-code/transformer';

@Workflow({ name: 'Fetch and Notify', active: false })
export class FetchAndNotify {
  @Node({
    type: 'n8n-nodes-base.httpRequest',
    position: [250, 300],
    parameters: { url: 'https://api.example.com/data', method: 'GET' },
  })
  fetchData!: NodeOutput;

  @Node({
    type: 'n8n-nodes-base.slack',
    position: [450, 300],
    parameters: {
      channel: '#notifications',
      text: '={{ $json.body }}',
    },
  })
  notifySlack!: NodeOutput;
}
```

### TS→JSONコンパイル
```bash
# TypeScriptデコレータ記法をn8n JSONに変換
npx @n8n-as-code/transformer compile workflows/fetch-and-notify.ts -o workflows/
```

### MCPサーバー起動
```bash
# AIエージェントからノードスキーマを検索可能にする
npx @n8n-as-code/skills mcp-serve --port 3100
```

### ノードスキーマ検索（プログラマティック）
```typescript
import { NodeSchemaSearch } from '@n8n-as-code/skills';

const results = await NodeSchemaSearch.search('http request');
// → [{ type: 'n8n-nodes-base.httpRequest', parameters: [...], ... }]
```

## ワークフロー例

### 1. GitOps同期フロー（ゼロから本番デプロイまで）
```bash
# 1. 初期化
export N8N_API_KEY="your-api-key"
n8nac init
# n8nac.config.json の instanceUrl を設定

# 2. 既存ワークフローをローカルに取得
n8nac pull
ls workflows/  # JSON/TSファイルが生成される

# 3. ローカルで編集後、差分を確認
n8nac diff

# 4. リモートに反映
n8nac push

# 5. 状態ファイルごとGitにコミット
git add workflows/ .n8n-state.json
git commit -m "feat: update workflow"
```

### 2. AIエージェントによるワークフロー生成
1. MCPサーバーを起動: `npx @n8n-as-code/skills mcp-serve --port 3100`
2. AIに「HTTPでデータ取得→Slackに通知するワークフロー」を指示
3. AIがノードスキーマを参照しながら `@Workflow`/`@Node` デコレータのTSコードを生成
4. コンパイル: `npx @n8n-as-code/transformer compile workflows/my-flow.ts -o workflows/`
5. デプロイ: `n8nac push`

### 3. 競合解決フロー
```bash
# syncが競合を検出（localHash/remoteHash/lastSyncedHashの3点比較）
n8nac sync
# → CONFLICT: workflows/abc123.json

# 競合ファイルを手動編集して解決
vim workflows/abc123.json

# 解決を確定して同期完了
n8nac sync --resolved
```

## 注意点
- **`.n8n-state.json` は必ずGitにコミットする**。3-wayマージのベース状態を保持しており、欠損すると全ワークフローが競合扱いになる
- **APIキーは環境変数で管理する**。`n8nac.config.json` には `${N8N_API_KEY}` と書き、直接APIキーを記載しない
- **デコレータTSはそのままpushできない**。必ず `@n8n-as-code/transformer compile` でJSONに変換してからpushすること
- **syncの並列実行は禁止**。StateManagerがファイルロックを取るため、複数プロセスから同時に `n8nac sync` を実行するとデータ破損の可能性がある
- **初回pullは全ワークフローを取得する**。大量のワークフローがある場合は `n8nac pull <workflowId>` で個別に取得する
- **n8nインスタンスのバージョンとスキーマの互換性**。`@n8n-as-code/skills` のノードスキーマはn8nバージョンに依存するため、インスタンスのバージョンを確認すること

## 関連スキル
- **n8n**: n8nワークフローエディタ自体の操作・ノード設定
- **cli**: `gws` などCLIツールとn8nacを組み合わせたワークスペース自動化
- **mcp**: MCPサーバーをAIエージェントのツールとして統合する場合
```

---

**主な改善点:**

| 基準 | 元の問題 | 改善 |
|---|---|---|
| 1. description精度 | 汎用的で具体的コマンド名なし | `n8nac` CLI名、`@Workflow`/`@Node`、MCPサーバーなど具体的トリガーキーワードを列挙 |
| 2. 行数 | 128行（問題なし） | 130行程度を維持 |
| 3. コマンド例 | インストール方法・コンパイルコマンド・MCP起動が欠落 | `npm install`、`transformer compile`、`mcp-serve` を追加。全コマンドがコピペ可能 |
| 4. ワークフロー例 | 手順が説明文のみでコマンドなし | GitOps/競合解決フローを実際のシェルコマンドブロックに変換 |
| 5. 注意点 | VSCode版揃え・prerelease等の低優先度項目が混在 | 実害の大きいハマりポイント（state欠損→全競合、TS直push不可、並列sync破損）に絞り込み |
| 6. 関連スキル | typescript/gitops/conventional-commits/monorepo等の汎用スキルが多すぎ | リポ内に存在する実スキル（n8n, cli, mcp）に限定 |
