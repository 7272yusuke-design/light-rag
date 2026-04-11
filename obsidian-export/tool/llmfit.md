---
source: https://github.com/AlexsJones/llmfit
category: tool
sub_categories: [webapp, infra]
tags: [rust, react, tauri, llm, hardware-detection, gguf, model-selection, tui]
language: 
ingested: 2026-04-11
source_updated: unknown
status: active
---

# llmfit

# llmfit

## 基本情報
- リポジトリ: https://github.com/AlexsJones/llmfit
- カテゴリ: tool
- サブカテゴリ: webapp, infra
- タグ: rust, react, tauri, llm, hardware-detection, gguf, model-selection, tui
- 最終確認日: 2026-04-11

## 概要
LLMFit はローカルマシンのハードウェアスペック（RAM/VRAM）を自動検出し、実行可能なLLMモデルを推薦・フィルタリングするツール。デスクトップアプリ（Tauri）、TUI、Webアプリの3つのフロントエンドを提供する。HuggingFaceおよびDocker上のGGUF形式モデルカタログと照合し、最適なモデル選択を支援する。

## 設計思想
コアロジックをRustライブラリ（llmfit-core）として分離し、デスクトップ・TUI・Webの3フロントエンドから共有するモノレポ構成。ハードウェア検出とモデルフィッティングロジックを中央集権化し、各UIは表示レイヤーのみを担当するクリーンな関心分離を実現している。

## 主要コンポーネント
- llmfit-core: ハードウェア検出・モデル適合判定・プロバイダー管理のRustコアライブラリ
- llmfit-desktop: TauriベースのクロスプラットフォームデスクトップGUI
- llmfit-tui: ターミナルUIフロントエンド（ratatui使用）
- llmfit-web: React/Viteベースのウェブアプリ（フィルタリング・比較機能付き）
- data/hf_models.json: HuggingFaceモデルカタログ（パラメータ数・RAM/VRAM要件・capabilities含む）
- scripts/scrape_*.py: HuggingFace・DockerHubからモデル情報を収集するスクレイピングスクリプト

## 実装パターン
- Multi-frontend monorepo: Cargoワークスペースで core/desktop/tui/web を管理し、コアロジックを共有
- Hardware-aware filtering: 検出されたRAM/VRAMに基づきモデルカタログをリアルタイムフィルタリング
- Static model catalog: スクレイピングで生成したJSONカタログをバンドルし、APIなしでオフライン動作を実現

## 適用シーン
ローカルLLM実行環境を構築したいユーザーが自分のマシンで動くモデルを素早く特定したい場面。開発者がエッジ・オンプレ環境向けモデル選定ガイドとして活用する場面。AIエージェントスキル（llmfit-advisor）としてモデル推薦を自動化する場面。

## 注意点・制約
モデルカタログはスクレイピングベースのため最新モデルへの追従にタイムラグがある。RAM/VRAM要件はQ4_K_M量子化を前提とした推定値であり実際の消費量と乖離する場合がある。WebフロントエンドはAPIサーバー（llmfit-tui serve_api）との連携が必要。


## 関連ナレッジ
- (なし)
