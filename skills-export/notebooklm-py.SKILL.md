改善した SKILL.md 全文を以下に出力します。

---

```markdown
---
name: notebooklm-py
description: Google NotebookLM をプログラムから操作するとき必ずこのスキルを使え。NotebookLMClient、notebooklm auth login、artifacts generate --type audio_overview、sources add --url、ポッドキャスト自動生成、クイズ／フラッシュカード JSON エクスポート、Playwright ブラウザ認証が含まれる場合は即座に参照せよ。
---

# notebooklm-py

## 概要
notebooklm-py は Google NotebookLM への Python 製 CLI／ライブラリインターフェースである。ノートブック管理・ソースインポート・ポッドキャスト／動画／クイズ等の AI コンテンツ生成・チャット操作をプログラムから自動化できる。Google の非公開 RPC プロトコルを内部で処理し、Playwright によるブラウザ認証でセッションを永続化する。CLI と async Python API の両方で利用可能。

## いつ使うか
- NotebookLM のノートブックを作成・一覧・削除したい
- URL・PDF・テキスト等のソースをノートブックへ一括インポートしたい
- ポッドキャスト（audio_overview）、動画概要、スライドデッキ、クイズ、フラッシュカード、マインドマップを自動生成したい
- 生成済みアーティファクトをバッチダウンロードしたい
- クイズ・フラッシュカード・マインドマップを JSON でエクスポートしたい
- CI/CD パイプラインや LLM エージェントから NotebookLM を操作したい
- 複数 Google アカウントをプロファイルで切り替えたい

## 主要コマンド・API

### 認証
```bash
# 初回ブラウザ認証（Playwright が起動する）
notebooklm auth login

# プロファイル指定で認証
notebooklm --profile work auth login

# 認証状態確認
notebooklm auth status
```

### ノートブック操作
```bash
# 一覧表示
notebooklm notebooks list

# JSON 出力（スクリプト連携用）
notebooklm notebooks list --json

# 作成
notebooklm notebooks create --title "Weekly Research"

# 削除（ID プレフィックスで指定可）
notebooklm notebooks delete abc123
```

### ソースインポート
```bash
# URL からインポート
notebooklm sources add <notebook_id> --url "https://arxiv.org/abs/2401.12345"

# 複数 URL を一括追加
notebooklm sources add <notebook_id> \
  --url "https://example.com/paper1.pdf" \
  --url "https://example.com/paper2.pdf"

# ローカルファイルからインポート
notebooklm sources add <notebook_id> --file ./document.pdf
```

### アーティファクト生成・ダウンロード
```bash
# ポッドキャスト生成（完了まで待機、指数バックオフ）
notebooklm artifacts generate <notebook_id> --type audio_overview --wait

# クイズ生成 → JSON エクスポート
notebooklm artifacts generate <notebook_id> --type quiz --wait
notebooklm artifacts export <artifact_id> --format json > quiz.json

# マインドマップ生成 → JSON エクスポート
notebooklm artifacts generate <notebook_id> --type mind_map --wait
notebooklm artifacts export <artifact_id> --format json

# アーティファクト一覧
notebooklm artifacts list <notebook_id>

# ダウンロード
notebooklm artifacts download <artifact_id> --output ./output/
```

アーティファクトタイプ一覧: `audio_overview`, `video_overview`, `slide_deck`, `infographic`, `quiz`, `flashcards`, `mind_map`, `report`

### Python ライブラリ（async API）
```python
import asyncio
from notebooklm import NotebookLMClient

async def main():
    async with NotebookLMClient(profile="default") as client:
        # ノートブック作成
        notebook = await client.notebooks.create(title="Research Pipeline")

        # ソース追加
        await client.sources.add(
            notebook_id=notebook.id,
            urls=["https://arxiv.org/abs/2401.12345"]
        )

        # ポッドキャスト生成（task_id 返却 → ポーリング）
        task = await client.artifacts.generate(
            notebook_id=notebook.id,
            artifact_type="audio_overview"
        )
        artifact = await client.artifacts.wait_for_completion(task.task_id)

        # ダウンロード
        await client.artifacts.download(artifact.id, output_path="./podcast.mp3")

        # クイズ生成 → JSON エクスポート
        task = await client.artifacts.generate(
            notebook_id=notebook.id,
            artifact_type="quiz"
        )
        quiz = await client.artifacts.wait_for_completion(task.task_id)
        result = await client.artifacts.export(quiz.id, format="json")

asyncio.run(main())
```

### 名前空間 API 一覧
```python
client.notebooks   # create, list, delete
client.sources     # add (urls / file)
client.artifacts   # generate, wait_for_completion, download, export, list
client.chat        # チャット操作
client.notes       # ノート管理
client.research    # リサーチ操作
client.settings    # 設定変更
client.sharing     # 共有設定
```

### マルチアカウント
```bash
notebooklm --profile personal notebooks list
notebooklm --profile work artifacts list <notebook_id>
```

## ワークフロー例

### リサーチ論文 → ポッドキャスト自動生成
1. `notebooklm auth login` でブラウザ認証を完了（初回のみ）
2. `notebooklm notebooks create --title "AI Survey Q1"` でノートブック作成、返却 ID を控える
3. `notebooklm sources add <id> --url "https://arxiv.org/abs/..." --url "https://..."` で論文を一括追加
4. `notebooklm artifacts generate <id> --type audio_overview --wait` でポッドキャスト生成（5〜15 分程度）
5. `notebooklm artifacts download <artifact_id> --output ./podcasts/` でローカル保存

### クイズ・フラッシュカードの JSON 一括エクスポート
1. `notebooklm notebooks list --json | jq -r '.[0].id'` で対象ノートブック ID を取得
2. `notebooklm artifacts generate <id> --type quiz --wait` でクイズ生成
3. `notebooklm artifacts export <artifact_id> --format json > quiz.json` でエクスポート
4. 同様に `--type flashcards` でフラッシュカードを生成・エクスポート

### LLM エージェントからの利用（Python）
1. `NotebookLMClient(profile="default")` を async context manager で初期化
2. `client.notebooks` / `client.sources` / `client.artifacts` の各名前空間 API を呼び出し
3. 生成タスクは `task_id` を即時返却 → `wait_for_completion()` で完了待ち
4. 401/403 発生時はクライアントが自動トークンリフレッシュ（セッション期限切れは除く）

### CI/CD パイプラインでの定期コンテンツ生成
1. CI ランナー上で事前に `notebooklm auth login` を実行し、`~/.notebooklm/profiles/ci/` にセッション保存
2. パイプラインで `notebooklm --profile ci notebooks create --title "$(date +%Y-%m-%d)"` を実行
3. ソース追加 → アーティファクト生成 → ダウンロードの一連を自動化
4. セッション切れ（1〜2 週間）に備え、定期的にログインを更新するジョブを設定

## 注意点
1. **初回認証は Playwright 必須**: ヘッドレス環境では事前にヘッド付きで `auth login` を実行し、`~/.notebooklm/profiles/<name>/storage_state.json` にセッションを保存しておくこと
2. **セッション有効期限**: Google セッションは約 1〜2 週間で失効する。CI 環境では定期的な再ログインが必要
3. **完全非同期設計**: `NotebookLMClient` に同期ラッパーは存在しない。既存イベントループ内では `asyncio.run()` は使えないため、直接 `await` すること。誤用すると `RuntimeError: This event loop is already running` になる
4. **生成タスクは非同期ポーリング**: `artifacts generate` は即座に `task_id` を返すだけ。CLI では `--wait`（指数バックオフ）、Python では `wait_for_completion()` で完了を待つこと
5. **動画生成は長時間**: `video_overview` は 15〜30 分以上かかる場合がある。タイムアウト設定に注意
6. **部分 ID マッチング**: CLI は ID プレフィックスを受け付けるが、一意に解決できない場合はエラー。`notebooks list` で完全 ID を確認してから使うと安全
7. **Google 非公開 RPC 依存**: 内部 API に依存しているため、Google 側の変更で突然動作しなくなる可能性がある。バージョンを固定し、アップデート時はテストすること
8. **レート制限**: 大量のソース追加やアーティファクト生成を短時間に行うと Google 側で制限される。バッチ処理には適切な待機を挟むこと
9. **--json フラグ**: CLI の全コマンドは `--json` で機械可読出力をサポート。スクリプト連携時は必ず使うこと
10. **プロファイル分離**: セッション情報は `~/.notebooklm/profiles/<name>/` に保存される。複数アカウントは `--profile` で必ず分離すること

## 関連スキル
- **playwright-cli**: 認証フローのブラウザ自動化に使用。認証トラブル時のデバッグに参照
- **LLM エージェントフレームワーク**（LangChain, CrewAI 等）: `NotebookLMClient` を tool として組み込む際の連携先
- **n8n / n8n-as-code**: NotebookLM 操作をワークフロー自動化に組み込む際の連携先
- **cli-anything**: CLI ハーネス設計パターンの参考。`--json` 出力やプロファイル管理の設計思想が共通
```

---

**改善サマリ（6 基準対応）:**

| # | 基準 | 元の評価 | 改善内容 |
|---|------|---------|---------|
| 1 | description トリガー精度 | 抽象的（「ノートブック管理・AI コンテンツ生成」） | 具体的 API 名を列挙（`NotebookLMClient`, `artifacts generate --type audio_overview`, `sources add --url`, `Playwright ブラウザ認証`）＋「即座に参照せよ」の二段トリガー |
| 2 | 500 行以下 | 145 行 OK | 約 160 行。名前空間 API 一覧・CI/CD ワークフロー・クイズ連携例を追加しても余裕 |
| 3 | コマンド例の具体性 | `"https://..."` など省略多い、`--json` 未記載 | URL を `arxiv.org/abs/2401.12345` 等の具体例に、`--json` フラグ・`jq` パイプ例を追加、アーティファクトタイプ全8種を一覧化 |
| 4 | ワークフロー実践性 | 3 パターン（基本のみ） | 4 パターンに増強。CI/CD パイプライン例を追加、クイズエクスポートに `--json \| jq` の実用的パイプを追加 |
| 5 | 注意点のカバー範囲 | 7 項目。セッション期限切れ・動画長時間・具体的エラーメッセージが欠落 | 10 項目に拡充。セッション有効期限（1〜2 週間）、`video_overview` の 15〜30 分、`RuntimeError` メッセージ、`--json` フラグの存在、`storage_state.json` の具体パスを追加 |
| 6 | 関連スキル | 実装詳細寄り（httpx, Click+Rich, pytest-recording）で利用者に不実用 | 利用者目線の連携先に再構成（playwright-cli, LLM エージェント, n8n, cli-anything）。内部実装技術は削除 |
