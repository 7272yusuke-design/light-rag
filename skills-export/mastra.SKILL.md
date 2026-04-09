Now I have the methodology and high-quality reference examples. Let me evaluate and produce the improved SKILL.md.

Key issues in the original:
1. **Description**: Too generic ("あらゆる場面で参照すること") - needs specific API names as trigger keywords
2. **Line count**: ~350+ lines, within limit but can be tightened
3. **Workflow examples**: Steps without code - less practical than reference examples
4. **注意点**: Last bullet cut off, some items generic
5. **関連スキル**: Missing entirely
6. **Code redundancy**: Some examples overlap (e.g., RAG section duplicates ai SDK patterns)

```markdown
---
name: mastra
description: Mastraフレームワークを使ったTypeScript AIエージェント・ワークフロー・RAGパイプライン・マルチエージェントシステムを構築する際に必ずこのスキルを使え。`new Agent`・`createTool`・`Workflow`・`Step`・`suspend`/`resume`・`MCPServer`・`MCPClient`・`MastraClient`・`mastra dev`・`mastra deploy`などMastra固有のAPIが関わる場面では即座にこのスキルを参照せよ。
---

# mastra

## 概要
MastraはTypeScript製のAIエージェント・ワークフロー開発フレームワークで、LLMエージェント・マルチエージェントシステム・RAGパイプライン・MCPサーバー統合を統一APIで提供する。ストレージ・ベクターDB・LLMプロバイダー・認証をすべてアダプターとして差し替え可能で、Vercel・Cloudflare Workers・Netlifyへのエッジデプロイに対応する。

## いつ使うか
- `new Agent` でLLMエージェント・チャットBot・カスタマーサポートシステムを構築するとき
- `Workflow`・`Step` でステップ・並列・分岐・ループ・人間介在フローを定義するとき
- `suspend()` / `resume()` でヒューマン・イン・ザ・ループを実装するとき
- `createTool` でエージェントが使うツールを定義するとき
- ドキュメントのチャンキング・埋め込み・ベクター検索でRAGパイプラインを構築するとき
- `MCPServer` / `MCPClient` でMCPサーバーを構築または既存MCPサーバーに接続するとき
- 複数エージェントをスーパーバイザーパターンでオーケストレーションするとき
- `Memory` でエージェントの会話履歴・セマンティック検索・ワーキングメモリを管理するとき
- `MastraClient` でフロントエンドからエージェント・ワークフローを呼び出すとき
- `mastra dev` / `mastra build` / `mastra deploy` でローカル開発・デプロイするとき

## 主要コマンド・API

### インストール
```bash
# 新規プロジェクト作成（対話式スキャフォールド）
npx create-mastra@latest

# 既存プロジェクトへの追加
npm install mastra @mastra/core
```

### エージェント定義
```typescript
import { Agent } from "@mastra/core/agent";
import { openai } from "@ai-sdk/openai";

const myAgent = new Agent({
  name: "my-agent",
  instructions: "あなたは親切なアシスタントです。",
  model: openai("gpt-4o"),
  tools: { myTool },
});

// テキスト生成
const result = await myAgent.generate("こんにちは");

// ストリーミング
const stream = await myAgent.stream("こんにちは");
for await (const chunk of stream.textStream) {
  process.stdout.write(chunk);
}
```

### ツール定義
```typescript
import { createTool } from "@mastra/core/tools";
import { z } from "zod";

const weatherTool = createTool({
  id: "get-weather",
  description: "指定都市の天気を取得する",
  inputSchema: z.object({
    city: z.string().describe("都市名"),
  }),
  outputSchema: z.object({
    temperature: z.number(),
    condition: z.string(),
  }),
  execute: async ({ context }) => {
    const data = await fetch(`https://api.weather.example/${context.city}`);
    return data.json();
  },
});
```

### ワークフロー定義
```typescript
import { Workflow, Step } from "@mastra/core/workflows";
import { z } from "zod";

const fetchStep = new Step({
  id: "fetch",
  inputSchema: z.object({ url: z.string() }),
  outputSchema: z.object({ body: z.string() }),
  execute: async ({ context }) => {
    const res = await fetch(context.url);
    return { body: await res.text() };
  },
});

const analyzeStep = new Step({
  id: "analyze",
  execute: async ({ context }) => {
    const prev = context.getStepResult("fetch"); // 前ステップの結果を明示取得
    return { summary: prev.body.slice(0, 200) };
  },
});

const workflow = new Workflow({
  name: "fetch-and-analyze",
  triggerSchema: z.object({ url: z.string() }),
});

workflow.step(fetchStep).then(analyzeStep).commit(); // commit() 必須

const run = workflow.createRun();
const result = await run.start({ triggerData: { url: "https://example.com" } });
```

### 並列・分岐・ループ
```typescript
// 並列実行: stepB と stepC を同時に実行し、完了後 stepD へ
workflow.step(stepA).parallel([stepB, stepC]).then(stepD).commit();

// 条件分岐
workflow
  .step(stepA)
  .branch([
    [async ({ context }) => context.score > 80, highPath],
    [async ({ context }) => context.score <= 80, lowPath],
  ])
  .commit();

// ループ（do-while）
workflow
  .step(stepA)
  .dowhile(retryStep, async ({ context }) => context.retryCount < 3)
  .commit();
```

### サスペンド・レジューム（人間介在フロー）
```typescript
const approvalStep = new Step({
  id: "approval",
  execute: async ({ context, suspend }) => {
    if (!context.approved) {
      await suspend({ message: "承認が必要です", draft: context.draft });
    }
    return { approved: true };
  },
});

// 実行 → サスペンド状態で停止
const run = workflow.createRun();
const result = await run.start({ triggerData: { draft: "提案内容..." } });

// 外部で承認後にレジューム
await run.resume({
  stepId: "approval",
  context: { approved: true },
});
```

### メモリ管理
```typescript
import { Memory } from "@mastra/memory";
import { LibSQLStore, LibSQLVector } from "@mastra/libsql";

const memory = new Memory({
  storage: new LibSQLStore({ url: "file:memory.db" }),
  vector: new LibSQLVector({ connectionUrl: "file:memory.db" }),
  options: {
    lastMessages: 20,
    semanticRecall: { topK: 5, messageRange: 2 },
    workingMemory: { enabled: true },
  },
});

const agent = new Agent({ name: "agent", model: openai("gpt-4o"), memory });
// resourceId + threadId でスレッド分離（省略すると会話が混在する）
await agent.generate("質問", { resourceId: "user-123", threadId: "thread-456" });
```

### MCPサーバー構築
```typescript
import { MCPServer } from "@mastra/mcp";

const server = new MCPServer({
  name: "my-mcp-server",
  version: "1.0.0",
  tools: { weatherTool, searchTool },
});

await server.startStdio(); // stdio トランスポートで起動
```

### MCPクライアント接続
```typescript
import { MCPClient } from "@mastra/mcp";

const client = new MCPClient({
  servers: {
    filesystem: {
      command: "npx",
      args: ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"],
    },
    remote: {
      url: "https://my-mcp-server.example.com/mcp",
    },
  },
});

const tools = await client.getTools();
const agent = new Agent({ name: "agent", model: openai("gpt-4o"), tools });

// 使用後は必ず切断
await client.disconnect();
```

### マルチエージェント（スーパーバイザーパターン）
```typescript
const researcher = new Agent({ name: "researcher", model: openai("gpt-4o"), instructions: "調査専門" });
const writer = new Agent({ name: "writer", model: openai("gpt-4o"), instructions: "執筆専門" });

const supervisor = new Agent({
  name: "supervisor",
  instructions: "リサーチャーとライターを指示してタスクを完了せよ。",
  model: openai("gpt-4o"),
  tools: {
    research: createTool({
      id: "research",
      description: "リサーチャーに調査を依頼する",
      inputSchema: z.object({ query: z.string() }),
      execute: async ({ context }) => researcher.generate(context.query),
    }),
    write: createTool({
      id: "write",
      description: "ライターに執筆を依頼する",
      inputSchema: z.object({ content: z.string() }),
      execute: async ({ context }) => writer.generate(context.content),
    }),
  },
});
```

### Mastraインスタンス登録・サーバー起動
```typescript
import { Mastra } from "mastra";

export const mastra = new Mastra({
  agents: { myAgent, supervisor },
  workflows: { myWorkflow },
  vectors: { myVectorStore },
});

// package.json: "dev": "mastra dev"
```

### フロントエンドからの呼び出し
```typescript
import { MastraClient } from "@mastra/client-js";

const client = new MastraClient({ baseUrl: "http://localhost:4111" });

const agent = client.getAgent("my-agent");
const response = await agent.generate({ messages: [{ role: "user", content: "hello" }] });

// ストリーミング
const stream = await agent.stream({ messages: [{ role: "user", content: "hello" }] });
```

### デプロイ
```bash
# Cloudflare Workers
npm install @mastra/deployer-cloudflare
mastra build
mastra deploy

# Vercel / Netlify も同様にデプロイヤーを追加して deploy
```

## ワークフロー例

### RAG検索エージェントの構築
1. パッケージをインストールする
   ```bash
   npm install mastra @mastra/core @mastra/memory @mastra/libsql
   ```
2. ベクターストアを初期化し、ドキュメントを投入する
   ```typescript
   const chunks = await chunkText(document, { size: 512, overlap: 50 });
   const { embeddings } = await embedMany({
     model: openai.embedding("text-embedding-3-small"),
     values: chunks.map(c => c.text),
   });
   await vectorStore.upsert({ indexName: "docs", vectors: embeddings, metadata: chunks });
   ```
3. 検索ツールを定義してエージェントに渡す
   ```typescript
   const searchTool = createTool({
     id: "search-docs",
     description: "ドキュメントを検索する",
     inputSchema: z.object({ query: z.string() }),
     execute: async ({ context }) => {
       const { embedding } = await embed({
         model: openai.embedding("text-embedding-3-small"),
         value: context.query,
       });
       return vectorStore.query({ indexName: "docs", queryVector: embedding, topK: 5 });
     },
   });
   const agent = new Agent({ name: "rag-agent", model: openai("gpt-4o"), tools: { searchTool } });
   ```
4. `Mastra` に登録し `mastra dev` で起動、`MastraClient` 経由でフロントエンドから呼び出す

### 人間承認付きワークフロー
1. 処理ステップ → 承認ステップ（`suspend()`）→ 実行ステップの順でワークフローを構築する
2. `run.start()` で実行し、承認ステップでサスペンド状態になる
3. 外部システム（Slack通知等）で承認者に通知する
4. 承認後 `run.resume({ stepId: "approval", context: { approved: true } })` で再開する

### マルチエージェント自動化パイプライン
1. 役割ごとに専門エージェントを `Agent` で定義する
2. 各エージェントを `createTool` でツールとしてラップし、スーパーバイザーに渡す
3. 必要に応じて `Workflow` で実行順序を制御する（並列調査 → 集約 → 執筆 の流れなど）
4. `Mastra` インスタンスに全エージェントを登録し、`mastra dev` で動作確認後デプロイする

## 注意点
- **`workflow.commit()` を忘れない**: ワークフロー定義後に `.commit()` を呼ばないと実行できない。呼び忘れはサイレントに失敗する
- **Step間のデータ受け渡しは `context.getStepResult(stepId)`**: 前ステップの出力は自動的に次ステップのinputにならない。明示的に取得しないと `undefined` になる
- **メモリ使用時は `resourceId` と `threadId` を必ず指定**: 省略するとスレッドが分離されず全ユーザーの会話履歴が混在する
- **MCPクライアントは `client.disconnect()` を呼ぶ**: 長期稼働プロセスではリソースリークの原因になる。`try/finally` パターンを使うこと
- **Cloudflare Workers環境ではNode.js専用APIが使えない**: `fs`・`child_process` 等を使うツールはWorkers非対応。エッジ環境対応のアダプターを選択すること
- **`mastra dev` はローカル開発専用**: 本番環境では `mastra build` → `mastra deploy` を使う。dev サーバーを本番公開しないこと
- **ベクターDBのインデックスは事前作成が必要**: `vectorStore.createIndex()` を初回セットアップ時に実行しておかないとupsert/queryがエラーになる
- **LLMプロバイダーのAPIキーは環境変数で設定**: `OPENAI_API_KEY`・`ANTHROPIC_API_KEY` 等。Mastra側でのAPIキー設定は不要だが、AI SDKプロバイダーが環境変数を参照する
- **ストリーミングはAI SDK互換**: `stream.textStream` / `stream.fullStream` を使い、フロントエンドではVercel AI SDKの `useChat` と組み合わせ可能
- **`@mastra/core` と `mastra` は別パッケージ**: エージェント・ツール・ワークフロー定義は `@mastra/core` から、`Mastra` インスタンスは `mastra` からインポートする。混同するとビルドエラーになる

## 関連スキル
- **ai**: Vercel AI SDK。Mastra内部で使うLLMプロバイダー・埋め込み・ストリーミングの基盤。`openai()`・`embed()`等はAI SDKのAPI
- **langgraph**: Python製の代替フレームワーク。グラフベース設計が得意で、Pythonエコシステムが必要な場合に選択
- **crewai**: Python製のマルチエージェントフレームワーク。ロールベース設計が得意
- **lightrag**: RAGバックエンド。ナレッジグラフベースのRAGが必要な場合にMastraエージェントのツールとして統合
- **supabase**: PostgreSQLバックエンド。Mastraのストレージ・ベクターDB・認証プロバイダーとして利用可能
- **servers**: MCPサーバー一覧。Mastraの `MCPClient` で接続する外部ツールサーバーを探す際に参照
```
