---
source: https://github.com/kepano/obsidian-skills
category: agent
sub_categories: [tool, workflow]
tags: [obsidian, markdown, PKM, claude-code, agent-skills, YAML, json-canvas, knowledge-management]
language: 
ingested: 2026-04-09
source_updated: unknown
status: active
---

# obsidian-skills

# obsidian-skills

## 基本情報
- リポジトリ: https://github.com/kepano/obsidian-skills
- カテゴリ: agent
- サブカテゴリ: tool, workflow
- タグ: obsidian, markdown, PKM, claude-code, agent-skills, YAML, json-canvas, knowledge-management
- 最終確認日: 2026-04-09

## 概要
ObsidianのVaultファイル（.md、.base、.canvas）をAIエージェントが操作するためのSkillパッケージ。Claude CodeやCodex CLIなどのSkill対応エージェントで使用でき、Obsidian Flavored Markdown、Bases、JSON Canvas、CLIコマンドの知識をエージェントに付与する。

## 設計思想
Agent Skills仕様に準拠したSkillファイル（SKILL.md）群として設計され、各ドメイン（Markdown記法、Bases、Canvas、CLI）を独立したSkillとして分離。エージェントが必要な知識のみを選択的にロードできるモジュール構造を採用。参照ドキュメントをreferences/サブディレクトリに分離することで、メインSkillの可読性と詳細リファレンスの両立を実現。

## 主要コンポーネント
- obsidian-markdown: Wikiリンク、埋め込み、コールアウト、フロントマターなどObsidian固有のMarkdown拡張構文をエージェントに教示
- obsidian-bases: .baseファイルのYAMLスキーマ、フィルタ構文、数式、ビュー設定をエージェントに教示
- json-canvas: .canvasファイルのノード・エッジ構造、ID生成、レイアウト規則をエージェントに教示
- obsidian-cli: Obsidian CLIコマンドによるVault操作とプラグイン開発ワークフローをエージェントに教示
- defuddle: WebページからクリーンなMarkdownを抽出するCLIツールの使用方法をエージェントに教示
- plugin.json / marketplace.json: Agent Skillsマーケットプレイス向けのメタデータ定義

## 実装パターン
- SKILL.mdフロントマター定義: 各Skillファイルの先頭にname/descriptionをYAMLフロントマターとして記述し、エージェントがSkillをいつ使用するかのトリガー条件を明示するパターン
- 主Skill＋referencesサブディレクトリ: 頻用情報はSKILL.mdに、詳細リファレンス（全関数一覧、コールアウト型一覧など）はreferences/配下の別ファイルに分離するドキュメント構造パターン
- ワークフロー番号付きステップ: Skillドキュメント内でCreate/Edit/Validateの手順を番号付きリストで明示し、エージェントが一貫した操作手順を踏めるよう誘導するパターン
- バリデーションチェックリスト: ファイル生成・編集後に検証すべき項目を明示的なチェックリストとして提供し、エージェントの出力品質を担保するパターン

## 適用シーン
ObsidianのVault上でAIエージェントを使って自動的にノート作成・編集・整理を行いたいプロジェクト。Claude CodeをObsidian Vaultのルートで使用してMarkdownノートやBaseデータベース、Canvasマインドマップを生成・管理したい場合。Obsidianプラグイン・テーマの開発自動化にも活用できる。

## 注意点・制約
Obsidianが起動中でないとobsidian-cli skillは動作しない。Agent Skills仕様準拠のエージェント（Claude Code、Codex CLIなど）でのみ動作し、汎用LLMAPIへの直接投入は想定外。defuddleは別途npm install -g defuddleが必要。obsidian-basesはObsidian Bases機能（比較的新しい機能）が有効な環境のみ対応。


## 関連ナレッジ
- (なし)
