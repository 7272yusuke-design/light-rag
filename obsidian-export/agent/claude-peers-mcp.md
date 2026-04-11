---
source: https://github.com/louislva/claude-peers-mcp
category: agent
sub_categories: [protocol, tool]
tags: [typescript, bun, MCP, sqlite, peer-discovery, claude-code, inter-agent-messaging, daemon]
language: 
ingested: 2026-04-11
source_updated: unknown
status: active
---

# claude-peers-mcp

# claude-peers-mcp

## 基本情報
- リポジトリ: https://github.com/louislva/claude-peers-mcp
- カテゴリ: agent
- サブカテゴリ: protocol, tool
- タグ: typescript, bun, MCP, sqlite, peer-discovery, claude-code, inter-agent-messaging, daemon
- 最終確認日: 2026-04-11

## 概要
claude-peersは、複数のClaude Codeインスタンス間でピア探索とメッセージングを実現するMCPサーバーです。ブローカーデーモン（localhost:7899 + SQLite）を介して、異なるターミナルで動作するClaudeインスタンスが互いを発見し、リアルタイムでメッセージを送受信できます。

## 設計思想
シングルトンブローカーデーモンパターンを採用し、1マシンに1つのHTTP+SQLiteブローカーが自動起動する。各Claude CodeセッションはMCP stdioサーバーとして起動し、ブローカーに登録・通信する。claude/channelプロトコルを利用したプッシュ通知により、ポーリングなしでメッセージをリアルタイム配信する疎結合アーキテクチャ。

## 主要コンポーネント
- broker.ts: localhost:7899で動作するシングルトンHTTPデーモン。SQLiteでピア情報とメッセージを永続化し、死活監視・自動クリーンアップを行う
- server.ts: Claude Codeが起動するMCP stdioサーバー。ブローカーへの登録・ハートビート・メッセージポーリング・チャネルプッシュを担当
- shared/types.ts: ブローカーAPIのリクエスト/レスポンス型定義。PeerおよびMessageデータ構造を共有
- shared/summarize.ts: gpt-4o-nanoを使い、作業ディレクトリとgitコンテキストからインスタンスの作業概要を自動生成
- cli.ts: ブローカー状態確認・ピア一覧・メッセージ送信・ブローカー停止を行うCLIユーティリティ

## 実装パターン
- Singleton Broker Daemon: 1マシンに1プロセスのブローカーを自動起動し、MCPサーバーが起動時に生存確認→未起動なら起動するパターン
- Channel Push Notification: claude/channelプロトコルを使い、ポーリング結果をMCPセッションへプッシュし即時通知を実現
- PID-based Liveness Check: ピアのPIDに対しsignal 0を送りプロセス生存確認し、死亡ピアをSQLiteから自動削除
- Non-blocking Auto Summary: OpenAI APIによるサマリー生成をバックグラウンドで実行し、完了後にブローカーへ非同期更新することで起動をブロックしない

## 適用シーン
複数のClaude Codeセッションを並行して使う開発者が、セッション間でコンテキストを共有したり作業調整したりしたい場合。マルチエージェント協調ワークフローや、異なるリポジトリを跨いだClaude間通信が必要なプロジェクトに有用。

## 注意点・制約
claude/channelプロトコルはClaude Code v2.1.80以上かつclaude.aiログイン（APIキー認証不可）が必要。Auto Summaryは OPENAI_API_KEY が必要でgpt-4o-nanoモデルを使用。ブローカーはlocalhost限定のため同一マシン内でのみ動作する。


## 関連ナレッジ
- (なし)
