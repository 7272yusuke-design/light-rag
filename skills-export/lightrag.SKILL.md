改善したSKILL.md全文を出力します。

---

```markdown
---
name: lightrag
description: LightRAG（lightrag-hku）でナレッジグラフ構築・RAGクエリ・ストレージバックエンド設定・FastAPIサーバー運用を行うときに必ずこのスキルを使え。QueryParam、ainsert/aquery、Neo4j/PG/Milvus接続、Docker Compose展開、エンティティ抽出プロンプトのカスタマイズが含まれる場合は即座に参照せよ。
---

# lightrag

## 概要
LightRAGはドキュメントコーパスからナレッジグラフを自動構築し、5つのクエリモード（naive/local/global/hybrid/mix）で検索・回答生成を行うRAGフレームワークである。OpenAI・Gemini・Ollamaなど多数のLLMプロバイダーと、Neo4j・PostgreSQL・Milvus・Qdrantなど多様なストレージバックエンドをプラグイン形式でサポートし、FastAPI REST APIとReact WebUIを標準搭載する。パッケージ名は `lightrag-hku`。

## いつ使うか
- ドキュメント群からナレッジグラフを構築・クエリしたい
- RAGシステムのストレージバックエンド（ベクターDB・グラフDB・KVストア）を切り替えたい
- LLMプロバイダーを変更・追加したい（OpenAI→Ollama等）
- FastAPIサーバーの起動・認証・エンドポイント設定を行いたい
- エンティティ抽出・関係抽出のプロンプトをカスタマイズしたい
- マルチテナント対応のワークスペース分離を実装したい
- Docker Composeで LightRAG + Neo4j + PostgreSQL を展開したい
- クエリモード（naive/local/global/hybrid/mix）の選択を最適化したい

## 主要コマンド・API

### インストール・起動
```bash
# 基本インストール
pip install lightrag-hku

# オプション依存付きインストール
pip install "lightrag-hku[neo4j]"
pip install "lightrag-hku[milvus]"

# 環境変数で設定
export OPENAI_API_KEY=sk-...
export LIGHTRAG_WORKING_DIR=./rag_storage
export LIGHTRAG_JWT_SECRET=your-secret

# FastAPIサーバー起動（ポートは環境変数 PORT でも指定可）
python -m lightrag.api.lightrag_server --host 0.0.0.0 --port 9621
```

### Docker Compose展開
```yaml
# docker-compose.yml
services:
  lightrag:
    image: ghcr.io/hkuds/lightrag:latest
    ports:
      - "9621:9621"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - LIGHTRAG_WORKING_DIR=/data/rag_storage
      - LIGHTRAG_JWT_SECRET=${LIGHTRAG_JWT_SECRET}
    volumes:
      - ./rag_storage:/data/rag_storage
    depends_on:
      - neo4j

  neo4j:
    image: neo4j:5
    ports:
      - "7474:7474"
      - "7687:7687"
    environment:
      - NEO4J_AUTH=neo4j/password
    volumes:
      - neo4j_data:/data

volumes:
  neo4j_data:
```
```bash
docker compose up -d
```

### コアエンジンの初期化
```python
from lightrag import LightRAG, QueryParam
from lightrag.llm.openai import openai_complete_if_cache, openai_embedding
from lightrag.utils import EmbeddingFunc

rag = LightRAG(
    working_dir="./rag_storage",
    llm_model_func=openai_complete_if_cache,
    llm_model_name="gpt-4o-mini",
    llm_model_max_async=4,          # 並列LLMリクエスト数
    llm_model_max_token_size=32768,
    embedding_func=EmbeddingFunc(
        embedding_dim=1536,
        max_token_size=8192,
        func=openai_embedding,
    ),
)
```

### ドキュメント投入
```python
# 単一テキスト挿入（非同期）
await rag.ainsert("ドキュメントテキスト...")

# 複数ドキュメント一括挿入
await rag.ainsert(["doc1テキスト", "doc2テキスト"])

# ファイルパスから挿入（同期版 — イベントループ外でのみ使用）
rag.insert_file("./document.pdf")
```

### クエリ実行とモード選択
```python
# クエリモードの使い分け:
#   naive  — チャンクの直接検索。シンプルなキーワード質問向き
#   local  — ローカルサブグラフ探索。特定エンティティの詳細質問向き
#   global — グローバルグラフ要約。全体傾向・統計的質問向き
#   hybrid — local + global の併用。バランス型
#   mix    — naive + local + global 全統合。最高精度だがコスト大

result = await rag.aquery(
    "質問テキスト",
    param=QueryParam(
        mode="hybrid",       # 通常はhybridで十分、精度優先ならmix
        top_k=60,
        max_token_for_text_chunk=4000,
        max_token_for_global_context=4000,
        max_token_for_local_context=4000,
        response_type="Single Paragraph",
    )
)
```

### ストレージバックエンド切り替え
```python
rag = LightRAG(
    working_dir="./rag_storage",
    graph_storage="Neo4JStorage",            # デフォルト: NetworkXStorage
    vector_storage="MilvusVectorDBStorage",  # デフォルト: NanoVectorDBStorage
    kv_storage="PGKVStorage",                # デフォルト: JsonKVStorage
    doc_status_storage="PGDocStatusStorage",
    addon_params={
        "neo4j_url": "bolt://localhost:7687",
        "neo4j_auth": ("neo4j", "password"),
    },
)
# 他の選択肢: graph=MemgraphStorage, vector=QdrantVectorDBStorage/FaissVectorDBStorage,
#             kv=MongoKVStorage/RedisKVStorage
```

### Ollamaバックエンド使用
```python
from lightrag.llm.ollama import ollama_model_complete, ollama_embedding

rag = LightRAG(
    working_dir="./rag_storage",
    llm_model_func=ollama_model_complete,
    llm_model_name="llama3.2",
    embedding_func=EmbeddingFunc(
        embedding_dim=768,               # nomic-embed-textの次元数
        max_token_size=8192,
        func=lambda texts: ollama_embedding(texts, embed_model="nomic-embed-text"),
    ),
)
```

### REST API呼び出し例
```bash
# ヘルスチェック
curl http://localhost:9621/health

# ドキュメントアップロード
curl -X POST http://localhost:9621/documents/upload \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@document.pdf"

# クエリ実行
curl -X POST http://localhost:9621/query \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "質問テキスト", "mode": "hybrid"}'

# エンティティ一覧取得
curl http://localhost:9621/graph/entities \
  -H "Authorization: Bearer $TOKEN"
```

### ワークスペース分離（マルチテナント）
```python
rag_tenant_a = LightRAG(
    working_dir="./storage",
    workspace="tenant_a",   # 全ストレージバックエンドで名前空間が分離される
    llm_model_func=openai_complete_if_cache,
    # ... 他の設定
)
```

### リランキング設定
```python
from lightrag.rerank import rerank_documents

rag = LightRAG(
    working_dir="./rag_storage",
    llm_model_func=openai_complete_if_cache,
    rerank_model_func=rerank_documents,
    rerank_model_name="BAAI/bge-reranker-v2-m3",
    # ... 他の設定
)
```

## ワークフロー例

### 新規RAGシステム構築（Python SDK）
1. `pip install lightrag-hku` でインストール。Neo4j使用時は `pip install "lightrag-hku[neo4j]"`
2. `export OPENAI_API_KEY=sk-...` でAPIキーを設定
3. `LightRAG(working_dir=..., llm_model_func=...)` でインスタンス初期化
4. `await rag.ainsert(documents)` でドキュメント投入 → エンティティ・関係抽出が自動実行される
5. `await rag.aquery(question, param=QueryParam(mode="hybrid"))` でクエリ
6. 精度不足なら `mode="mix"` に変更、コスト削減なら `mode="local"` に変更

### Docker Composeでのプロダクション展開
1. `docker-compose.yml` に lightrag + neo4j + postgres サービスを定義
2. `.env` に `OPENAI_API_KEY`, `LIGHTRAG_JWT_SECRET`, ストレージ接続情報を記述
3. `docker compose up -d` で起動
4. `curl http://localhost:9621/health` でヘルスチェック
5. `curl http://localhost:9621/docs` でSwagger UIを確認し、JWT認証トークンを取得
6. ドキュメントをREST API経由でアップロードし、WebUIでグラフ可視化を確認

### プロンプトカスタマイズ（日本語ドメイン特化）
1. `lightrag/prompt.py` でエンティティ抽出・関係抽出・回答生成のテンプレートを確認
2. `LightRAG(addon_params={"language": "Japanese"})` で言語を指定
3. ドメイン固有のエンティティタイプが必要なら、プロンプトテンプレートを直接編集

### カスタムストレージバックエンド実装
1. `lightrag/kg/base.py` の `BaseVectorStorage` / `BaseGraphStorage` / `BaseKVStorage` を確認
2. 全抽象メソッドを実装したクラスを作成
3. `LightRAG(vector_storage="MyCustomStorage")` でクラス名を文字列指定
4. `addon_params={"my_db_url": "..."}` で接続情報を渡す

## 注意点
- **非同期必須**: コアAPIはすべて `async/await` ベース。同期版（`insert`/`query`）は内部で `asyncio.run()` を使うため、既存のイベントループ内では必ず `ainsert`/`aquery` を使うこと。混在させると `RuntimeError: This event loop is already running` になる
- **埋め込み次元の一致**: `EmbeddingFunc(embedding_dim=...)` とストレージバックエンドの次元設定を必ず一致させること。不一致はエラーにならず**無言の精度劣化**を招く。OpenAI=1536、nomic-embed-text=768
- **max_async の調整**: `llm_model_max_async` のデフォルトが高すぎるとLLMプロバイダーのレート制限で429エラーが頻発する。OpenAI=4〜8、Ollama=1〜2が目安
- **ワークスペース名の変更禁止**: 一度データを投入した `workspace` 名を変更すると既存データに一切アクセスできなくなる。テナント名は慎重に決めること
- **クエリモードの選択**: `mix`は最高精度だがLLMコスト3倍。通常は`hybrid`で十分。単一エンティティの詳細なら`local`、全体傾向なら`global`
- **デッドロック回避**: カスタムストレージ実装時、非同期ジェネレーターではロック保持中にスナップショットを取得してからyieldすること。複数ロック取得時はソート済みキー順で取得（`operate.py` 参照）
- **base64埋め込み**: Azure OpenAI等は埋め込みをbase64で返す。カスタムアダプター実装時は `lightrag/llm/` の既存コードを参考にfloat配列へ正規化すること
- **Neo4j接続プール**: Neo4j使用時は非同期ドライバーの接続プール枯渇に注意。`addon_params` で `max_connection_pool_size` を明示設定するのが安全
- **WebUIビルド**: `lightrag_webui/` は `npm install && npm run build` が別途必要。ビルド成果物のパスをサーバーの静的ファイル設定と合わせること

## 関連スキル
- **fastapi**: LightRAGサーバーのエンドポイント拡張・ミドルウェア追加・認証カスタマイズ
- **neo4j**: グラフDBバックエンドの設定・Cypherクエリによるナレッジグラフ直接操作
- **postgresql**: PGKVStorage・PGDocStatusStorageのバックエンド設定・マイグレーション
- **docker**: LightRAG + Neo4j + PostgreSQL + Milvusのコンテナ化とdocker-compose構成
- **ollama**: ローカルLLM/埋め込みモデルのセットアップとOllama互換エンドポイント統合
```

---

**改善ポイント:**

| 基準 | 元の評価 | 改善内容 |
|---|---|---|
| 1. description精度 | 抽象的な「ナレッジグラフ構築・RAGシステム」 | 具体的API名（QueryParam, ainsert/aquery）とインフラキーワード（Docker Compose, Neo4j/PG/Milvus）をトリガーに追加 |
| 2. 500行以下 | 207行 OK | 約210行。Docker Compose例を追加しても範囲内 |
| 3. コマンド例 | ポート8020（実環境と不一致）、`...`省略多い | ポート9621に統一、オプション依存のインストール構文追加、REST APIにヘルスチェック追加 |
| 4. ワークフロー | Docker展開フローが欠落 | Docker Compose展開ワークフローを追加、SDKワークフローにモード切替の判断基準を追加 |
| 5. 注意点 | RuntimeErrorの具体メッセージ欠落、モード選択コスト感なし | 非同期エラーメッセージを明記、クエリモードのコスト比較（mix=3倍）を追加、埋め込み次元の具体値を付記 |
| 6. 関連スキル | reactが入っていたが優先度低い | reactを削除（WebUIカスタマイズは稀）、残り5つに絞り各説明を具体化 |
