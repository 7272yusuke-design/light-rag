---
source: https://github.com/vercel/vercel
category: tool
sub_categories: [framework, infra]
tags: [TypeScript, Rust, Python, CLI, Vercel, deployment, monorepo, serverless]
language: 
ingested: 2026-04-11
source_updated: unknown
status: active
---

# vercel

# vercel

## 基本情報
- リポジトリ: https://github.com/vercel/vercel
- カテゴリ: tool
- サブカテゴリ: framework, infra
- タグ: TypeScript, Rust, Python, CLI, Vercel, deployment, monorepo, serverless
- 最終確認日: 2026-04-11

## 概要
Vercel CLIおよびVercelプラットフォームのSDK・ビルドユーティリティを含むモノレポ。フロントエンド・バックエンド・サーバーレス関数のデプロイメントを管理するCLIツールと、50以上のフレームワーク向けビルダープラグインを提供する。Python/Rust/Node.js等の多言語ランタイムサポートと、エッジ関数・OIDC認証・ファイアウォール等のVercelプラットフォーム機能へのアクセスを実現する。

## 設計思想
モノレポ構成でCLI・ビルダー・クライアントライブラリを分離管理し、各フレームワーク向けビルダーを独立パッケージとして実装するプラグインアーキテクチャ。Vercelプラットフォームのすべての機能をCLIコマンドとして表現し、テレメトリ・エラーハンドリング・出力フォーマットを横断的関心事として統一実装している。

## 主要コンポーネント
- packages/cli: Vercel CLIのメインエントリポイント。deploy/dev/env/domains等60以上のサブコマンドを実装
- packages/build-utils: Lambda・プリレンダリング・ファイルシステム操作等のビルド共通ユーティリティ
- packages/frameworks: 50以上のフレームワーク検出・設定情報のカタログ
- packages/fs-detectors: フレームワーク・モノレポ・パッケージマネージャの自動検出
- packages/node / python / go / ruby / rust: 各言語ランタイム向けサーバーレスビルダー
- packages/functions: Vercel Functions SDK（キャッシュ・OIDC・Purge API等）
- packages/edge: Vercel Edge Functionsランタイム型定義・ユーティリティ
- crates/vercel_runtime: RustのAxum向けVercelランタイム統合
- python/vercel-runtime: ASGI/WSGI対応PythonランタイムとuvicornベンダリングRuntimeライブラリ

## 実装パターン
- Framework Builder Plugin: 各フレームワーク（Next.js・Remix・Nuxt等）向けにbuild/prepareCache/devServerを実装する統一インターフェースのビルダーパッケージ
- Command + Telemetry分離: CLIコマンドごとにTelemetryクラスを対応させ、使用状況トラッキングをコマンドロジックから分離
- Rolldown-based bundling: packages/backendsでrolldownを使いCJS/ESMデュアル出力とNode File Traceによる依存トレースを実現
- Agent Eval Framework: packages/cli/evalsでLLMエージェントによるCLI操作の評価・スモークテストを自動化するEVAL.ts/PROMPT.md構造
- WASM Python Analysis: packages/python-analysisでRustをWASMにコンパイルしPython依存関係の解析をJS環境から実行

## 適用シーン
Vercelへのアプリケーションデプロイメントを自動化したいCIパイプライン、Vercelプラットフォーム機能（Edge Functions・Blob・Firewall等）を利用するWebアプリ開発、Vercel互換のカスタムフレームワークビルダーを実装したいフレームワーク開発者、Vercel CLIを組み込んだ開発ツール構築。

## 注意点・制約
Vercelプラットフォーム専用であり他クラウドには非対応。モノレポ規模が非常に大きくビルド環境の整備が必要。一部ビルダーパッケージ（.deployファイル存在）はVercel内部デプロイメントシステムと密結合。Python WASMビルドはRustツールチェーンが必要。CLIのエージェント評価機能は実験的でAPIキーやサンドボックス環境が必要。


## 関連ナレッジ
- (なし)
