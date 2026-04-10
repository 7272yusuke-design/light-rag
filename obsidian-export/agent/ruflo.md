---
source: https://github.com/ruvnet/ruflo
category: agent
sub_categories: [framework, workflow]
tags: [TypeScript, JavaScript, Svelte, multi-agent, swarm-coordination, MCP, SPARC-methodology, Claude-AI]
language: 
ingested: 2026-04-10
source_updated: unknown
status: active
---

# ruflo

# ruflo

## 基本情報
- リポジトリ: https://github.com/ruvnet/ruflo
- カテゴリ: agent
- サブカテゴリ: framework, workflow
- タグ: TypeScript, JavaScript, Svelte, multi-agent, swarm-coordination, MCP, SPARC-methodology, Claude-AI
- 最終確認日: 2026-04-10

## 概要
Claude-Flowは、Claude AIを活用したマルチエージェントスワームオーケストレーションフレームワークで、SPARC方法論に基づいて複数のAIエージェントを協調させて複雑なタスクを自動化する。SPARCコマンド群、Hive-Mindアーキテクチャ、MCP(Model Context Protocol)統合、メモリ管理機能などを提供し、ソフトウェア開発・コードレビュー・GitHub操作などを自律的に実行できる。また、Rufloというフォークされたチャットインターフェース(SvelteKitベース)も内包し、MCPツールをブリッジ経由で利用可能にしている。

## 設計思想
SPARCメソドロジー(Specification, Pseudocode, Architecture, Refinement, Completion)を中心に、Queen-Worker階層型スワーム、Hive-Mind集合知、コンセンサスアルゴリズム(Raft/Byzantine/Gossip/CRDT)などの分散協調パターンを組み合わせる。エージェントはスキル(SKILL.md)とコマンド(slash commands)で定義・拡張可能で、メモリの永続化とチェックポイントによる長時間タスクのサポートを重視する。

## 主要コンポーネント
- SPARC Commands: コーダー・アーキテクト・TDD・デバッガーなど役割別エージェントを起動するCLIコマンド群
- Hive-Mind / Swarm Orchestrator: Queen-Workerパターンで複数エージェントを階層的に管理・調整するオーケストレーター
- MCP Bridge (mcp-bridge): MCPプロトコルをHTTP/stdio経由でブリッジし、外部ツールをエージェントに統合
- Skills / Agents Directory: 再利用可能なエージェント定義(SKILL.md)と.claude/agentsのMarkdown仕様ファイル群
- Memory & Checkpoint System: エージェントの記憶をベクトル検索・永続化・チェックポイントで管理するメモリ基盤
- Ruvocal / Ruflo Chat UI: SvelteKit製チャットインターフェースのフォーク。複数LLMバックエンドとMCPツールを統合したUI
- Consensus Coordinators: Raft・Byzantine・Gossip・CRDTなど分散合意アルゴリズムを実装したコーディネーター群

## 実装パターン
- SPARC Methodology: 仕様→擬似コード→アーキテクチャ→改善→完成の5段階でエージェントタスクを構造化する開発フロー
- Queen-Worker Swarm: Queen Coordinatorがタスクを分解しWorker Specialistに委譲、結果を集約するヒエラルキー型スワームパターン
- Skill-based Agent Definition: SKILL.mdファイルでエージェントの能力・制約・使用ツールを宣言的に定義し再利用可能にするパターン
- MCP Tool Integration: Model Context Protocolを通じて外部ツール(GitHub API・DB・検索等)をエージェントに統合するブリッジパターン
- Checkpoint-based Recovery: 長時間実行タスクをJSONチェックポイントで定期保存し、障害時に再開可能にするパターン

## 適用シーン
大規模なソフトウェア開発タスクの自動化(コードレビュー・PR管理・リリース管理)、複数リポジトリにまたがる開発オーケストレーション、AI駆動のシステム設計・アーキテクチャ策定、自律的なGitHub Issue/PRトリアージ、チャットUIを介したマルチモデル・マルチツールAIアシスタントの構築。

## 注意点・制約
チェックポイントファイルが膨大(数百〜数千個)になりリポジトリが肥大化しやすい。SPARCメソドロジーやエージェント定義がMDファイルに分散しており学習コストが高い。MCP Bridgeや各種コーディネーターの依存関係が複雑で、セットアップに手順が多い。Ruflo/Ruvocalチャットは別途Dockerや環境構築が必要。


## 関連ナレッジ
- (なし)
