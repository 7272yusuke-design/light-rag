```markdown
---
name: ai
description: Vercel AI SDK（`ai`パッケージ）を使ったチャットボット・エージェント・構造化出力・ストリーミングUIを構築する際に必ずこのスキルを使え。`generateText`・`streamText`・`useChat`・`generateObject`・ツール呼び出し・MCP連携などAI SDK固有のAPIが関わる場面では即座にこのスキルを参照せよ。
---

# ai

## 概要
Vercel AI SDKはTypeScript/JavaScript向けのAIアプリケーション構築フレームワークで、OpenAI・Anthropic・Google等30以上のLLMプロバイダーを統一APIで扱える。テキスト生成・ストリーミング・構造化オブジェクト生成・ツール呼び出し・エージェントループ・埋め込み・マルチモーダル対応を提供し、Next.js/React等のフロントエンドとシームレスに統合できる。

## いつ使うか
- LLMを使ったチャットボット・AIアシスタントをTypeScriptで実装するとき
- `useChat`・`useCompletion`・`useObject`フックでストリーミングUIを構築するとき
- ツール呼び出し（function calling）やエージェントループを`maxSteps`で実装するとき
- zodスキーマを使って構造化オブジェクト（JSON）をLLMから生成したいとき
- OpenAI・Anthropic・Googleなど複数プロバイダーをコード変更なく切り替えたいとき
- MCPサーバーのツールをLLMに接続してエージェントを構築するとき
- RAGシステムで埋め込み生成（`embed`/`embedMany`）を行うとき
- Next.js App RouterのRoute HandlerでLLMレスポンスをストリーミング返却するとき
- LLMの推論過程（reasoning）を抽出・表示したいとき

## 主要コマンド・API

### インストール
```bash
# コアパッケージ
npm install ai

# プロバイダー（必要なものを選択）
npm install @ai-sdk/openai @ai-sdk/anthropic @ai-sdk/google

# zodは構造化出力・ツール定義に必須
npm install zod
```

### テキスト生成
```typescript
import { generateText } from 'ai';
import { openai } from '@ai-sdk/openai';

const { text, usage } = await generateText({
  model: openai('gpt-4o'),
  system: 'あなたは親切なアシスタントです。',
  prompt: 'TypeScriptの型システムを説明してください',
});
```

### ストリーミング（サーバー側 Route Handler）
```typescript
// app/api/chat/route.ts
import { streamText } from 'ai';
import { anthropic } from '@ai-sdk/anthropic';

export async function POST(req: Request) {
  const { messages } = await req.json();

  const result = streamText({
    model: anthropic('claude-sonnet-4-20250514'),
    system: 'あなたは親切なアシスタントです。',
    messages,
  });

  return result.toDataStreamResponse();
}
```

### ストリーミング（クライアント側 React）
```typescript
'use client';
import { useChat } from '@ai-sdk/react';

export default function Chat() {
  const { messages, input, handleInputChange, handleSubmit, isLoading } = useChat();

  return (
    <div>
      {messages.map(m => (
        <div key={m.id}>
          <strong>{m.role}:</strong> {m.content}
        </div>
      ))}
      <form onSubmit={handleSubmit}>
        <input value={input} onChange={handleInputChange} disabled={isLoading} />
        <button type="submit" disabled={isLoading}>送信</button>
      </form>
    </div>
  );
}
```

### 構造化オブジェクト生成
```typescript
import { generateObject } from 'ai';
import { openai } from '@ai-sdk/openai';
import { z } from 'zod';

const { object } = await generateObject({
  model: openai('gpt-4o'),
  schema: z.object({
    title: z.string().describe('タスクのタイトル'),
    tags: z.array(z.string()).describe('関連タグ'),
    priority: z.enum(['low', 'medium', 'high']),
  }),
  prompt: 'このタスクを分類してください: 本番環境でログイン画面が白くなるバグ',
});
// object は { title: string; tags: string[]; priority: "low"|"medium"|"high" } 型
```

### ストリーミング構造化オブジェクト生成
```typescript
import { streamObject } from 'ai';
import { openai } from '@ai-sdk/openai';
import { z } from 'zod';

const result = streamObject({
  model: openai('gpt-4o'),
  schema: z.object({
    summary: z.string(),
    keyPoints: z.array(z.string()),
  }),
  prompt: 'この記事を要約してください: ...',
});

// 部分的なオブジェクトをストリーミングで受信
for await (const partialObject of result.partialObjectStream) {
  console.log(partialObject); // { summary: "途中まで...", keyPoints: undefined }
}
```

### ツール呼び出し + エージェントループ
```typescript
import { generateText, tool } from 'ai';
import { openai } from '@ai-sdk/openai';
import { z } from 'zod';

const { text, steps } = await generateText({
  model: openai('gpt-4o'),
  tools: {
    getWeather: tool({
      description: '指定都市の天気を取得する',
      parameters: z.object({
        city: z.string().describe('都市名'),
      }),
      execute: async ({ city }) => {
        // 実際のAPI呼び出し
        return { city, temperature: 22, condition: '晴れ' };
      },
    }),
    searchWeb: tool({
      description: 'ウェブ検索を実行する',
      parameters: z.object({ query: z.string() }),
      execute: async ({ query }) => {
        return { results: [`${query}の検索結果1`, `${query}の検索結果2`] };
      },
    }),
  },
  maxSteps: 5, // ツール呼び出し→結果→再呼び出しを最大5回繰り返す
  prompt: '東京と大阪の天気を比較してください',
});
// steps で各ステップのツール呼び出し・結果を確認可能
```

### マルチモーダル（画像入力）
```typescript
import { generateText } from 'ai';
import { openai } from '@ai-sdk/openai';

const { text } = await generateText({
  model: openai('gpt-4o'),
  messages: [
    {
      role: 'user',
      content: [
        { type: 'text', text: 'この画像を説明してください' },
        { type: 'image', image: new URL('https://example.com/photo.jpg') },
      ],
    },
  ],
});
```

### 埋め込み生成
```typescript
import { embed, embedMany, cosineSimilarity } from 'ai';
import { openai } from '@ai-sdk/openai';

const { embedding } = await embed({
  model: openai.embedding('text-embedding-3-small'),
  value: '埋め込みたいテキスト',
});

// バッチ処理
const { embeddings } = await embedMany({
  model: openai.embedding('text-embedding-3-small'),
  values: ['テキスト1', 'テキスト2', 'テキスト3'],
});

// 類似度計算
const similarity = cosineSimilarity(embeddings[0], embeddings[1]);
```

### MCPクライアント統合
```typescript
import { generateText, experimental_createMCPClient as createMCPClient } from 'ai';
import { openai } from '@ai-sdk/openai';

const mcpClient = await createMCPClient({
  transport: {
    type: 'sse',
    url: 'http://localhost:8080/sse',
  },
});

try {
  const tools = await mcpClient.tools();
  const { text } = await generateText({
    model: openai('gpt-4o'),
    tools,
    maxSteps: 5,
    prompt: '/tmpディレクトリのファイル一覧を取得して',
  });
} finally {
  await mcpClient.close(); // 必ずクリーンアップ
}
```

### Provider Registry（動的モデル切り替え）
```typescript
import { generateText } from 'ai';
import { createProviderRegistry } from 'ai';
import { openai } from '@ai-sdk/openai';
import { anthropic } from '@ai-sdk/anthropic';
import { google } from '@ai-sdk/google';

const registry = createProviderRegistry({
  openai,
  anthropic,
  google,
});

// 文字列でモデルを指定（設定ファイルや環境変数から渡せる）
const model = registry.languageModel('anthropic:claude-sonnet-4-20250514');

const { text } = await generateText({
  model,
  prompt: 'こんにちは',
});
```

### Provider Middleware（ガードレール・ロギング）
```typescript
import { wrapLanguageModel, generateText } from 'ai';
import { openai } from '@ai-sdk/openai';

const guardedModel = wrapLanguageModel({
  model: openai('gpt-4o'),
  middleware: {
    transformParams: async ({ params }) => {
      console.log(`[LOG] messages=${params.prompt.length}`);
      return params;
    },
    wrapGenerate: async ({ doGenerate }) => {
      const result = await doGenerate();
      console.log(`[LOG] tokens=${result.usage?.totalTokens}`);
      return result;
    },
  },
});
```

## ワークフロー例

### チャットボット（Next.js App Router）の構築
1. パッケージをインストールする
   ```bash
   npm install ai @ai-sdk/openai zod
   ```
2. Route Handler `app/api/chat/route.ts` を作成する
   ```typescript
   import { streamText } from 'ai';
   import { openai } from '@ai-sdk/openai';

   export async function POST(req: Request) {
     const { messages } = await req.json();
     const result = streamText({
       model: openai('gpt-4o'),
       system: 'あなたは親切なアシスタントです。',
       messages,
     });
     return result.toDataStreamResponse();
   }
   ```
3. クライアントコンポーネント `app/page.tsx` で `useChat` を使ってUIに接続する
4. 必要に応じて `tools` オプションにツール定義を追加し、`maxSteps` を設定してエージェントループを有効化する
5. `onToolCall` コールバックでクライアント側ツール実行やHuman-in-the-loop承認を挿入する

### MCPツール統合エージェントの構築
1. MCPサーバーを起動する（例: `npx @modelcontextprotocol/server-filesystem /tmp`）
2. `experimental_createMCPClient` でMCPクライアントを初期化し、`tools()` でツール一覧を取得する
3. `generateText` または `streamText` の `tools` にMCPツールを渡し、`maxSteps` を設定する
4. LLMが自動的にMCPツールを選択・呼び出し、結果を使って回答を生成する
5. 処理完了後に `mcpClient.close()` でクリーンアップする

### 構造化データ抽出パイプラインの構築
1. 抽出したいデータ構造をzodスキーマで定義する（各フィールドに `.describe()` で説明を付与）
2. `generateObject` を使い `schema` オプションにzodスキーマを渡す
3. 返却された `object` は型推論が効くためそのまま型安全に利用できる
4. ストリーミングが必要な場合は `streamObject` を使い `partialObjectStream` で逐次受信する

### マルチプロバイダー対応アプリケーション
1. 使用するプロバイダーパッケージをインストールする
   ```bash
   npm install @ai-sdk/openai @ai-sdk/anthropic @ai-sdk/google
   ```
2. `createProviderRegistry` で全プロバイダーを登録する
3. 環境変数 `AI_MODEL=anthropic:claude-sonnet-4-20250514` 等でモデルを指定する
4. `registry.languageModel(process.env.AI_MODEL)` でモデルを取得し、`generateText`/`streamText` に渡す
5. APIコードの変更なくプロバイダー切り替えが完了する

## 注意点
- **`useChat`のインポートパス**: v4以降は `@ai-sdk/react` からインポートする。旧パス `ai/react` は非推奨
- **`useChat`のデフォルトエンドポイント**: `useChat()` はデフォルトで `/api/chat` にPOSTする。変更する場合は `api` オプションを指定すること
- **`toDataStreamResponse()` vs `toTextStreamResponse()`**: ツール呼び出し・メタデータを含む場合は `toDataStreamResponse()` を使うこと。`useChat` はデータストリームプロトコルを前提としている
- **`maxSteps` の設定忘れ**: ツール呼び出しを含むエージェントループでは `maxSteps` を明示的に設定しないと1ステップ（ツール呼び出し1回）で止まる
- **`system` メッセージの指定方法**: `generateText`/`streamText` では `system` を専用オプションで渡す。`messages` 配列に `role: 'system'` として含めるのではない
- **ストリーミング中のエラーハンドリング**: ストリーム開始後のエラーはHTTPステータスコードで返せない。`onError` コールバックまたはエラーイベントとしてストリームに送信する設計が必要
- **MCPクライアントのクリーンアップ**: `mcpClient.close()` を必ず呼び出すこと。`try/finally` パターンを使うべし
- **zodスキーマの複雑さ**: 過度に深いネストや多数のフィールドはLLMの出力精度を下げる。フラットに保ち、各フィールドに `.describe()` を付与すると精度が上がる
- **プロバイダーごとの機能差異**: ツール呼び出し・ビジョン・構造化出力の対応状況はプロバイダーにより異なる。非対応機能を使うとランタイムエラーになる
- **`experimental_` プレフィックスのAPI**: MCPクライアント等は実験的APIであり、マイナーバージョンでも破壊的変更の可能性がある
- **環境変数の命名規則**: 各プロバイダーは固有の環境変数名を期待する（`OPENAI_API_KEY`・`ANTHROPIC_API_KEY`・`GOOGLE_GENERATIVE_AI_API_KEY`）。設定漏れは認証エラーとなる

## 関連スキル
- **Next.js**: App RouterのRoute Handler・Server Actions・Middlewareとの統合が主要ユースケース
- **React**: `useChat`・`useCompletion`・`useObject` フックによるストリーミングUIコンポーネント実装
- **Zod**: 構造化出力の `schema` 定義・ツールの `parameters` 定義に必須
- **MCP (Model Context Protocol)**: `experimental_createMCPClient` による外部ツールサーバー統合
- **Prisma / Drizzle**: チャット履歴の永続化・RAG用ベクトル検索（pgvector等）
- **Tailwind CSS**: チャットUI・ストリーミング表示のスタイリング
```

**主な改善点:**

1. **description**: 「必ず使え」「即座に参照せよ」に統一。具体的なAPI名（`generateText`・`useChat`等）をトリガーワードに含め、「あらゆる場面で適用」のような曖昧表現を排除
2. **行数**: 約250行。500行以下を維持
3. **コマンド例**: `useChat`のインポートパスを`@ai-sdk/react`に修正、`streamObject`・マルチモーダル・`cosineSimilarity`・Provider Registry・ガードレールミドルウェアの実用例を追加。MCPは`generateText`と組み合わせた実用パターンに変更
4. **ワークフロー例**: MCPエージェント構築フローを新規追加、マルチプロバイダーフローに`createProviderRegistry`の具体的コードを追加、各ステップにコードを含めて実践的に
5. **注意点**: `useChat`のインポートパス変更（v4）、デフォルトエンドポイント`/api/chat`、`system`オプションの正しい渡し方、環境変数命名規則など実際にハマるポイントを追加
6. **関連スキル**: LangChain/LlamaIndex（競合製品）・Upstash/Redis（間接的すぎ）を削除し、Tailwind CSS（チャットUI構築で頻出）を追加
