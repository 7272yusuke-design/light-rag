---
source: https://github.com/EtienneLescot/n8n-as-code
category: tool
sub_categories: [workflow, agent]
tags: [typescript, n8n, gitops, monorepo, vscode-extension, cli, workflow-automation, mcp]
language: 
ingested: 2026-04-09
source_updated: unknown
status: active
---

# n8n-as-code

# n8n-as-code

## 基本情報
- リポジトリ: https://github.com/EtienneLescot/n8n-as-code
- カテゴリ: tool
- サブカテゴリ: workflow, agent
- タグ: typescript, n8n, gitops, monorepo, vscode-extension, cli, workflow-automation, mcp
- 最終確認日: 2026-04-09

## 概要
n8n-as-code (n8nac) はn8nワークフローをTypeScriptコードとしてバージョン管理・同期するためのモノレポツールキット。CLI・VSCode拡張・AIスキル・MCPサーバーを含み、ローカルファイルとn8nインスタンス間の3-wayマージ同期を実現する。

## 設計思想
関心の分離を徹底した3-wayマージアーキテクチャ。Watcherは状態を観察するだけ（読み取り専用）、SyncEngineはI/O操作のみを実行し、SyncManagerが全体を調整する。CLIコアにsyncエンジンを埋め込み、VSCode拡張やAIツールが同じビジネスロジックを再利用するモノレポ設計。

## 主要コンポーネント
- CLI (n8nac): ワークフローのinit/list/push/pull/sync等のgitライクなコマンドを提供するエントリーポイント
- SyncEngine: n8nインスタンスとローカルファイル間の実際のI/O操作を実行するステートレスエグゼキュータ
- SyncManager: Watcher・SyncEngine・ResolutionManagerを調整するハイレベルオーケストレータ
- StateManager: .n8n-state.jsonを管理し3-wayマージのためのベース状態を追跡
- @n8n-as-code/skills: AIエージェント向けのノードスキーマ検索・コンテキスト生成・MCP統合を提供するライブラリ
- @n8n-as-code/transformer: TypeScriptデコレータとJSON間のワークフロー変換コンパイラ
- VSCode Extension: ワークフローツリービュー・n8nキャンバスWebview・プロキシサービスを持つエディタ統合
- Claude Plugin / OpenClaw Plugin: packages/skillsから生成されるAIエージェントスキルの配布アーティファクト

## 実装パターン
- 3-Way Merge Sync: localHash・remoteHash・lastSyncedHash（ベース）のSHA-256比較により競合をDeterministicに検出。両側が変更された場合のみCONFLICTと判定する
- Embedded Core Library: syncエンジンをCLIパッケージ内に埋め込み、VSCode拡張がCLIをインポートして同じロジックを再利用するアーキテクチャ
- TypeScript Decorator Workflow: @Workflow/@Nodeデコレータを使いTypeScriptでn8nワークフローを記述し、コンパイラがJSON形式に変換する
- Commit-driven Release: Conventional Commitsからバージョンバンプを自動計算し、nextブランチでプレリリース、mainブランチで安定版を独立してリリースする
- AI Context Generation: AiContextGeneratorがAGENTS.md・VSCodeスニペット・Claudeスキルを同一ソースから生成し一貫性を保つ

## 適用シーン
n8nワークフローをGitで管理したいチーム、CI/CDパイプラインにワークフロー変更を組み込みたい場合、AI（Claude・Cursor・Copilot等）を使ってn8nワークフローをTypeScriptで生成・管理したいプロジェクト、複数n8nインスタンスを管理するエンタープライズ環境。

## 注意点・制約
n8n REST APIへのアクセスが必須。ワークフロー同期時にクレデンシャル情報は除去されるため別途管理が必要。VSCode拡張はn8nキャンバスをWebviewでプロキシ経由表示するため、n8nインスタンスへのネットワーク到達性が前提。TypeScriptトランスフォーマーは一部のn8nノード構造に依存するため、n8nバージョンアップ時に互換性確認が必要。


## 関連ナレッジ
- (なし)
