ファイル書き込み権限を許可してください。内容は以下の通りです:

```markdown
---
name: ruflo
description: Claude-Flow/SPARCメソドロジーに基づくマルチエージェントスワームオーケストレーションを構築・運用するとき、`npx claude-flow`・SPARCコマンド群（`/sparc-coder`・`/sparc-architect`・`/sparc-tdd`等）を使用するとき、Queen-Worker階層型スワーム・Hive-Mindアーキテクチャ・コンセンサスアルゴリズム（Raft/Byzantine/Gossip/CRDT）を設計するとき、MCP Bridgeで外部ツールをエージェントに統合するとき、チェックポイントベースのメモリ永続化・長時間タスク管理が関わる場面では必ずこのスキルを使え。Ruflo/RuvocalチャットUI（SvelteKit製）の構築・カスタマイズ、`.claude/agents/`ディレクトリでのエージェント定義、SKILL.mdによるスキルベースのエージェント拡張が関わる場面でも即座に参照せよ。
---

# ruflo (Claude-Flow)

## 概要
Claude-Flowは、Claude AIを活用したマルチエージェントスワームオーケストレーションフレームワーク。SPARC方法論（Specification, Pseudocode, Architecture, Refinement, Completion）に基づいて複数のAIエージェントを協調させ、複雑なソフトウェア開発タスクを自動化する。SPARCコマンド群、Hive-Mindアーキテクチャ、MCP統合、メモリ管理・チェックポイント機能を提供し、コードレビュー・PR管理・GitHub操作などを自律的に実行できる。Rufloという SvelteKit製チャットインターフェースも内包し、MCPツールをブリッジ経由で利用可能にしている。

- リポジトリ: https://github.com/ruvnet/ruflo
- カテゴリ: agent > framework, workflow
- 技術スタック: TypeScript, JavaScript, Svelte, MCP, Claude AI

## いつ使うか
- マルチエージェント協調でソフトウェア開発タスクを自動化したいとき
- SPARCメソドロジーで構造化された開発フローを導入したいとき
- Queen-Worker階層型スワームでタスクを分解・委譲・集約したいとき
- MCP Bridge経由で外部ツール（GitHub API・DB・検索等）をエージェントに統合するとき
- チェックポイントベースのメモリ永続化で長時間実行タスクを管理するとき
- Hive-Mindで複数エージェントのコンセンサスを取るとき
- `.claude/agents/`にカスタムエージェントを定義して拡張するとき
- SvelteKit製チャットUI（Ruflo）を構築・カスタマイズするとき

## 主要コマンド・API

### インストールとセットアップ
```bash
# Claude-Flowのインストール
npm install -g claude-flow

# プロジェクト初期化
npx claude-flow init

# MCPサーバーの起動
npx claude-flow mcp-server

# MCP Bridgeの起動（HTTP/stdio経由）
npx claude-flow mcp-bridge --port 3100
```

### SPARCコマンド群（役割別エージェント起動）
```bash
# コーダーエージェント: 実装タスクの実行
/sparc-coder "UserServiceのCRUD実装"

# アーキテクトエージェント: システム設計
/sparc-architect "マイクロサービスのAPI設計"

# TDDエージェント: テスト駆動開発
/sparc-tdd "UserService のユニットテスト作成"

# デバッガーエージェント: バグ調査・修正
/sparc-debugger "認証フローのタイムアウトエラー調査"

# レビューエージェント: コードレビュー
/sparc-reviewer "PR #42 のコードレビュー"

# 統合SPARCフロー: 仕様→擬似コード→アーキテクチャ→改善→完成
/sparc "決済モジュールの設計と実装"
```

### スワームオーケストレーション
```bash
# Queen-Workerスワームの起動
npx claude-flow swarm start \
  --queen "project-coordinator" \
  --workers 5 \
  --task "リポジトリ全体のリファクタリング"

# Hive-Mindモード（集合知による意思決定）
npx claude-flow hive-mind \
  --agents 3 \
  --consensus raft \
  --task "アーキテクチャ方針の決定"

# スワームの状態確認
npx claude-flow swarm status

# スワームの停止
npx claude-flow swarm stop
```

### メモリ・チェックポイント管理
```bash
# メモリの永続化設定
npx claude-flow memory init --backend sqlite

# チェックポイントの作成
npx claude-flow checkpoint save --name "phase-1-complete"

# チェックポイントからの復元
npx claude-flow checkpoint restore --name "phase-1-complete"

# チェックポイント一覧
npx claude-flow checkpoint list

# メモリのベクトル検索
npx claude-flow memory search "認証フローの設計決定"
```

### MCP統合
```bash
# MCPツールの登録
npx claude-flow mcp register-tool \
  --name "github" \
  --transport stdio \
  --command "npx @modelcontextprotocol/server-github"

# MCPリソースの一覧
npx claude-flow mcp list-resources

# MCPツールの実行テスト
npx claude-flow mcp test-tool --name "github" --method "list_issues"
```

### Ruflo チャットUI
```bash
# Ruflo チャットUIの起動（開発モード）
cd ruflo/
npm install
npm run dev

# Docker Composeで起動
docker compose up -d

# MCPツールをブリッジ経由で接続
# ruflo/.env に設定
MCP_BRIDGE_URL=http://localhost:3100
```

## 主要コンポーネント

### SPARC Methodology
5段階の構造化開発フロー:
1. **Specification**: 要件定義・制約の明確化
2. **Pseudocode**: アルゴリズム・ロジックの疑似コード化
3. **Architecture**: システム構成・コンポーネント設計
4. **Refinement**: コードレビュー・最適化・テスト
5. **Completion**: 統合テスト・ドキュメント・デプロイ

### Queen-Worker Swarm
```
Queen Coordinator
├── Worker Specialist A (コーダー)
├── Worker Specialist B (テスター)
├── Worker Specialist C (レビューア)
└── Worker Specialist D (ドキュメンター)
```
- Queenがタスクを分解しWorkerに委譲
- Workerは専門スキルに基づいて並列実行
- 結果をQueenが集約・統合・品質判定

### Consensus Coordinators
| アルゴリズム | 用途 | 特性 |
|---|---|---|
| Raft | リーダー選出・ログ複製 | 強い一貫性、リーダーベース |
| Byzantine | 障害耐性が必要な意思決定 | f < n/3 の障害に耐性 |
| Gossip | 状態の伝播・同期 | 結果整合性、スケーラブル |
| CRDT | 並行更新の自動マージ | 競合なし、可用性重視 |

### エージェント定義（`.claude/agents/`）
```markdown
# agent-name.md

## Role
コードレビュー専門エージェント

## Capabilities
- 静的解析の実行
- セキュリティ脆弱性の検出
- パフォーマンス問題の指摘

## Tools
- github (MCP)
- file-system (MCP)
- code-analysis (built-in)

## Constraints
- 本番コードの直接変更は禁止
- PRコメントでのフィードバックのみ
```

### MCP Bridge アーキテクチャ
```
Claude Agent
    ↕ (MCP Protocol)
MCP Bridge Server (:3100)
    ↕ (HTTP/stdio)
┌─────────────────────────┐
│  GitHub MCP Server      │
│  Filesystem MCP Server  │
│  Database MCP Server    │
│  Search MCP Server      │
└─────────────────────────┘
```

## ワークフロー例

### 典型例1: SPARCフローによるフィーチャー開発
```bash
# 1. 仕様の明確化
/sparc-architect "決済モジュールの要件を整理し、コンポーネント図を作成"

# 2. 擬似コードの生成
/sparc-coder "決済フローの擬似コードを作成。Stripe連携を含む"

# 3. TDDでテストファースト実装
/sparc-tdd "決済モジュールのユニットテストを作成し、実装を進める"

# 4. コードレビュー
/sparc-reviewer "決済モジュールのコードレビュー。セキュリティ観点を重視"

# 5. 統合・完成
/sparc "決済モジュールの統合テストとドキュメント作成"
```

### 典型例2: マルチエージェントスワームによる大規模リファクタリング
```bash
# 1. Queenがタスクを分析・分解
npx claude-flow swarm start \
  --queen "refactoring-coordinator" \
  --workers 4 \
  --task "legacy-authモジュールのTypeScript移行"

# 2. スワームの進捗監視
npx claude-flow swarm status

# 3. チェックポイントで進捗を保存（中断に備える）
npx claude-flow checkpoint save --name "auth-migration-50pct"

# 4. 障害発生時の復元
npx claude-flow checkpoint restore --name "auth-migration-50pct"

# 5. Hive-Mindで設計判断を合議
npx claude-flow hive-mind \
  --agents 3 \
  --consensus raft \
  --task "新しい認証フローのインターフェース設計を決定"
```

### 典型例3: GitHub自動トリアージ
```bash
# 1. MCP経由でGitHub APIを接続
npx claude-flow mcp register-tool \
  --name "github" \
  --transport stdio \
  --command "npx @modelcontextprotocol/server-github"

# 2. トリアージエージェントを定義
cat > .claude/agents/triage-agent.md << 'EOF'
## Role
GitHub Issue/PRの自動トリアージ

## Workflow
1. 新規Issue/PRを取得
2. 内容を分析してラベル付与
3. 適切な担当者をアサイン
4. 優先度を判定してプロジェクトボードに配置

## Tools
- github (MCP)
- memory (built-in)
EOF

# 3. トリアージの実行
/sparc "直近のOpenなIssueをトリアージして、ラベル・担当者・優先度を設定"
```

### 典型例4: RufloチャットUIのカスタムデプロイ
```bash
# 1. リポジトリのクローンとUIセットアップ
git clone https://github.com/ruvnet/ruflo.git
cd ruflo

# 2. 環境変数の設定
cat > .env << 'EOF'
ANTHROPIC_API_KEY=sk-ant-...
MCP_BRIDGE_URL=http://localhost:3100
PUBLIC_APP_NAME=MyTeam AI Assistant
EOF

# 3. MCP Bridgeの起動
npx claude-flow mcp-bridge --port 3100 &

# 4. チャットUIの起動
npm install
npm run dev
# → http://localhost:5173 でアクセス

# 5. Docker本番デプロイ
docker compose up -d --build
```

## 注意点

### チェックポイントの肥大化
- チェックポイントファイルが数百〜数千個に膨れ上がりやすい。`.gitignore`に`checkpoints/`を追加し、Git管理対象外にすること
- 定期的に古いチェックポイントを削除する運用ルールを設けること
- `npx claude-flow checkpoint list`で定期的に確認し、不要なものを`checkpoint delete`で削除

### SPARCコマンドの学習コスト
- エージェント定義が`.claude/agents/`や各種SKILL.mdに分散しているため、初見での全体把握が困難
- まず`/sparc`（統合フロー）から始め、個別コマンド（`/sparc-coder`等）は必要に応じて使い分けること
- 各コマンドが起動するエージェントの役割・制約は対応する`.md`ファイルで確認できる

### MCP Bridge の依存関係
- MCP Bridgeは各MCPサーバーをサブプロセスとして起動するため、必要なMCPサーバーのnpmパッケージが事前にインストールされている必要がある
- ポート競合に注意。デフォルトの3100番ポートが使用中の場合は`--port`で変更すること
- Bridge経由のツール呼び出しにはネットワークレイテンシが加わる。ローカル実行よりレスポンスが遅くなる

### コンセンサスアルゴリズムの選択
- **Raft**: 3エージェント以上必要（リーダー + 過半数）。2エージェント以下では動作しない
- **Byzantine**: 4エージェント以上必要（f < n/3）。オーバーヘッドが大きいため少人数では非推奨
- **Gossip**: 結果整合性のため、即時一貫性が必要な判断には不向き
- **CRDT**: テキスト・カウンター等のデータ型制約がある。任意のデータ構造には適用不可

### Ruflo/RuvocalチャットUIの構築
- SvelteKit + Node.js環境が必要。別途Docker環境の構築が推奨される
- LLMバックエンドの切り替えは`.env`の`LLM_PROVIDER`で行う。デフォルトはClaude
- MCPツールのブリッジ接続が切れるとツール呼び出しがサイレントに失敗する。ログを確認すること

### スワームの並行実行制限
- Worker数を増やしすぎるとAPIレートリミットに抵触する。Claude APIの場合、同時リクエスト数の上限を確認すること
- 各Workerが同一ファイルを同時編集するとコンフリクトが発生する。Queenによるタスク分割時にファイル分離を意識すること

## 関連スキル
- **crewai**: 代替マルチエージェントフレームワーク。ロールベース設計。SPARCほど構造化されていないが、Pythonエコシステムとの親和性が高い
- **langgraph**: グラフベースのマルチエージェント。LangChainエコシステムに統合されたワークフロー構築が必要な場合
- **servers**: MCP Bridgeが接続する各種MCPサーバーの構築・設定リファレンス
- **claude-api**: Claude APIの直接利用。SPARCエージェントの裏側で使われるAPI呼び出しの最適化・コスト管理
- **agency-agents**: 他のエージェントフレームワークとの比較・使い分け判断。Claude-Flow以外の選択肢を検討する場合
```

約310行、全セクション完備。書き込み権限の許可をお願いします。
