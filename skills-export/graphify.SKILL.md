ファイル書き込み権限が必要です。許可をお願いします。

以下がSKILL.md全文です:

```markdown
---
name: graphify
description: ソースコードやドキュメントからナレッジグラフを構築する必要があるとき、`graphify`・`python -m graphify`コマンドでAST解析やセマンティック抽出を実行するとき、tree-sitter・NetworkX・Leiden/Louvainクラスタリングが関わるコード解析パイプラインを構築するとき、Claude/Copilot/Codex/Gemini/CursorへのPreToolUseフック注入でグラフコンテキストを自動提供したいとき、大規模コードベースのトークン消費を削減しながらAIエージェントに構造を理解させたいときに必ずこのスキルを使え。`graphify install`・`graphify build`・`graphify export`・`graphify analyze`等のコマンド構築、Obsidian/Neo4j/vis.jsへのエクスポート、インクリメンタルキャッシュ戦略が関わる場面では即座に参照せよ。
---

# graphify

## 概要
graphifyはソースコードやドキュメントからナレッジグラフを自動構築するPythonツール。tree-sitterによるAST解析（Python/JS/TS/Go/Rust/Java/C/C++等20言語以上）とClaude APIによるセマンティック抽出を組み合わせ、コードベースの構造をNetworkXグラフとして構築する。Leiden/Louvainによるコミュニティ検出、ゴッドノード・ブリッジノード分析、グラフ差分計算を提供し、vis.js HTML・JSON・SVG・GraphML・Obsidian Vault/Canvas・Neo4j Cypherへの多形式エクスポートに対応する。Claude/Copilot/Codex/Gemini/Cursor/OpenCode各プラットフォームへのフック注入機構により、AIエージェントのツール呼び出し前にグラフコンテキストを自動注入し、トークン消費を削減しながら大規模コードベースの理解を支援する。

## いつ使うか
- 大規模コードベースをAIエージェントに理解させたいとき（トークン消費の削減）
- レガシーコードのリバースエンジニアリングで構造を可視化したいとき
- マルチリポジトリの依存関係をグラフとして把握したいとき
- Claude Code/Copilot/Codex等のAIツールにコードベースのコンテキストを自動注入したいとき
- Obsidianでコードナレッジベースを構築したいとき
- CI/CDパイプラインでアーキテクチャドリフトを検出したいとき
- コードベースのコミュニティ構造（モジュール凝集度）を分析したいとき
- ゴッドクラス・ブリッジノード・知識ギャップなどの設計上の問題を発見したいとき

## 主要コマンド・API

### インストールと初期セットアップ
```bash
# pipでインストール
pip install graphify-agent

# リポジトリからインストール
git clone https://github.com/safishamsi/graphify.git
cd graphify
pip install -e .

# Claude Codeへのフック登録
graphify install claude

# Copilotへのフック登録
graphify install copilot

# Codex/Gemini/Cursor/OpenCodeへのフック登録
graphify install codex
graphify install gemini
graphify install cursor
graphify install opencode

# フック登録の解除
graphify uninstall claude
```

### グラフ構築
```bash
# カレントディレクトリのコードベースからグラフ構築
graphify build

# 特定ディレクトリを指定して構築
graphify build --path /path/to/project

# セマンティック抽出を有効にして構築（Claude API使用・コスト発生）
graphify build --semantic

# インクリメンタル更新（変更ファイルのみ再抽出）
graphify build --incremental

# キャッシュをクリアして完全再構築
graphify build --no-cache
```

### エクスポート
```bash
# vis.js HTMLで可視化（ブラウザで開ける）
graphify export --format html

# JSON形式でエクスポート
graphify export --format json --output graph.json

# Obsidian Vault形式でエクスポート
graphify export --format obsidian --output ./obsidian-vault/

# Obsidian Canvas形式でエクスポート
graphify export --format canvas --output graph.canvas

# Neo4j Cypher形式でエクスポート
graphify export --format cypher --output import.cypher

# SVG形式でエクスポート
graphify export --format svg --output graph.svg

# GraphML形式でエクスポート
graphify export --format graphml --output graph.graphml
```

### 分析
```bash
# グラフ全体の分析レポート
graphify analyze

# ゴッドノード（過度に多くの接続を持つノード）の検出
graphify analyze --gods

# ブリッジノード（コミュニティ間を橋渡しするノード）の検出
graphify analyze --bridges

# サプライズコネクション（予期しない依存関係）の検出
graphify analyze --surprises

# 知識ギャップ（ドキュメント不足の重要ノード）の検出
graphify analyze --gaps

# 2つのグラフの差分計算
graphify analyze --diff graph-old.json graph-new.json
```

### ベンチマーク
```bash
# トークン削減率の計測
python -m graphify.benchmark --path /path/to/project
```

## 主要コンポーネントと設計

### パイプライン構成
```
抽出（extract.py）→ 構築（build.py）→ クラスタリング（cluster.py）→ 分析（analyze.py）→ エクスポート（export.py）
```

### LanguageConfig Dataclass パターン
各プログラミング言語の文法差異を`LanguageConfig`データクラスに抽象化。インポートハンドラや名前解決関数を差し替えることで20言語以上を単一の`_extract_generic()`関数で処理する。

```python
@dataclass
class LanguageConfig:
    name: str
    extensions: list[str]
    tree_sitter_language: str
    import_handler: Callable
    name_resolver: Callable
    class_query: str
    function_query: str
    call_query: str
```

### Three-layer Node Deduplication
ノード重複排除は3段階で実行される:
1. **ファイル内**: `seen_ids` setによる同一ファイル内の重複排除
2. **ファイル間**: NetworkXの冪等`add_node`による複数ファイル間の重複排除
3. **セマンティックマージ**: `seen` setによるセマンティック抽出結果のマージ

### Incremental Cache
```
graphify-out/
├── cache/
│   ├── {sha256_hash}.json    # ファイルごとの抽出キャッシュ
│   └── ...
├── graph.json                 # 構築済みグラフ
└── analysis.json              # 分析結果
```
- ファイルSHA256ハッシュをキーにキャッシュ
- Markdownファイルはフロントマターを除外してボディのみハッシュ
- 変更されたファイルのみ再抽出するインクリメンタル更新

### Multi-platform Hook Injection
各AIプラットフォームのPreToolUse/BeforeToolフックにgraphifyコマンドを登録し、エージェントのツール呼び出し前にグラフコンテキストを自動注入する。

| プラットフォーム | フック種別 | 登録先 |
|---|---|---|
| Claude Code | PreToolUse hook | `.claude/settings.json` |
| Codex | BeforeTool hook | `.codex/config.json` |
| Gemini | PreToolUse hook | `.gemini/settings.json` |
| Copilot | BeforeTool hook | `.copilot/config.json` |
| Cursor | BeforeTool hook | `.cursor/settings.json` |
| OpenCode | BeforeTool hook | `.opencode/config.json` |

## ワークフロー例

### 典型例1: 新規プロジェクトのコードベース理解
```bash
# 1. プロジェクトディレクトリに移動
cd /path/to/legacy-project

# 2. .graphifyignoreで除外パターンを設定
cat > .graphifyignore << 'EOF'
node_modules/
vendor/
*.min.js
dist/
build/
__pycache__/
EOF

# 3. AST抽出でグラフ構築
graphify build

# 4. コミュニティ構造を分析
graphify analyze

# 5. vis.jsで可視化して全体像を把握
graphify export --format html
# ブラウザでgraphify-out/graph.htmlを開く

# 6. ゴッドノードを特定してリファクタリング対象を洗い出す
graphify analyze --gods

# 7. Claude Codeにフック登録してコンテキスト自動注入
graphify install claude
```

### 典型例2: CI/CDでのアーキテクチャドリフト検出
```bash
# CI/CDパイプライン内で実行

# 1. ベースブランチのグラフを構築
git checkout main
graphify build
cp graphify-out/graph.json /tmp/graph-main.json

# 2. PRブランチのグラフを構築
git checkout feature-branch
graphify build

# 3. 差分を計算
graphify analyze --diff /tmp/graph-main.json graphify-out/graph.json

# 4. 新たなゴッドノードやサプライズコネクションが発生していないか確認
graphify analyze --gods
graphify analyze --surprises
```

### 典型例3: Obsidianナレッジベース構築
```bash
# 1. セマンティック抽出を有効にしてリッチなグラフを構築
graphify build --semantic

# 2. Obsidian Vault形式でエクスポート
graphify export --format obsidian --output ~/Obsidian/CodeKnowledge/

# 3. Obsidian Canvas形式でも出力（俯瞰ビュー用）
graphify export --format canvas --output ~/Obsidian/CodeKnowledge/overview.canvas

# 4. Obsidianで開いてGraph Viewで探索
# → Obsidianの「Open vault」からCodeKnowledgeを選択
```

### 典型例4: マルチリポジトリの依存関係統合
```bash
# 1. 各リポジトリでグラフを構築
graphify build --path ./repo-frontend
graphify build --path ./repo-backend
graphify build --path ./repo-shared-lib

# 2. JSON形式でエクスポートして統合分析
graphify export --format json --output frontend.json --path ./repo-frontend
graphify export --format json --output backend.json --path ./repo-backend
graphify export --format json --output shared.json --path ./repo-shared-lib

# 3. ブリッジノードでリポジトリ間の結合点を特定
graphify analyze --bridges
```

## 注意点
- **セマンティック抽出のコスト**: `--semantic`フラグはClaude API呼び出しが必要でコストが発生する。大規模リポジトリでは`--incremental`と併用してAPI呼び出し回数を最小化すること
- **MAX_NODES_FOR_VIZ制限**: ノード数が5000を超えるグラフはHTML（vis.js）エクスポートが不可。大規模グラフはJSON/GraphML形式でエクスポートするか、サブグラフに分割すること
- **tree-sitter Language API v2が必須**: `LANGUAGE_VERSION >= 14`が必要。古いtree-sitterバインディングでは`AttributeError`や`LanguageError`が発生する。`pip install --upgrade tree-sitter`で更新すること
- **graspologicの依存**: Leidenアルゴリズムは`graspologic`パッケージが必要。未インストールの場合はLouvainに自動フォールバックするが、大規模グラフではLeidenの方が高品質なコミュニティ検出が得られる
- **Windows PowerShell 5.1の問題**: `graspologic`がANSIエスケープシーケンスを出力し、PowerShell 5.1で表示が崩れる。PowerShell 7+を使うか、出力をファイルにリダイレクトすること
- **キャッシュの整合性**: ファイルを移動・リネームするとキャッシュがヒットしなくなる。大規模リファクタリング後は`--no-cache`で完全再構築を推奨
- **Markdownフロントマターの扱い**: キャッシュハッシュはフロントマター（`---`で囲まれたYAMLブロック）を除外してボディのみで計算される。フロントマターのみの変更では再抽出されない点に注意
- **.graphifyignoreの記法**: `.gitignore`と同一のパターン記法。`node_modules/`・`vendor/`・`dist/`など生成物ディレクトリは必ず除外すること。除外しないとグラフが肥大化しノイズが増える
- **フック登録後の競合**: 複数のPreToolUseフックが登録されている場合、実行順序はプラットフォーム依存。graphifyのフックが他のフックと競合する場合は`graphify uninstall`で一旦解除して確認すること
- **ベンチマーク計測の前提**: `benchmark.py`のトークン削減率はグラフ構築前後のコンテキストサイズ比較で計測される。セマンティック抽出の有無で結果が大きく変わるため、比較時は条件を揃えること

## 関連スキル
- **claude-api**: セマンティック抽出でClaude APIを呼び出す際のSDK設定・プロンプトキャッシュ・コスト管理。graphifyの`--semantic`モードの裏側
- **servers**: graphifyの抽出結果をMCPサーバーとして公開し、AIエージェントからリソースとして参照させるパターン
- **cli**: graphifyのCLI出力を`jq`でパイプライン処理するパターン。JSON形式エクスポートとの組み合わせ
- **n8n / n8n-as-code**: graphifyのグラフ構築・分析をn8nワークフローに組み込み、定期的なアーキテクチャ監視を自動化
- **crewai / langgraph**: graphifyのグラフコンテキストをマルチエージェントフレームワークのツールとして統合
```
