# エージェントAPI利用ガイドライン

## 概要
外部エージェント（OpenClaw等）からLightRAG APIを利用する際のルール。

## 認証
- エンドポイント: http://localhost:9621 (VPS内部) / http://76.13.187.66:9621 (外部)
- 認証方式: JWT Bearer Token
- トークン取得: POST /login (username + password)
- トークン有効期限: 取得後都度利用を推奨（キャッシュする場合は1時間以内に再取得）

## 利用可能エンドポイント

| メソッド | パス | 用途 | レート目安 |
|---|---|---|---|
| POST | /query | ナレッジ検索 | 10回/分 |
| GET | /documents | ドキュメント一覧 | 5回/分 |
| POST | /documents/upload | ドキュメント投入 | 投入時のみ |
| DELETE | /documents/delete_document | ドキュメント削除 | 運用時のみ |

## 検索のベストプラクティス
- mode: hybrid を基本とする（精度と網羅性のバランス）
- プロジェクト文脈を付加する場合はクエリ先頭に `[プロジェクト文脈: ...]` を付与
- 利用可能プロジェクト: config/project_profiles.json を参照

## エージェント統合パターン

### パターン1: MCP経由（Claude Code）
mcp_lightrag.py を利用。search_knowledge / list_knowledge / list_projects ツール。

### パターン2: REST直接（OpenClaw等）
```python
import requests

# トークン取得
token = requests.post("http://localhost:9621/login",
    data={"username": "admin", "password": "<.envを参照>"}).json()["access_token"]

# 検索
result = requests.post("http://localhost:9621/query",
    headers={"Authorization": f"Bearer {token}"},
    json={"query": "検索クエリ", "mode": "hybrid"}).json()
```

### パターン3: search_knowledge.sh ラッパー（シェル経由）
```bash
/docker/lightrag/scripts/search_knowledge.sh "クエリ" hybrid openclaw
```

## セキュリティ注意事項
- 認証情報は.envから取得。コードにハードコードしない
- 外部公開する場合はNginxリバースプロキシ + HTTPS必須
- 現状はVPS内部アクセスのみ。外部公開は未設定
