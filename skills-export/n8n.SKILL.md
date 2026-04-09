改善したSKILL.md全文を出力します。

---

```markdown
---
name: n8n
description: n8nワークフロー自動化プラットフォームのセルフホスト展開・カスタムノード開発・AIエージェント構築（`@n8n/agents` StateGraph）・内部パッケージ（`@n8n/db` TypeORM / `@n8n/expression-runtime` isolated-vm / `@n8n/di`）の設計・実装を行うときに必ず参照せよ。Docker Compose展開、REST API操作、pnpmモノレポのビルド・テストにも適用すること。
---

# n8n

## 概要
n8nはノードベースのワークフロー自動化プラットフォームで、500以上の組み込みノードによる外部サービス連携、LangGraph StateGraphベースのAIエージェント、MCP統合、サンドボックスコード実行を提供する。TypeScript製pnpmモノレポ構成で、`@n8n/agents`・`@n8n/db`・`@n8n/ai-workflow-builder.ee`・`@n8n/expression-runtime`・`@n8n/di`が疎結合に組み合わさる。

## いつ使うか
- n8nをDocker Compose / npmでセルフホスト展開・運用するとき
- `@n8n/agents` の `StateGraph` でプランナー・スーパーバイザー・レスポンダーのマルチエージェントを構築するとき
- MCPサーバーを `MCPClient` 経由でエージェントツールに統合するとき
- `@n8n/db` の TypeORM エンティティ・リポジトリパターンでバックエンド実装するとき
- `@n8n/expression-runtime` の `isolated-vm` サンドボックスで式評価するとき
- `@n8n/di` のデコレータベースDI・ライフサイクル管理を使うとき
- カスタムノード・カスタムクレデンシャルを開発するとき
- pnpmモノレポのビルド・テスト・パッケージ間依存を管理するとき

## 主要コマンド・API

### セルフホスト展開（Docker Compose）

```yaml
# docker-compose.yml
services:
  n8n:
    image: n8nio/n8n:latest
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=changeme
      - DB_TYPE=postgresdb
      - DB_POSTGRESDB_HOST=postgres
      - DB_POSTGRESDB_DATABASE=n8n
      - DB_POSTGRESDB_USER=n8n
      - DB_POSTGRESDB_PASSWORD=n8n
      - N8N_ENCRYPTION_KEY=${N8N_ENCRYPTION_KEY}
    volumes:
      - n8n_data:/home/node/.n8n
    depends_on:
      - postgres

  postgres:
    image: postgres:16
    environment:
      - POSTGRES_DB=n8n
      - POSTGRES_USER=n8n
      - POSTGRES_PASSWORD=n8n
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  n8n_data:
  postgres_data:
```
```bash
# 起動・停止
docker compose up -d
docker compose logs -f n8n
docker compose down

# npm直接起動（開発用）
npx n8n start --tunnel  # Webhookトンネル付き
```

### モノレポのビルド・テスト（pnpm）

```bash
# 依存関係インストール
pnpm install

# 特定パッケージのビルド
pnpm --filter @n8n/agents build
pnpm --filter @n8n/ai-workflow-builder.ee build
pnpm --filter @n8n/db build

# 開発サーバー（ホットリロード付き）
pnpm dev

# テスト
pnpm --filter @n8n/agents test
pnpm --filter @n8n/db test
pnpm test:e2e

# リント
pnpm lint
pnpm typecheck
```

### マルチエージェント StateGraph（`@n8n/agents`）

```typescript
import { StateGraph, END } from "@langchain/langgraph";
import { BaseMessage } from "@langchain/core/messages";

interface WorkflowBuilderState {
  userRequest: string;
  plan: string[];
  currentTask: string;
  result: string;
  messages: BaseMessage[];
}

const graph = new StateGraph<WorkflowBuilderState>({
  channels: {
    userRequest: { value: (a, b) => b ?? a },
    plan: { value: (a, b) => b ?? a, default: () => [] },
    currentTask: { value: (a, b) => b ?? a },
    result: { value: (a, b) => b ?? a },
    messages: { value: (a, b) => a.concat(b), default: () => [] },
  },
});

graph.addNode("planner", plannerFn);
graph.addNode("supervisor", supervisorFn);
graph.addNode("responder", responderFn);

graph.addEdge("__start__", "planner");
graph.addEdge("planner", "supervisor");
graph.addConditionalEdges("supervisor", (state) =>
  state.plan.length === 0 ? "responder" : "planner"
);
graph.addEdge("responder", END);

const app = graph.compile();
const result = await app.invoke({
  userRequest: "Slackに毎朝レポートを送るワークフローを作って",
});
```

### MCPサーバーをエージェントツールに統合（`@n8n/agents`）

```typescript
import { MCPClient } from "@n8n/agents/mcp";
import { DynamicStructuredTool } from "@langchain/core/tools";

const mcpClient = new MCPClient({
  transport: "stdio",
  command: "npx",
  args: ["-y", "@modelcontextprotocol/server-filesystem", "/workspace"],
});
await mcpClient.connect();

// MCPツール → LangChainツール変換
const langchainTools = (await mcpClient.getTools()).map(
  (tool) =>
    new DynamicStructuredTool({
      name: tool.name,
      description: tool.description,
      schema: tool.inputSchema,
      func: async (input) =>
        JSON.stringify((await mcpClient.callTool(tool.name, input)).content),
    })
);

const agent = createReactAgent({ llm, tools: langchainTools });

// シャットダウン時に必ず切断
process.on("SIGTERM", () => mcpClient.disconnect());
```

### TypeORMエンティティ・リポジトリ（`@n8n/db`）

```typescript
import { Entity, Column, PrimaryGeneratedColumn, Repository } from "typeorm";
import { InjectRepository } from "@n8n/db";
import { Injectable } from "@n8n/di";

@Entity("workflow_entity")
export class WorkflowEntity {
  @PrimaryGeneratedColumn("uuid")
  id: string;

  @Column({ type: "varchar", length: 255 })
  name: string;

  @Column({ type: "json" })
  nodes: INode[];

  @Column({ type: "json" })
  connections: IConnections;

  @Column({ type: "boolean", default: true })
  active: boolean;
}

@Injectable()
export class WorkflowService {
  constructor(
    @InjectRepository(WorkflowEntity)
    private readonly workflowRepo: Repository<WorkflowEntity>,
  ) {}

  async findActiveWorkflows(): Promise<WorkflowEntity[]> {
    return this.workflowRepo.find({ where: { active: true } });
  }
}
```

### サンドボックス式評価（`@n8n/expression-runtime`）

```typescript
import { ExpressionEvaluator } from "@n8n/expression-runtime";

const evaluator = new ExpressionEvaluator({
  sandbox: "isolated-vm",
  cacheSize: 100,
  timeout: 5000,
});

const result = await evaluator.evaluate(
  "{{ $json.name.toUpperCase() + '_' + $now.toISO() }}",
  { $json: { name: "workflow" } },
);
// => "WORKFLOW_2026-04-09T..."
```

### デコレータベースDI（`@n8n/di`）

```typescript
import { Module, Injectable, OnLifecycleEvent } from "@n8n/di";

@Injectable()
export class WorkflowExecutionService {
  @OnLifecycleEvent("init")
  async onInit() {
    await this.loadActiveWorkflows();
  }

  @OnLifecycleEvent("shutdown")
  async onShutdown() {
    await this.stopAllExecutions();
  }
}

@Module({
  providers: [WorkflowExecutionService],
  exports: [WorkflowExecutionService],
})
export class WorkflowModule {}
```

### REST API操作

```bash
# ヘルスチェック
curl http://localhost:5678/healthz

# ワークフロー一覧取得
curl -H "X-N8N-API-KEY: $N8N_API_KEY" \
  http://localhost:5678/api/v1/workflows

# ワークフロー作成
curl -X POST http://localhost:5678/api/v1/workflows \
  -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "My Workflow", "nodes": [...], "connections": {...}}'

# ワークフロー実行
curl -X POST http://localhost:5678/api/v1/workflows/{id}/run \
  -H "X-N8N-API-KEY: $N8N_API_KEY"

# 実行履歴取得
curl -H "X-N8N-API-KEY: $N8N_API_KEY" \
  http://localhost:5678/api/v1/executions?workflowId={id}&limit=10
```

## ワークフロー例

### 1. Docker Composeによるプロダクション展開

1. `docker-compose.yml` にn8n + PostgreSQLサービスを定義（上記テンプレート参照）
2. 暗号化キーを生成して `.env` に設定する
   ```bash
   echo "N8N_ENCRYPTION_KEY=$(openssl rand -hex 32)" >> .env
   ```
3. 起動してヘルスチェックを確認する
   ```bash
   docker compose up -d
   curl http://localhost:5678/healthz  # => {"status":"ok"}
   ```
4. ブラウザで `http://localhost:5678` にアクセスし、初期ユーザーを作成する
5. Settings → API → API Keyを発行し、外部連携用に保管する

### 2. AIワークフロービルダーの実装

1. `@n8n/ai-workflow-builder.ee` の既存エージェント構成を確認する
   ```bash
   pnpm --filter @n8n/ai-workflow-builder.ee build
   ```
2. `WorkflowBuilderState` を定義し、channelsのリデューサーを設計する（messages は `a.concat(b)`、それ以外は `b ?? a`）
3. planner → supervisor → responder の3ノードを `StateGraph` に登録する
4. supervisor の `addConditionalEdges` で未完タスクの有無によりルーティングする
5. `graph.compile()` でアプリを生成し、エンドツーエンドテストを実施する
   ```typescript
   const result = await app.invoke({
     userRequest: "GitHub Issueが作成されたらSlackに通知するワークフロー",
   });
   expect(isValidWorkflowJSON(result)).toBe(true);
   ```

### 3. カスタムノード開発

1. `packages/nodes-base/nodes/` の既存ノードを参考にディレクトリを作成する
   ```bash
   mkdir -p packages/nodes-base/nodes/MyService
   ```
2. `MyService.node.ts` にノードクラスを実装する（`INodeType` インターフェース）
3. `MyService.credentials.ts` に認証情報クラスを実装する
4. `package.json` の `n8n.nodes` / `n8n.credentials` に登録する
5. ビルドしてローカルで動作確認する
   ```bash
   pnpm --filter n8n-nodes-base build
   pnpm dev
   ```

## 注意点

- **モノレポのパッケージ境界を守る**: `@n8n/agents`・`@n8n/db`・`@n8n/ai-workflow-builder.ee` は疎結合に設計されており、パッケージをまたぐ直接importは避けること。依存はパッケージの `package.json` で明示管理する
- **`N8N_ENCRYPTION_KEY` の固定が必須**: この値が変わるとクレデンシャル（APIキー等）が全て復号不能になる。Docker再起動時に消失しないよう `.env` またはシークレット管理で永続化すること
- **SQLiteは本番非推奨**: デフォルトのSQLiteは同時実行に弱く、ワークフロー数が増えるとロック競合が頻発する。本番では `DB_TYPE=postgresdb` を設定すること
- **`isolated-vm` のメモリ制限**: `@n8n/expression-runtime` のサンドボックスはデフォルトでヒープ制限がある。大量データを式内で処理するとOOMで静かに失敗する。`timeout` 設定も忘れずに行うこと
- **MCPClient の切断忘れ**: `mcpClient.connect()` 後に `disconnect()` を呼ばないとstdioプロセスがゾンビ化する。シャットダウンフック（`@OnLifecycleEvent("shutdown")` や `process.on("SIGTERM")`）に必ず登録すること
- **StateGraph のリデューサー未定義**: channelsにリデューサーを定義しないとノード出力が上書きモードになり、messagesの蓄積が消える。`messages` チャンネルには必ず `a.concat(b)` 等の結合リデューサーを指定すること
- **TypeORMマイグレーションの順序**: `@n8n/db` のマイグレーションはSQLiteとPostgreSQLで別ファイル。`pnpm migration:run` 時にDB_TYPEに対応するマイグレーションが選択されるが、手動でファイルを追加する場合はタイムスタンプ順に注意すること
- **pnpm workspace のビルド順序**: パッケージ間に依存がある場合、`pnpm --filter` で個別ビルドすると依存先が未ビルドでエラーになる。`pnpm build` でトポロジカル順にビルドするか、依存先を先にビルドすること
- **Webhookトンネルは開発専用**: `npx n8n start --tunnel` はngrok経由の一時URLを使う。本番ではリバースプロキシ + `N8N_HOST` / `WEBHOOK_URL` 環境変数で固定URLを設定すること
- **`.ee` パッケージはエンタープライズ機能**: `@n8n/ai-workflow-builder.ee` 等の `.ee` 付きパッケージはエンタープライズライセンスが必要。OSS版では機能が制限される

## 関連スキル
- **n8n-mcp**: MCPサーバー経由でのノード検索・ワークフロー検証・自動修正・CRUD操作。AI生成ワークフローの品質向上に使用
- **n8n-as-code**: `n8nac` CLIによるワークフローのGit管理・3-wayマージ同期・TypeScriptデコレータ記法
- **langgraph**: `StateGraph`・`@entrypoint`・`@task` 等のLangGraph本体API。`@n8n/agents` はLangGraphの上に構築されている
- **docker**: n8n + PostgreSQL + Redis のコンテナオーケストレーション・ボリューム管理・ネットワーク設計
- **supabase**: PostgreSQLバックエンドのホスティング。`@n8n/db` の接続先として利用する場合
```

---

**改善サマリ:**

| 基準 | 元の問題 | 改善 |
|---|---|---|
| 1. description精度 | 汎用的で具体的パッケージ名・APIなし | `@n8n/agents StateGraph`・`@n8n/db TypeORM`・`isolated-vm`・`Docker Compose`等の具体的トリガーキーワードを列挙 |
| 2. 500行以下 | ~300行だが注意点が途切れて未完成 | 約290行。Docker Compose・REST API・カスタムノード開発を追加しつつ範囲内 |
| 3. コマンド例 | `pnpm install`/`pnpm dev`のみで具体性不足、ポート番号なし | Docker Compose全文（ポート5678）、REST API（curl + 認証ヘッダ）、暗号化キー生成コマンドを追加 |
| 4. ワークフロー例 | テキスト手順のみでコード片なし、Yjs/CRDT等ニッチなテーマが混在 | 各ステップにコピペ可能なコード片を埋め込み、実践的な3シナリオ（展開・AIビルダー・カスタムノード）に整理 |
| 5. 注意点 | 1項目目で途切れて未完成 | 10項目に拡充。暗号化キー消失・SQLiteロック競合・MCPゾンビプロセス・ビルド順序・EEライセンス等の実害ベースのハマりポイントをカバー |
| 6. 関連スキル | セクション自体が欠落 | n8n-mcp・n8n-as-code・langgraph・docker・supabaseの5つを各1行の用途説明付きで追加 |
