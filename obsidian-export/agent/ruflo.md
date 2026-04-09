---
source: https://github.com/ruvnet/ruflo
category: agent
sub_categories: [framework, workflow]
tags: [TypeScript, JavaScript, Svelte, multi-agent, swarm, MCP, SPARC, hive-mind]
language: 
ingested: 2026-04-09
source_updated: unknown
status: active
---

# ruflo

# ruflo

## 基本情報
- リポジトリ: https://github.com/ruvnet/ruflo
- カテゴリ: agent
- サブカテゴリ: framework, workflow
- タグ: TypeScript, JavaScript, Svelte, multi-agent, swarm, MCP, SPARC, hive-mind
- 最終確認日: 2026-04-09

## 概要
Claude-Flowは、Claude AIを活用したマルチエージェントオーケストレーションフレームワークで、SPARCメソドロジーに基づくエージェントスウォーム、ハイブマインド、メモリ管理などの高度な協調パターンを提供する。rufloサブプロジェクトとして、HuggingFace Chat UIをフォークしたSvelteKit製のチャットWebアプリも含む。MCPプロトコルを介した外部ツール連携やGitHub自動化ワークフローも統合されている。

## 設計思想
SPARCメソドロジー（Specification, Pseudocode, Architecture, Refinement, Completion）を中心に据え、専門化されたエージェント（planner, coder, reviewer, tester等）が階層的・メッシュ状・ハイブマインド型などの複数のトポロジーで協調動作する。Byzantine Fault Tolerance、RAFT、CRDTなどの分散システム合意アルゴリズムをエージェント間調整に応用し、高可用・自己修復的なマルチエージェント環境を実現する。

## 主要コンポーネント
- SPARC Agents: specification/pseudocode/architecture/refinement/coderの各フェーズを担う専門エージェント群
- Hive Mind System: Queen Coordinator, Scout Explorer, Worker Specialistによる集合知コーディネーション
- Swarm Orchestrator: 階層的・メッシュ・アダプティブなスウォームトポロジーの管理と負荷分散
- MCP Bridge: Model Context Protocolによる外部ツール・サービスとの接続レイヤー
- Memory Manager: セッション横断の知識永続化・ベクトル検索・AgentDB連携
- ruflo/ruvocal: SvelteKit製チャットUI、OpenAI互換エンドポイント、マルチモデルルーティング
- Consensus Coordinators: RAFT/CRDT/Byzantine/Gossipプロトコルによるエージェント間合意形成
- GitHub Automation: PR管理・コードレビュー・リリース・Issue追跡の自動化エージェント群

## 実装パターン
- SPARC Methodology: Specification→Pseudocode→Architecture→Refinement→Completionの5段階でタスクを構造化し、各フェーズに専門エージェントを割り当てる
- Swarm Topology Selection: タスク特性に応じてhierarchical/mesh/adaptive/hive-mindのトポロジーを動的に選択し、エージェントを配置する
- Hook-based Automation: pre-task/post-task/pre-edit/post-editフックでセッション横断メモリ保存・チェックポイント・学習最適化を自動実行
- Consensus-based Coordination: Byzantine Fault Tolerance、Quorum Management、CRDT同期によって分散エージェント間の一貫性を保証
- Skill Registry Pattern: .agents/skillsと.claude/skillsに分離されたSKILL.mdファイル群でエージェントの能力・手順・制約を宣言的に定義
- Stream Chain Pipeline: 非同期ジェネレータのチェーンでテキスト生成・ツール呼び出し・推論ステップを逐次処理

## 適用シーン
大規模コードベースの自律的開発・レビュー・リファクタリング、GitHub リポジトリの自動管理、マルチモデル対応チャットUIの構築、分散エージェントによる研究・分析タスクの並列実行、CI/CDパイプラインへのAIエージェント統合

## 注意点・制約
checkpoint JSONファイルが数千個生成される設計のためストレージ消費が大きい。v2/v3の複数バージョンが並存しており移行中の状態。ruflo/ruvocalはHuggingFace Chat UIのフォークであるため上流の変更追従コストが発生する。MCP Bridgeはローカル/クラウド混在構成に対応するが、セキュリティ境界の設定が複雑。


## 関連ナレッジ
- (なし)
