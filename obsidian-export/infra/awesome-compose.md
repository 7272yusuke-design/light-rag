---
source: https://github.com/docker/awesome-compose
category: infra
sub_categories: [webapp, tool]
tags: [docker-compose, multi-language, containerization, nginx, postgresql, react, golang, python]
language: 
ingested: 2026-04-09
source_updated: unknown
status: active
---

# awesome-compose

# awesome-compose

## 基本情報
- リポジトリ: https://github.com/docker/awesome-compose
- カテゴリ: infra
- サブカテゴリ: webapp, tool
- タグ: docker-compose, multi-language, containerization, nginx, postgresql, react, golang, python
- 最終確認日: 2026-04-09

## 概要
Docker Composeを使った多様な技術スタックのサンプルアプリケーション集。Angular、React、Vue.js、Django、Flask、FastAPI、ASP.NET、Spring Boot、Rust等を組み合わせたコンポーズ構成例を提供する。各サンプルはDockerfileとcompose.yamlで構成され、開発環境の即時起動を可能にする。

## 設計思想
各サンプルは独立したディレクトリに格納され、フロントエンド・バックエンド・DB・プロキシを明確に分離したマルチコンテナ構成を採用。dev-envs向けのDockerfileターゲットも用意され、VSCode Remote Containersとの統合も考慮されている。

## 主要コンポーネント
- compose.yaml: 各サンプルのサービス定義・ポートマッピング・ネットワーク構成
- Dockerfile: 各サービスのコンテナイメージビルド定義（builderとdev-envsの2ステージ）
- nginx proxy: リバースプロキシとして複数サンプルで使用
- db/password.txt: Docker Secretsによるデータベースパスワード管理
- frontend: React/Angular/Vue等のSPAフロントエンド実装
- backend: Go/Python/Java/Rust等の各種バックエンドAPI実装

## 実装パターン
- Multi-stage Dockerfile: builderステージとdev-envsステージを分離し、開発環境と本番環境の差異を吸収
- Docker Secrets: password.txtファイルをDocker Secretsとしてマウントし、DBパスワードを安全に管理
- Reverse Proxy Pattern: nginxやTraefikをフロントに配置し、バックエンドAPIへのリクエストをプロキシ
- Service Separation: frontend/backend/db/proxyを独立コンテナに分離し、スケーラビリティと保守性を確保

## 適用シーン
Docker Composeを学習したい開発者、特定の技術スタック（React+Node+MongoDB、Spring+PostgreSQL等）の雛形が必要なプロジェクト、ローカル開発環境の迅速な構築が必要なチームに最適。

## 注意点・制約
各サンプルはデモ・学習用途であり、本番環境向けのセキュリティ設定（TLS、認証強化等）は含まれていない。一部サンプルのバージョンが古い場合がある。WasmEdge等の実験的サンプルは環境依存が高い。


## 関連ナレッジ
- (なし)
