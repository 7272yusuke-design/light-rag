```markdown
---
name: n8n-mcp
description: n8nワークフローの生成・ノード検索・JSON検証・自動修正・テンプレート活用を行うときに必ずこのスキルを使え。search_nodes・get_node_info・validate_workflow・fix_workflow・search_templates・create_workflow・execute_workflowなどMCPツール経由のn8n操作が含まれる場合は即座に参照せよ。
---

# n8n-mcp

## 概要
n8n-MCPはModel Context Protocol (MCP) サーバーとして動作し、AIアシスタントにn8nの525以上のワークフロー自動化ノードへの構造化アクセスを提供する。ノード検索・スキーマ取得・ワークフロー検証/修正・テンプレート検索・CRUD操作をMCPツールとして公開し、SQLite FTS5による高速全文検索とバリデーションエンジンによってAI生成ワークフローの精度を大幅に向上させる。

## いつ使うか
- n8nワークフローをゼロから生成・設計するとき
- 特定のユースケースに適したn8nノードを`search_nodes`で探すとき
- `get_node_info`でノードの必須パラメータ・認証方式・スキーマを確認するとき
- 既存のワークフローJSONを`validate_workflow`で検証するとき
- バリデーションエラーを`fix_workflow`で自動修正するとき
- `search_templates`でコミュニティテンプレートを検索・再利用するとき
- `create_workflow`/`execute_workflow`でn8nインスタンスへデプロイ・実行するとき
- Claude DesktopやClaude CodeからMCP経由でn8nを操作する設定を行うとき

## 主要コマンド・API

### サーバー起動
```bash
# stdio モード（Claude Desktop / Claude Code向け）
npx n8n-mcp

# HTTP シングルセッションモード
N8N_MCP_MODE=http npx n8n-mcp

# HTTP マルチテナントモード（複数クライアント同時接続）
N8N_MCP_MODE=http-multi npx n8n-mcp

# Docker（HTTPモード）
docker run -e N8N_MCP_MODE=http -p 3000:3000 ghcr.io/n8n-mcp/n8n-mcp
```

### Claude Desktop 設定 (claude_desktop_config.json)
```json
{
  "mcpServers": {
    "n8n-mcp": {
      "command": "npx",
      "args": ["n8n-mcp"],
      "env": {
        "N8N_API_URL": "http://localhost:5678",
        "N8N_API_KEY": "your-api-key"
      }
    }
  }
}
```

### Claude Code 設定 (.mcp.json)
```json
{
  "mcpServers": {
    "n8n-mcp": {
      "command": "npx",
      "args": ["n8n-mcp"],
      "env": {
        "N8N_API_URL": "http://localhost:5678",
        "N8N_API_KEY": "your-api-key"
      }
    }
  }
}
```

### ノード検索
```typescript
// キーワードでノードを検索（OR: いずれかにマッチ）
await mcp.call("search_nodes", {
  query: "HTTP request webhook",
  mode: "OR",
  limit: 10
});
// → [{ nodeType: "n8n-nodes-base.httpRequest", ... }, { nodeType: "n8n-nodes-base.webhook", ... }]

// 複数キーワードすべてにマッチ（結果を絞り込む）
await mcp.call("search_nodes", {
  query: "slack send message",
  mode: "AND",
  limit: 5
});

// タイポ許容検索
await mcp.call("search_nodes", {
  query: "schedul trigr",
  mode: "FUZZY",
  limit: 5
});
```

### ノード詳細取得
```typescript
// ノードの全パラメータ・認証方式・入出力スキーマを取得
await mcp.call("get_node_info", {
  nodeType: "n8n-nodes-base.httpRequest"
});
// → { displayName, description, properties: [...], credentials: [...], inputs, outputs }
```

### ワークフロー検証・修正
```typescript
// AI生成ワークフローの検証（通常はai-friendlyプロファイルを使用）
const result = await mcp.call("validate_workflow", {
  workflow: workflowJson,
  profile: "ai-friendly"  // minimal | ai-friendly | strict
});
// → { valid: false, errors: [{ nodeId: "...", message: "Missing required param: channel" }] }

// エラーを自動修正
const fixed = await mcp.call("fix_workflow", {
  workflow: workflowJson
});
// → { workflow: { ...修正済みJSON }, changes: ["Added missing channel param to Slack node"] }
```

### テンプレート検索
```typescript
// コミュニティテンプレートからユースケースに近いワークフローを検索
await mcp.call("search_templates", {
  query: "Slack notification on new GitHub issue",
  limit: 5
});
// → [{ id, name, description, nodes: [...], workflow: {...} }]
```

### ワークフローCRUD・実行
```typescript
// n8nインスタンスにワークフローを作成（N8N_API_KEY必須）
const created = await mcp.call("create_workflow", {
  workflow: workflowJson
});
// → { id: "wf_abc123", name: "Daily Slack Report", active: false }

// ワークフローを手動実行
await mcp.call("execute_workflow", {
  workflowId: "wf_abc123"
});

// 既存ワークフロー一覧取得
await mcp.call("list_workflows", {});

// ワークフロー更新
await mcp.call("update_workflow", {
  workflowId: "wf_abc123",
  workflow: updatedWorkflowJson
});
```

### 環境変数
```bash
N8N_API_URL=http://localhost:5678   # n8nインスタンスURL
N8N_API_KEY=your-api-key            # n8n APIキー（CRUD・実行に必須）
N8N_MCP_MODE=stdio                  # stdio | http | http-multi
PORT=3000                           # HTTPモード時のポート
TELEMETRY_ENABLED=false             # テレメトリ無効化
```

## ワークフロー例

### AI支援によるワークフロー生成フロー（定時Slack通知）
1. 要件からノードを検索する
   ```
   search_nodes("schedule trigger") → n8n-nodes-base.scheduleTrigger を特定
   search_nodes("slack send message") → n8n-nodes-base.slack を特定
   ```
2. 各ノードのスキーマ・必須パラメータを取得する
   ```
   get_node_info("n8n-nodes-base.scheduleTrigger") → rule: { interval, cronExpression }
   get_node_info("n8n-nodes-base.slack") → authentication: oAuth2, params: { channel, text }
   ```
3. コミュニティテンプレートで類似例を参照する
   ```
   search_templates("daily slack report") → テンプレートのノード構成・接続パターンを確認
   ```
4. ノードスキーマに基づいてワークフローJSONを構築する（ノード間接続・パラメータ・認証設定を含む）
5. バリデーションを実行する
   ```
   validate_workflow(workflowJson, profile="ai-friendly") → エラー0件を確認
   ```
6. n8nインスタンスにデプロイして動作確認する
   ```
   create_workflow(workflowJson) → wf_abc123
   execute_workflow("wf_abc123") → 実行結果を確認
   ```

### 既存ワークフローのデバッグ・修正フロー
1. n8nで実行エラーが出ているワークフローJSONを取得する
2. `validate_workflow`で`strict`プロファイルを使い、全エラーを網羅的に洗い出す
   ```
   validate_workflow(brokenJson, profile="strict") → エラー3件検出
   ```
3. `fix_workflow`で自動修正を試みる
   ```
   fix_workflow(brokenJson) → 2件自動修正、1件は手動対応が必要
   ```
4. 手動対応が必要なエラーは`get_node_info`で正しいパラメータを確認して修正する
5. 再度`validate_workflow`を実行してエラー0件を確認する
6. `update_workflow`で修正済みJSONをn8nに反映する

### テンプレートベースの高速ワークフロー構築
1. ユースケースに近いテンプレートを検索する
   ```
   search_templates("webhook to Google Sheets") → テンプレート候補を取得
   ```
2. テンプレートのワークフローJSONをベースにノード設定をカスタマイズする
3. カスタマイズ後のJSONを`validate_workflow`で検証する
4. `create_workflow`でデプロイし、Webhookをテスト送信して動作確認する

## 注意点
- **バリデーションプロファイルの使い分け**: `strict`はAI生成ワークフローで誤検知が多い。生成時は`ai-friendly`を使い、最終チェック・デバッグ時のみ`strict`を使うこと。`minimal`は接続の基本チェックのみで検証が甘すぎる
- **FTS5検索モードの選択順序**: まず`OR`で広く検索し、結果が多すぎる場合に`AND`で絞り込む。`FUZZY`はタイポ許容だが無関係なノードもヒットするため、正確なノード名が分かっている場合は`AND`を優先すること
- **N8N_API_KEY未設定時の制限**: APIキーがないと`search_nodes`・`get_node_info`・`validate_workflow`・`search_templates`は使えるが、`create_workflow`・`execute_workflow`・`update_workflow`等のCRUD操作は全てエラーになる。エラーメッセージに認証情報不足と出る
- **コミュニティノードの初回取得**: 組み込みノード（`n8n-nodes-base.*`）以外はnpmから動的フェッチするため初回アクセスに数秒〜数十秒かかる。オフライン環境では組み込みノードのみ利用可能
- **SQLiteデータの永続化**: ノードリポジトリ・テンプレートキャッシュ・ワークフロー差分履歴はSQLiteファイルに保存される。Dockerで運用する場合、ボリュームマウントしないとコンテナ再起動で全データが消失する
- **HTTP マルチテナントモードの認証**: `http-multi`モードではセッション管理が必須。認証設定とセッションタイムアウト（デフォルト30分）を明示的に構成しないと、セッションリークやメモリ肥大の原因になる
- **テレメトリのデフォルト有効**: デフォルトで匿名テレメトリが送信される。機密環境・エアギャップ環境では`TELEMETRY_ENABLED=false`を必ず設定すること
- **n8n本体のバージョン互換**: n8n v1.0以上が必要。v0.x系のワークフローJSONはノードタイプ名やパラメータ構造が異なるため、`validate_workflow`でエラーになる場合がある

## 関連スキル
- **n8n**: デプロイ先のワークフローエンジン本体。ノードの実行環境・認証情報（Credentials）管理・Webhook設定はn8n側で行う
- **docker**: n8nとn8n-MCPを同一Dockerネットワークで運用する場合の構成管理。SQLiteボリュームマウント設定を含む
- **typescript-mcp-sdk**: n8n-MCPにカスタムツールを追加する場合の`@modelcontextprotocol/sdk`による拡張実装
- **ai**: Vercel AI SDKの`experimental_createMCPClient`でn8n-MCPをLLMエージェントのツールとして接続する場合
- **cli**: Claude DesktopやClaude Codeでのstdio MCP接続設定・デバッグ全般
```
