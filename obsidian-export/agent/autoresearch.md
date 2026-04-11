---
source: https://github.com/karpathy/autoresearch
category: agent
sub_categories: [workflow, framework]
tags: [python, pytorch, LLM-pretraining, hyperparameter-tuning, autonomous-research, BPE-tokenizer, Muon-optimizer, transformer]
language: 
ingested: 2026-04-11
source_updated: unknown
status: active
---

# autoresearch

# autoresearch

## 基本情報
- リポジトリ: https://github.com/karpathy/autoresearch
- カテゴリ: agent
- サブカテゴリ: workflow, framework
- タグ: python, pytorch, LLM-pretraining, hyperparameter-tuning, autonomous-research, BPE-tokenizer, Muon-optimizer, transformer
- 最終確認日: 2026-04-11

## 概要
自律的なLLM事前学習実験フレームワーク。AIエージェントがtrain.pyを反復的に修正し、5分間の固定タイムバジェットで学習を実行し、val_bpb（バリデーション bits per byte）を最小化するよう自律的にハイパーパラメータ・アーキテクチャを探索する。ユーザーが就寝中でも継続して実験を繰り返すことを想定した設計。

## 設計思想
単一ファイル（train.py）のみをエージェントが編集可能とし、評価・データロード・定数は prepare.py に固定することで実験の公平性を担保。固定5分タイムバジェットにより異なるアーキテクチャ間での直接比較を実現。シンプルさを明示的な設計基準とし、改善幅と複雑性のトレードオフを重視するgit-based keep/discard実験ループを採用。

## 主要コンポーネント
- train.py: エージェントが自由に編集するGPTモデル・オプティマイザ・学習ループの実装ファイル
- prepare.py: 固定評価ハーネス(evaluate_bpb)・データローダー・BPEトークナイザー・定数を含む読み取り専用ファイル
- program.md: エージェントへの実験プロトコル指示書（セットアップ・実験ループ・ロギング手順を定義）
- MuonAdamW: 2D行列パラメータにMuon、その他にAdamWを適用する複合オプティマイザ
- GPT: スライディングウィンドウアテンション・Value Embedding・RoPEを備えたトランスフォーマーモデル
- results.tsv: 実験結果（commit hash・val_bpb・メモリ・keep/discard・説明）を記録するログファイル
- analysis.ipynb: 実験結果の可視化・統計分析用Jupyterノートブック

## 実装パターン
- Git-based Keep/Discard Loop: 改善した場合はgitコミットを維持し、改善しなかった場合はgit resetで巻き戻す実験管理パターン
- Fixed Time Budget Training: エポック数ではなく壁時計5分を学習停止条件とすることでプラットフォーム間・実験間の公平な比較を実現
- BPB Metric Evaluation: 語彙サイズに依存しないbits-per-byteを評価指標とし、アーキテクチャ変更時も公平比較できるよう設計
- Best-fit Document Packing: BOS整列・ベストフィットビンパッキングによるパディングゼロの100%トークン利用率データローダー
- Sliding Window Attention Pattern: SSSL等のパターンでフル/ハーフコンテキストのウィンドウアテンションを層ごとに交互適用

## 適用シーン
単一GPUで自律的なモデルアーキテクチャ・ハイパーパラメータ探索を行いたい研究者や開発者。AIエージェントに一晩中実験を回させて朝に結果を確認するワークフローを構築したい場合。小規模LLM事前学習の実験基盤として、Muon最適化器やスライディングウィンドウアテンション等の技術を検証したい場合。

## 注意点・制約
単一NVIDIA GPUのみサポート（H100でテスト済み）。CPU・MPS非対応。固定タイムバジェットにより結果は実行プラットフォーム依存で他環境と非比較。prepare.pyおよび評価ハーネスは変更不可。新規パッケージのインストール不可。分散学習非対応。


## 関連ナレッジ
- (なし)
