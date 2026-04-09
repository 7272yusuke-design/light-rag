```markdown
---
name: servers
description: MCPサーバーを新規開発する際の`McpServer`・`server.tool()`・`server.resource()`・`server.prompt()`の実装パターン、`StdioServerTransport`・`SSEServerTransport`・`StreamableHTTPServerTransport`の3トランスポート接続、`claude_desktop_config.json`へのサーバー登録、既存MCPサーバーのデバッグを行うときに必ずこのスキルを参照せよ。`@modelcontextprotocol/sdk`・`mcp-server-git`・`mcp-server-fetch`・`mcp-server-filesystem`など公式リファレンス実装の構造とベストプラクティスを網羅している。
---

# servers

## 概要
公式のModel Context Protocol (MCP) リファレンスサーバー実装集。filesystem・git・fetch・memory・sequentialthinkingなどの実用サーバーと、MCPの全機能を網羅したデモサーバー「everything」を含む。STDIO・SSE・Streamable HTTPの3トランスポートに対応し、LLMクライアント（Claude Desktop・Claude Code等）とのツール・リソース・プロンプト連携の正規実装パターンを提供する。

## いつ使うか
- `McpServer`を使って新規MCPサーバーをゼロから実装するとき
- `server.tool()`・`server.resource()`・`server.prompt()`の登録方法やzodスキーマ定義の確認
- `StdioServerTransport` / `SSEServerTransport` / `StreamableHTTPServerTransport` の接続実装
- `getClientCapabilities()`によるelicitation・samplingの条件付きツール登録
- `oninitialized`・`onclose`ハンドラのライフサイクル管理
- `claude_desktop_config.json`へのMCPサーバー登録・接続トラブルシューティング
- `mcp-server-git`・`mcp-server-fetch`・`mcp-server-filesystem`の起動・設定
- MCPプロトコル準拠のデバッグ（everythingサーバーとの比較検証）
- LLMエージェントにファイルシステム・Git・Web取得機能をMCP経由で付与したいとき

## 主要コマンド・API

### サーバーのビルド・起動（TypeScript系）
```bash
# 依存インストール＆ビルド
cd src/everything   # または filesystem / memory / sequentialthinking
npm install
npm run build

# STDIOモードで起動
node dist/index.js

# SSEモードで起動（ポート指定）
node dist/index.js --port 3001

# Streamable HTTPモードで起動
node dist/index.js --transport streamable-http --port 3001
```

### サーバーのビルド・起動（Python系: git / fetch）
```bash
# uvxで分離環境実行（推奨）
uvx mcp-server-git --repository /path/to/repo
uvx mcp-server-fetch

# pipインストール後に起動
pip install mcp-server-git
python -m mcp_server_git --repository /path/to/repo
```

### Server Factory Pattern（新規サーバーの基本構造）
```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";

export function createServer(): { server: McpServer; cleanup: () => void } {
  const server = new McpServer({
    name: "my-server",
    version: "1.0.0",
  });

  // ツール登録: 第2引数=説明, 第3引数=zodスキーマ, 第4引数=ハンドラ
  server.tool(
    "my_tool",
    "ツールの説明（LLMが読むので具体的に書く）",
    {
      input: z.string().describe("入力パラメータの説明"),
      count: z.number().optional().describe("オプション引数"),
    },
    async ({ input, count }) => ({
      content: [{ type: "text", text: `結果: ${input}` }],
    })
  );

  // リソース登録: URIテンプレート + ハンドラ
  server.resource(
    "myapp://data/{id}",
    new ResourceTemplate("myapp://data/{id}", { list: undefined }),
    async (uri, { id }) => ({
      contents: [{ uri: uri.href, text: `Data for ${id}`, mimeType: "text/plain" }],
    })
  );

  // プロンプト登録
  server.prompt(
    "my_prompt",
    "プロンプトの説明",
    { query: z.string() },
    ({ query }) => ({
      messages: [{ role: "user", content: { type: "text", text: query } }],
    })
  );

  const cleanup = () => { /* インターバル・接続のクリーンアップ */ };
  return { server, cleanup };
}
```

### Conditional Tool Registration（ケーパビリティ確認後の遅延登録）
```typescript
// McpServerの内部Serverインスタンスにアクセスしてハンドラを設定
server.server.oninitialized = () => {
  const capabilities = server.server.getClientCapabilities();

  if (capabilities?.elicitation) {
    server.tool("interactive_config", "ユーザーに設定値を確認する", {}, async () => {
      const result = await server.server.elicit({
        message: "APIキーを入力してください",
        requestedSchema: { type: "object", properties: { apiKey: { type: "string" } } },
      });
      return { content: [{ type: "text", text: `設定完了: ${result.content.apiKey}` }] };
    });
  }

  if (capabilities?.sampling) {
    server.tool("summarize_with_llm", "LLMを使って要約する", {
      text: z.string(),
    }, async ({ text }) => {
      const result = await server.server.createMessage({
        messages: [{ role: "user", content: { type: "text", text: `要約: ${text}` } }],
        maxTokens: 500,
      });
      return { content: [result.content] };
    });
  }
};
```

### Multi-transport 接続（Express.js）
```typescript
import express from "express";
import { randomUUID } from "crypto";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { SSEServerTransport } from "@modelcontextprotocol/sdk/server/sse.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";

// STDIO（CLIやClaude Desktopから利用）
const { server, cleanup } = createServer();
const transport = new StdioServerTransport();
await server.connect(transport);

// SSE（ブラウザ・リモートクライアント向け）
const app = express();
const sseTransports = new Map<string, SSEServerTransport>();
app.get("/sse", async (req, res) => {
  const { server } = createServer();
  const transport = new SSEServerTransport("/messages", res);
  sseTransports.set(transport.sessionId, transport);
  await server.connect(transport);
});
app.post("/messages", async (req, res) => {
  const sessionId = req.query.sessionId as string;
  const transport = sseTransports.get(sessionId);
  if (!transport) return res.status(404).send("Session not found");
  await transport.handlePostMessage(req, res);
});

// Streamable HTTP（最新推奨プロトコル）
app.post("/mcp", async (req, res) => {
  const { server } = createServer();
  const transport = new StreamableHTTPServerTransport({
    sessionIdGenerator: () => randomUUID(),
  });
  await server.connect(transport);
  await transport.handleRequest(req, res, req.body);
});

app.listen(3001, () => console.error("MCP server on port 3001"));
```

### Progress通知付きツール（長時間処理）
```typescript
server.tool(
  "long_task",
  "時間のかかる処理を実行する",
  { steps: z.number().default(10) },
  async ({ steps }, { sendNotification }) => {
    for (let i = 0; i < steps; i++) {
      await doWork(i);
      await sendNotification({
        method: "notifications/progress",
        params: { progress: i + 1, total: steps, progressToken: `step-${i}` },
      });
    }
    return { content: [{ type: "text", text: `${steps}ステップ完了` }] };
  }
);
```

### Claude Desktop / Claude Code への登録
```json
// claude_desktop_config.json
{
  "mcpServers": {
    "everything": {
      "command": "node",
      "args": ["/path/to/servers/src/everything/dist/index.js"]
    },
    "filesystem": {
      "command": "node",
      "args": ["/path/to/servers/src/filesystem/dist/index.js", "/allowed/path"]
    },
    "git": {
      "command": "uvx",
      "args": ["mcp-server-git", "--repository", "/path/to/repo"]
    },
    "fetch": {
      "command": "uvx",
      "args": ["mcp-server-fetch"]
    }
  }
}
```
```json
// Claude Code: .mcp.json（プロジェクトルート）
{
  "mcpServers": {
    "my-server": {
      "command": "node",
      "args": ["./dist/index.js"],
      "env": { "API_KEY": "..." }
    }
  }
}
```

## ワークフロー例

### 新規MCPサーバーをゼロから作る
1. `npm init -y && npm install @modelcontextprotocol/sdk zod`
2. `src/everything/src/index.ts` を参照してServer Factoryパターンを把握
3. `createServer()` 関数にツール・リソース・プロンプトを登録（上記パターン参照）
4. `tsconfig.json` に `"module": "NodeNext"`, `"moduleResolution": "NodeNext"` を設定
5. `npx tsc && node dist/index.js` でSTDIOモード起動、MCP Inspectorで動作確認
6. `claude_desktop_config.json` または `.mcp.json` に登録してE2Eテスト
7. 必要に応じて `oninitialized` で条件付きツールを追加、SSE/Streamable HTTPを追加

### 既存MCPサーバーのデバッグ
1. `npx @modelcontextprotocol/inspector` でMCP Inspectorを起動
2. サーバーをSTDIOモードでInspectorに接続
3. ツール一覧・リソース一覧が正しく返るか確認
4. 各ツールを手動実行し、レスポンスの `content` 配列の形式を検証
5. エラー時は `isError: true` フラグが設定されているか確認
6. Claude Desktopのログ（`~/Library/Logs/Claude/mcp*.log`）でプロトコルエラーを調査

### everythingサーバーでプロトコル全機能を検証
1. `cd src/everything && npm install && npm run build`
2. Claude Desktopに登録して接続
3. `echo`（基本）→ `add`（計算）→ `longRunningOperation`（progress通知）→ `sampleLLM`（sampling）の順にツールを実行
4. リソースサブスクリプション（`test://static/resource`）・定期通知の動作を確認
5. 自サーバーの実装と比較して差異を特定

### LLMエージェントにGit操作機能を付与
1. `uvx mcp-server-git --repository /path/to/repo` で起動確認
2. `claude_desktop_config.json` に登録（上記設定例参照）
3. `git_log`・`git_diff`・`git_status`・`git_show` ツールが利用可能になることを確認
4. エージェントのプロンプトに「リポジトリの変更履歴を確認してからコードレビューせよ」等の指示を追加

## 注意点
- **`console.log` はSTDIOを壊す**: STDIOモードではすべてのデバッグ出力を `console.error` に向けること。`console.log` への出力はJSON-RPCメッセージと混在し、クライアントが `SyntaxError: Unexpected token` で切断される。最も頻出のハマりポイント
- **`McpServer` と `Server` の違い**: `McpServer`（`@modelcontextprotocol/sdk/server/mcp.js`）は高レベルAPI。`Server`（`@modelcontextprotocol/sdk/server/index.js`）は低レベルAPI。新規開発には `McpServer` を使え。内部の `Server` インスタンスには `server.server` でアクセス
- **ツールのレスポンス形式**: `content` は必ず配列で返す。`{ type: "text", text: "..." }` または `{ type: "image", data: "base64...", mimeType: "image/png" }`。文字列を直接返すとプロトコルエラー
- **エラーハンドリング**: ツール実行エラーは例外を投げるのではなく `{ content: [...], isError: true }` を返す。未捕捉例外はクライアントにinternal errorとして伝わり、ユーザーに有用なメッセージが表示されない
- **Conditional Tool Registration のタイミング**: 遅延登録は `server.server.oninitialized` 内で行うこと。`connect()` 前はケーパビリティが未確定。`oninitialized` の外で `getClientCapabilities()` を呼ぶと `undefined` が返る
- **セッションスコープのリソース管理**: `onclose` でのクリーンアップを怠るとメモリリークする。特にSSE/Streamable HTTPでは接続断がサイレントに起きるため、タイムアウトベースのGCも検討
- **filesystemサーバーのパス制限**: 許可ディレクトリを引数で明示しないと起動しない。シンボリックリンクによるパストラバーサルも防いでいるため、シンボリックリンク先のディレクトリも許可リストに含めること
- **SSE の `sessionId` 管理**: SSEではクライアントがGET `/sse` で接続後、POST `/messages?sessionId=xxx` でメッセージを送る。`sessionId` の紐付けを間違えると別セッションにメッセージが届く
- **Streamable HTTPのセッション**: `sessionIdGenerator` を指定しないとステートレスモードになり、セッション横断の状態管理ができない。永続化が必要な場合は必ず指定
- **Pythonサーバー（git/fetch）は `uvx` 推奨**: `pip` 直接インストールよりも `uvx` による分離環境実行が安全。グローバル環境への依存汚染を防ぐ
- **`zod` スキーマの `.describe()` は必須級**: ツールパラメータの `.describe()` を省略するとLLMが引数の用途を理解できず、誤った値を渡す原因になる

## 関連スキル
- **n8n-mcp**: n8nからMCPサーバーを呼び出すMCPClient統合。サーバー側の実装パターンと合わせてクライアント側の動作を理解する際に参照
- **lightrag**: LightRAGのMCPサーバー統合。RAG機能をMCPツールとして公開する実装例
- **langgraph**: LangGraphエージェントからMCPツールを呼び出すパターン。エージェント側のツール統合設計に参照
- **ai**: Vercel AI SDKのMCPクライアント統合。フロントエンドからMCPサーバーを利用する際の接続パターン
- **cli**: CLIツール開発の汎用パターン。MCPサーバーのCLIラッパー実装に応用可能
```
