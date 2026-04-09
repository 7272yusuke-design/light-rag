---
source: https://github.com/microsoft/playwright-cli
category: tool
sub_categories: [agent, workflow]
tags: [javascript, typescript, playwright, browser-automation, cli, test-generation, web-scraping, claude-code]
language: 
ingested: 2026-04-09
source_updated: unknown
status: active
---

# playwright-cli

# playwright-cli

## 基本情報
- リポジトリ: https://github.com/microsoft/playwright-cli
- カテゴリ: tool
- サブカテゴリ: agent, workflow
- タグ: javascript, typescript, playwright, browser-automation, cli, test-generation, web-scraping, claude-code
- 最終確認日: 2026-04-09

## 概要
playwright-cliはPlaywrightをCLIインターフェースで操作するためのツールで、AIコーディングエージェント向けにSKILL形式でブラウザ自動化を提供する。MCPと比較してトークン効率が高く、コンパクトなコマンド群でページ操作・テスト生成・ネットワークモック・動画録画などを実現する。

## 設計思想
LLMのコンテキストウィンドウ効率を最大化するため、MCPのようなリッチなツールスキーマではなくCLIコマンドとSKILLファイルを採用。各コマンドはPlaywright TypeScriptコードを自動生成し、インタラクティブな操作からテストコードへの変換をシームレスに行う。セッション分離・永続プロファイル・インメモリデフォルトでセキュリティと利便性を両立する。

## 主要コンポーネント
- playwright-cli.js: CLIエントリーポイント。Playwrightのprogramモジュールを介してコマンドを実行する。
- skills/playwright-cli/SKILL.md: コーディングエージェントが読み込む全コマンドのリファレンス定義ファイル。
- scripts/update.js: Playwright依存関係のバージョンアップ時にスキルとREADMEを自動同期するスクリプト。
- references/: テスト生成・リクエストモック・セッション管理・動画録画などのユースケース別詳細ガイド群。
- .claude/skills/: Claude Code向けのdevスキル定義。依存関係ロールアップ手順を含む。

## 実装パターン
- SKILL-based agent integration: playwright-cli install --skillsでエージェントのワークスペースにSKILLファイルをインストールし、エージェントがCLIコマンドを自律的に使用できるようにする。
- ref-based element targeting: snapshotコマンドでe1/e2形式のref番号を取得し、以降のコマンドでそのrefを指定してDOM要素を操作する。CSS/ロールロケータも併用可能。
- code generation on action: すべてのCLI操作がPlaywright TypeScriptコードを自動出力し、そのままテストファイルへコピー可能にする。
- named session isolation: -s=nameフラグで複数の独立したブラウザコンテキストを並列管理し、Cookie/ストレージを分離する。
- run-code escape hatch: CLIコマンドでカバーできない高度なシナリオにrun-codeでPlaywrightの任意のコードを直接実行できるエスケープハッチを提供する。

## 適用シーン
AIコーディングエージェント(Claude Code, GitHub Copilotなど)によるWebアプリのE2Eテスト自動化、ブラウザ操作からのPlaywrightテストコード生成、Webスクレイピング、ネットワークモックを用いたフロントエンド開発、認証状態の保存・再利用、デバッグ用トレース・動画録画。

## 注意点・制約
CLIはPlaywright本体のmonorepoで開発されており、このリポジトリ自体はラッパーと配布パッケージ。動画録画やトレースはオーバーヘッドとディスク消費を伴う。デフォルトはヘッドレスかつインメモリセッションのため、永続化が必要な場合は--persistentフラグが必要。認証状態ファイルをgitにコミットしないよう注意が必要。


## 関連ナレッジ
- (なし)
