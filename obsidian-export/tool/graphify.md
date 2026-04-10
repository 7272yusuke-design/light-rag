---
source: https://github.com/safishamsi/graphify
category: tool
sub_categories: [workflow, agent]
tags: [python, knowledge-graph, AST-extraction, tree-sitter, networkx, LLM-integration, community-detection, code-analysis]
language: 
ingested: 2026-04-10
source_updated: unknown
status: active
---

# graphify

# graphify

## 基本情報
- リポジトリ: https://github.com/safishamsi/graphify
- カテゴリ: tool
- サブカテゴリ: workflow, agent
- タグ: python, knowledge-graph, AST-extraction, tree-sitter, networkx, LLM-integration, community-detection, code-analysis
- 最終確認日: 2026-04-10

## 概要
graphifyはソースコードやドキュメントからナレッジグラフを自動構築するPythonツール。AST解析（tree-sitter）と意味的抽出を組み合わせ、コードベースの構造をグラフ化してClaude/Copilot/Codexなどの各種AIエージェントに提供する。AIエージェントがグラフを参照することでトークン消費を削減しながら大規模コードベースを理解できる。

## 設計思想
抽出（AST＋セマンティック）→構築（NetworkX）→クラスタリング（Leiden/Louvain）→分析→エクスポートのパイプライン設計。各AIプラットフォーム（Claude、Copilot、Codex、Gemini、Cursor等）へのフック機構でエージェントの全ツール呼び出し前にグラフコンテキストを注入する。キャッシュとインクリメンタル更新で再実行コストを最小化。

## 主要コンポーネント
- extract.py: tree-sitterを使った多言語AST解析（Python/JS/TS/Go/Rust/Java/C/C++等20言語以上）。クラス・関数・インポート・呼び出しグラフを抽出
- build.py: 複数ファイルの抽出結果をNetworkXグラフに統合。ノード重複排除（ファイル内・ファイル間・セマンティックマージの3層）
- cluster.py: Leiden（graspologic）またはLouvainによるコミュニティ検出。大規模コミュニティの再分割とコヒーション計算
- analyze.py: ゴッドノード・サプライズコネクション・ブリッジノード・知識ギャップの分析。グラフ差分計算
- export.py: vis.js HTML、JSON、SVG、GraphML、Obsidian Vault/Canvas、Neo4j Cypherへの多形式エクスポート
- cache.py: ファイルハッシュベースの抽出キャッシュ。Markdownはフロントマターを除外してボディのみハッシュ
- detect.py: ファイル種別分類（コード/ドキュメント/論文/画像）、コーパス規模検出、.graphifyignore対応
- __main__.py: CLIエントリポイント。各AIプラットフォームへのインストール・アンインストール・フック登録を管理

## 実装パターン
- LanguageConfig Dataclass: 各プログラミング言語の文法差異をLanguageConfigデータクラスに抽象化。インポートハンドラや名前解決関数を差し替えることで20言語以上を単一の_extract_generic()関数で処理
- Multi-platform Hook Injection: Claude/Codex/Gemini/OpenCode/Cursor/Copilot各プラットフォームのPreToolUse/BeforeToolフックにgraphifyコマンドを登録し、AIエージェントのツール呼び出し前に自動的にグラフコンテキストを注入
- Three-layer Node Deduplication: ファイル内（seen_ids set）→ファイル間（NetworkX idempotent add_node）→セマンティックマージ（seen set）の3段階でノード重複を排除
- Incremental Cache: ファイルSHA256ハッシュをキーにgraphify-out/cache/{hash}.jsonにキャッシュ。変更されたファイルのみ再抽出するインクリメンタル更新モードをサポート

## 適用シーン
大規模コードベースをAIエージェントに理解させる際のコンテキスト圧縮（平均トークン削減率をbenchmark.pyで計測）。レガシーコードのリバースエンジニアリング。マルチリポジトリの依存関係可視化。Obsidianでのコードナレッジベース構築。CI/CDパイプラインへの組み込みによるアーキテクチャドリフト検出。

## 注意点・制約
セマンティック抽出はClaude API呼び出しが必要（コスト発生）。MAX_NODES_FOR_VIZ=5000を超えるグラフはHTML出力不可。tree-sitter Language API v2（LANGUAGE_VERSION>=14）が必要。graspologicはオプション依存でインストール済みでない場合Louvainにフォールバック。Windows PowerShell 5.1ではgraspologicのANSIエスケープ出力が問題になるため出力抑制が必要。


## 関連ナレッジ
- (なし)
