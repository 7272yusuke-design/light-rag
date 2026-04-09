---
source: https://github.com/microsoft/playwright-cli
category: tool
sub_categories: [agent, workflow]
tags: [javascript, playwright, browser-automation, CLI, test-generation, claude-code, nodejs, skills]
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
- タグ: javascript, playwright, browser-automation, CLI, test-generation, claude-code, nodejs, skills
- 最終確認日: 2026-04-09

## 概要
playwright-cliはPlaywrightをCLIコマンドとして操作できるツールで、コーディングエージェント（Claude Code等）向けにSKILLS形式で提供される。ブラウザ自動化・テスト生成・ネットワークモック・セッション管理・動画録画など豊富な操作をトークン効率よく実行できる。MCPに比べてコンテキストウィンドウを節約しながらブラウザ自動化を行うことに特化している。

## 設計思想
LLMコーディングエージェントのトークン効率を最優先とし、大きなツールスキーマやアクセシビリティツリーをモデルコンテキストに読み込まない設計。SKILLSファイル（Markdown）をエージェントに提供することで、CLIコマンドの使い方を簡潔に伝えるアーキテクチャ。セッション分離・永続プロファイル・並列ブラウザ操作を標準サポートし、Playwright本体に依存してCLI薄層として実装されている。

## 主要コンポーネント
- playwright-cli.js: CLIエントリポイント。Playwrightのプログラムモジュールを呼び出す薄いラッパー
- skills/playwright-cli/SKILL.md: エージェント向けスキル定義。全コマンドのリファレンスとして機能するソースオブトゥルース
- skills/playwright-cli/references/: テスト生成・リクエストモック・セッション管理・トレース・動画録画など機能別の詳細リファレンス群
- scripts/update.js: Playwright依存バージョン更新時にスキルファイルとREADMEを同期する自動化スクリプト
- .claude/skills/dev/: リポジトリメンテナンス（依存バージョンのロール等）向け開発者用スキル定義

## 実装パターン
- SKILL-driven CLI: Markdownで記述されたSKILLSファイルをエージェントにインストールし、CLIコマンドの使い方をコンテキスト効率よく提供するパターン
- ref-based element targeting: スナップショットから取得したref（e1, e2...）を使って要素を指定することで、DOM構造をLLMコンテキストに大量展開せずに操作するパターン
- named session isolation: -s=フラグでブラウザセッションを名前で分離し、クッキー・ストレージ・履歴を独立させて並列操作するパターン
- run-code escape hatch: CLIコマンドでカバーできない高度なシナリオをrun-codeで任意のPlaywright TypeScriptコードを実行して対応するパターン
- code generation on action: CLIで実行した各アクションに対応するPlaywright TypeScriptコードが自動出力され、テストファイルに直接コピーできるパターン

## 適用シーン
Claude CodeやGitHub CopilotなどのコーディングエージェントによるWebアプリのE2Eテスト自動化・テストコード生成・ブラウザ操作の自動化に最適。トークン消費を抑えながらブラウザ自動化を行いたいエージェントワークフロー、複数サイトの並列スクレイピング、認証状態の保存・再利用が必要なテストシナリオに有用。

## 注意点・制約
CLIはPlaywright本体（playwright npm package）に強く依存しており、バージョン追随のためのロール作業が定期的に必要。グローバルインストールが必要な場合あり（npxフォールバックあり）。ヘッドレスがデフォルトのため視覚確認には--headedフラグが必要。セッションはデフォルトでインメモリのみで永続化にはオプション指定が必要。MCP比で永続的なブラウザコンテキストや豊富な内省機能は劣る。


## 関連ナレッジ
- (なし)
