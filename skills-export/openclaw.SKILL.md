```markdown
---
name: openclaw
description: OpenClawフレームワークでプラグイン開発（contract-api/runtime-api/setup-api分離）、SKILL.mdトリガー定義、GatewayChannel/GatewayNodeSessionのWebSocket通信、CanvasA2UIストリーミング、InvokeCommandRegistry（Android/Kotlin）、OpenClawKit（Swift/iOS）のデバイス機能拡張を行うときに必ず使え。ExecApprovals設定・TalkMode/VoiceWake・セッションコンパクションの実装時も即座に参照せよ。
---

# openclaw

## 概要
OpenClawはmacOS/iOS/Android/Apple Watchのネイティブアプリと中央ゲートウェイサーバーを接続するマルチプラットフォームAIアシスタントフレームワークである。LLMエージェントがカメラ・カレンダー・位置情報・SMSなどのデバイス機能や、Discord・Telegram・iMessageなど50以上のメッセージングチャネルとプラグインベースのアーキテクチャを通じて連携する。`openclaw.plugin.json`によるプラグイン宣言、4ファイル分離（contract-api/runtime-api/setup-api/channel-config-api）、宣言的SKILL.mdによるエージェント能力拡張が設計の中核。

## いつ使うか
- `openclaw.plugin.json` でプラグイン（チャネル・LLMプロバイダー・ツール）を定義・実装するとき
- `.agents/skills/` にSKILL.mdを作成してトリガー・capabilities・手順を定義するとき
- `GatewayChannel`（iOS/Swift）または`GatewayNodeSession`（Android/Kotlin）でWebSocket通信を実装するとき
- `CanvasA2UI`プロトコルでエージェントからクライアントUIにJSONLストリーミングするとき
- `InvokeCommandRegistry`にAndroidデバイス機能のコマンドハンドラを登録するとき
- `OpenClawKit`のSwift APIでカメラ・位置情報などのデバイス抽象化を拡張するとき
- `ExecApprovals`のallowlist・承認ポリシーを設定するとき
- TalkMode/VoiceWakeの音声ウェイクワード・ストリーミングTTSを設定するとき
- セッションコンパクション・チェックポイントの戦略を調整するとき

## 主要コマンド・API

### プラグインマニフェスト
```json
// plugins/my-channel/openclaw.plugin.json
{
  "id": "my-channel-plugin",
  "version": "1.0.0",
  "capabilities": ["channel", "tool"],
  "entry": "./dist/index.js",
  "configSchema": "./channel-config-api.ts"
}
```

### プラグイン4ファイル構造
```
plugins/my-channel/
├── openclaw.plugin.json       # マニフェスト（id・capabilities・entry）
├── contract-api.ts            # 型定義・インターフェース境界（ビルド時参照）
├── runtime-api.ts             # 実行時メッセージハンドラ
├── setup-api.ts               # 起動時のレジストリ登録
├── channel-config-api.ts      # チャネル設定スキーマ
└── dist/
    └── index.js               # ビルド成果物（entry指定先）
```

### contract-api.ts（型定義）
```typescript
// ビルド時にのみ参照される。runtime-apiへの直接importは禁止
export interface MyChannelConfig {
  apiToken: string;
  webhookUrl: string;
  retryCount?: number;
}

export interface IncomingMessage {
  channelId: string;
  senderId: string;
  text: string;
  attachments?: Attachment[];
}
```

### setup-api.ts（起動時登録）
```typescript
import { PluginRegistry } from "@openclaw/core";
import { MyChannelProvider } from "./runtime-api";
import { MyToolHandler } from "./tools";

export function register(registry: PluginRegistry): void {
  registry.registerChannel("my-channel", MyChannelProvider);
  registry.registerTool("my-tool", MyToolHandler);
}
```

### runtime-api.ts（実行時ハンドラ）
```typescript
import { RuntimeContext, IncomingMessage } from "@openclaw/core";

export async function handleIncoming(
  message: IncomingMessage,
  ctx: RuntimeContext
): Promise<void> {
  const response = await ctx.agent.generate(message.text);
  await ctx.channel.send(message.channelId, response);
}
```

### SKILL.md の定義（エージェント能力拡張）
```markdown
<!-- .agents/skills/camera-analyze/SKILL.md -->
---
name: camera-analyze
version: 1.0.0
triggers:
  - "カメラで撮影して分析"
  - "写真を撮って教えて"
  - "目の前のものを見て"
capabilities:
  - camera
  - vision
---

# Camera Analyze

## 手順
1. `camera.capture()` でフレームを取得
2. 画像をbase64エンコードしてLLMに送信
3. 結果をCanvasA2UIでクライアントに返す

## 制約
- カメラ権限が未許可の場合はユーザーに許可を求める
- 画像サイズは1MB以下にリサイズしてから送信
```

### InvokeCommandRegistry（Android/Kotlin）
```kotlin
class CameraHandler : CommandHandler {
    override val commandName = "device.camera.capture"

    override suspend fun invoke(
        params: JsonObject,
        session: GatewayNodeSession
    ): JsonObject {
        val resolution = params["resolution"]?.jsonPrimitive?.content ?: "1080p"
        val frame = CameraManager.capture(resolution)
        return buildJsonObject {
            put("status", "ok")
            put("imageBase64", frame.toBase64())
            put("width", frame.width)
            put("height", frame.height)
        }
    }
}

// Application起動時に登録
val registry = InvokeCommandRegistry()
registry.register(CameraHandler())
registry.register(LocationHandler())  // 複数ハンドラを登録可能
registry.register(CalendarHandler())
```

### OpenClawKit（Swift/iOS）
```swift
import OpenClawKit

// デバイス機能の抽象化
let camera = CameraAbstraction()
let frame = try await camera.captureFrame()

// CanvasA2UIアクションのストリーミング（JSONL形式）
let canvas = CanvasSession(channel: gatewayChannel)
await canvas.stream([
    .renderText("分析結果: \(result)"),
    .showImage(frame.jpegData),
    .renderButton("もう一度撮影", action: "camera.capture")
])
// 各アクションは1行のJSONとしてクライアントに順次送信される
```

### ゲートウェイWebSocket接続（TLSピニング + TOFU）
```swift
// Bonjourで自動探索 → QRコードで初回ペアリング → TOFU証明書ピン留め
let gateway = GatewayChannel(
    endpoint: discoveredEndpoint,
    identity: deviceIdentity,
    tlsCertificatePin: pinnedCert  // 初回接続時に自動保存される
)
try await gateway.connect()

gateway.onMessage { message in
    switch message.type {
    case .invoke:
        dispatcher.dispatch(message)
    case .canvas:
        canvasRenderer.render(message.payload)
    case .heartbeat:
        gateway.pong()
    }
}
```

### ブラウザ自動化（Playwrightプラグイン）
```typescript
const browser = await BrowserPlugin.getInstance();

// アクセシビリティスナップショット取得
const snapshot = await browser.snapshot({ url: "https://example.com" });
// snapshot.elements: [{ref: 1, role: "button", name: "Submit"}, ...]

// ref番号を使ったエージェントアクション実行
await browser.agentAct({
  action: "click",
  ref: 1,           // snapshot内のref番号（揮発性・毎回取得し直すこと）
  cdpProxy: true
});
```

### ExecApprovals設定
```json
{
  "allowlist": [
    { "pattern": "git status", "autoApprove": true },
    { "pattern": "git diff *", "autoApprove": true },
    { "pattern": "npm run build", "autoApprove": true }
  ],
  "denylist": [
    { "pattern": "rm -rf *" },
    { "pattern": "curl * | bash" }
  ],
  "defaultPolicy": "require-approval",
  "gatewayPrompt": true,
  "timeoutSeconds": 30
}
```

### セッションコンパクション
```typescript
// コンテキストウィンドウ圧迫時にチェックポイントを作成
await session.compact({
  strategy: "checkpoint",     // "checkpoint" | "rolling" | "summary-only"
  preserveLastN: 20,          // 直近20メッセージはそのまま保持
  summaryPrompt: "これまでの会話を要約してください",
  mustPreserve: ["user_name", "current_task"]  // 明示的に保持するキー
});
// 注意: compact中は保持対象外のコンテキストにアクセス不可
```

## ワークフロー例

### 新しいメッセージングチャネルプラグインを追加する
1. `plugins/my-channel/` ディレクトリを作成し、4ファイル構造を配置する
   ```bash
   mkdir -p plugins/my-channel && cd plugins/my-channel
   touch openclaw.plugin.json contract-api.ts runtime-api.ts setup-api.ts channel-config-api.ts
   ```
2. `openclaw.plugin.json` に `"id": "my-channel"`, `"capabilities": ["channel"]` を記述する
3. `contract-api.ts` でチャネル設定の型（トークン・Webhook URL等）とメッセージ型を定義する
4. `channel-config-api.ts` で設定スキーマを定義し、ゲートウェイUIのフォーム自動生成に使う
5. `setup-api.ts` で `registry.registerChannel("my-channel", MyChannelProvider)` を呼び出す
6. `runtime-api.ts` で `handleIncoming` を実装し、受信メッセージをエージェントに転送する
7. `npm run build` でビルド後、ゲートウェイを再起動する
   ```bash
   npm run build && npm run gateway:restart
   ```
8. ゲートウェイ管理UIからチャネル設定を入力してアクティベートし、テストメッセージを送信する

### カスタムスキルをエージェントに追加する
1. スキルディレクトリを作成する
   ```bash
   mkdir -p .agents/skills/my-skill
   ```
2. `SKILL.md` にフロントマター（name・version・triggers・capabilities）を記述する
3. triggers は3〜5個に絞る（多すぎるとシステムプロンプトのコンテキストを圧迫する）
4. 手順セクションにツール呼び出し・条件分岐・制約をMarkdownで具体的に定義する
5. スキルが使うツールがあれば `setup-api.ts` でハンドラを登録する
6. ゲートウェイを再起動してスキルがシステムプロンプトに注入されることを確認する
   ```bash
   npm run gateway:restart && curl http://localhost:3000/api/debug/system-prompt | grep "my-skill"
   ```
7. トリガーフレーズでエージェントに話しかけてスキルが発動することをテストする

### Androidデバイス機能をゲートウェイに公開する
1. `CommandHandler`を実装したクラスを作成する
   ```kotlin
   class MyHandler : CommandHandler {
       override val commandName = "device.my.feature"
       override suspend fun invoke(params: JsonObject, session: GatewayNodeSession): JsonObject {
           // 長時間処理はwithContext(Dispatchers.IO)で非同期化すること
           return withContext(Dispatchers.IO) {
               buildJsonObject { put("status", "ok") }
           }
       }
   }
   ```
2. `InvokeCommandRegistry` にハンドラを登録する
3. アプリ起動時に `GatewayNodeSession` でゲートウェイに接続し、ケイパビリティを宣言する
4. ゲートウェイ管理UIでAndroidノードが表示されケイパビリティが認識されることを確認する
5. プラグインマニフェストにエージェントツールとしてコマンド名を宣言する

### CanvasA2UIでリッチUIを表示する
1. エージェントがCanvasアクションをJSONL形式で生成する（1行=1アクション）
   ```jsonl
   {"type":"renderText","content":"分析結果を表示します"}
   {"type":"showImage","base64":"...","width":640,"height":480}
   {"type":"renderButton","label":"再撮影","action":"camera.capture"}
   ```
2. ゲートウェイが `GatewayChannel` 経由でクライアントにストリーミングする
3. iOSの `CanvasSession` がJSONLを1行ずつ受信してインクリメンタルレンダリングする
4. ユーザーのボタンタップ等のインタラクションがゲートウェイ経由でエージェントにフィードバックされる

## 注意点
- **4ファイル分離を絶対に崩さないこと**: `contract-api.ts`（型定義）→`setup-api.ts`（起動時登録）→`runtime-api.ts`（実行時処理）→`channel-config-api.ts`（設定スキーマ）のライフサイクル分離を破ると、ビルド時と実行時の型安全性が失われる。`runtime-api.ts`から`contract-api.ts`の実装詳細を直接importすると循環依存エラーになる
- **TLSピニングはTOFU方式**: 初回接続で証明書をピン留めする。ゲートウェイの証明書を更新した場合、全モバイルクライアントで再ペアリング（QRコード再スキャン）が必要。証明書更新前にクライアント側で `gateway.unpinCertificate()` を呼ぶと再ペアリングなしで移行可能
- **ExecApprovalsのバイパス厳禁**: `defaultPolicy: "require-approval"` を `"auto-approve"` に変更するとシェルインジェクションのリスクが生じる。allowlistは最小権限で、globパターン（`git *`）よりも完全一致（`git status`）を優先すること
- **JSONL順序の保証**: CanvasA2UIのストリーミングはJSONL行の到着順でレンダリングされる。`Promise.all` で並列送信すると順序が崩れてUIが壊れる。必ず逐次送信（`for...of` + `await`）を使うこと
- **セッションコンパクション中のコンテキスト消失**: `compact()` 実行中は `preserveLastN` と `mustPreserve` 以外のコンテキストにアクセスできない。重要なステート（ユーザー名・進行中タスク）は `mustPreserve` に明示的に含めること
- **Bonjour探索はLAN限定**: QRコードペアリングはゲートウェイとクライアントが同一ネットワーク上にある前提。リモート接続には `gateway.config.json` で `"remoteAccess": true` とTailscale/Cloudflare Tunnel等の設定が必要
- **プラグインIDの重複**: `openclaw.plugin.json` の `id` が既存プラグインと重複すると、`PluginLoadError: Duplicate plugin id "xxx"` で起動に失敗する。命名規則は `{vendor}-{feature}`（例: `acme-slack-channel`）を推奨
- **SKILL.mdトリガーの肥大化**: triggersがシステムプロンプトに全注入されるため、スキルごとに3〜5個が上限。10個以上あるとコンテキストウィンドウの5%以上を消費してエージェントの応答品質が劣化する
- **Android InvokeDispatcherのタイムアウト**: `CommandHandler.invoke()` が同期的に30秒以上かかると `GatewayTimeoutException` が発生する。カメラ撮影・ファイルダウンロード等の長時間処理は必ず `withContext(Dispatchers.IO)` でコルーチン化すること
- **OpenClawKit SPMの最小バージョン**: `OpenClawKit` はSwift 5.9+/iOS 16+が必須。`Package.swift` の `platforms` 設定が不足すると `Compiling for iOS 15.0, but module 'OpenClawKit' has a minimum deployment target of iOS 16.0` エラーになる

## 関連スキル
- **playwright-cli**: OpenClawのブラウザプラグインはPlaywrightベース。ref番号によるスナップショット操作・CDP proxyのパターンが共通する
- **ai**: ゲートウェイのLLMプロバイダー統合でVercel AI SDKの `generateText`・`streamText` パターンを参考にできる
- **n8n** / **n8n-as-code**: マルチエージェントワークフローの外部オーケストレーションにn8nのWebhookトリガー・HTTP Requestノードを組み合わせて使う
- **mastra**: エージェントフレームワークとしてのツール定義・ワークフロー構築パターンが類似する
- **supabase**: チャット履歴・ユーザー設定の永続化バックエンドとしてSupabase Auth/Database/Realtimeを統合する場合に参照する
```
