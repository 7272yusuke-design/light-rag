改善した SKILL.md 全文を出力します:

```markdown
---
name: comfyui
description: ComfyUI のカスタムノード開発・ワークフロー JSON の構築やデバッグ・REST/WebSocket API 経由のバッチ実行・モデルパイプラインの構成変更を行う場合は必ずこのスキルを使え。Stable Diffusion / Flux / HunyuanVideo などの生成 AI パイプラインをノードグラフで組む作業、`NODE_CLASS_MAPPINGS` の登録やテンソル形状の確認が必要な場面にも即座に適用すること。
---

# comfyui

## 概要
ComfyUI は生成 AI モデル（Stable Diffusion, Flux, HunyuanVideo 等）をノードグラフで組み合わせて実行する GUI + バックエンドフレームワーク。画像・動画・音声の生成パイプラインをビジュアルに構築でき、aiohttp ベースの REST/WebSocket API で外部アプリケーションへの組み込みも可能。カスタムノードの追加、LoRA/ControlNet の適用、サードパーティ API との統合まで幅広く対応する。

## いつ使うか
- カスタムノードを新規作成・修正する（`NODE_CLASS_MAPPINGS` への登録、入出力スキーマ定義）
- ワークフロー JSON を生成・編集・デバッグする
- `comfy_api` の versioned インターフェースを使って型安全なノード I/O を実装する
- サーバー API（REST / WebSocket）経由でワークフローをプログラム実行する
- モデルのロード・LoRA 適用・サンプリングパラメータを調整する
- `comfy_extras/` や `comfy_api_nodes/` の既存ノードを拡張・参照する
- グラフ実行のキャッシュ挙動やジョブスケジューリングを調査・改修する
- Docker / GPU 環境でのデプロイ・パフォーマンスチューニング

## 主要コマンド・API

### サーバー起動
```bash
python main.py --listen 0.0.0.0 --port 8188
python main.py --cpu                # GPU なし動作確認
python main.py --preview-method auto  # プレビュー有効化
python main.py --help               # 全オプション確認
```

### カスタムノードの最小実装
```python
# custom_nodes/my_nodes/__init__.py

class MyProcessingNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "strength": ("FLOAT", {
                    "default": 1.0, "min": 0.0, "max": 2.0, "step": 0.01,
                    "tooltip": "処理の強度",
                }),
            },
            "optional": {
                "mask": ("MASK",),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",  # ノード固有ID（進捗通知等で使用）
            },
        }

    RETURN_TYPES = ("IMAGE",)       # ← タプルの末尾カンマ必須（1要素時）
    RETURN_NAMES = ("processed_image",)
    FUNCTION = "process"
    CATEGORY = "my_category/processing"
    OUTPUT_NODE = False  # 終端ノード（SaveImage等）なら True
    DESCRIPTION = "画像に強度パラメータを適用する処理ノード"

    def process(self, image, strength, mask=None, unique_id=None):
        # image: torch.Tensor [B, H, W, C] float32 0-1
        result = image * strength
        if mask is not None:
            result = result * mask.unsqueeze(-1)
        return (result,)  # ← 戻り値もタプル（末尾カンマ必須）

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        # キャッシュを常に無効にする場合は float("NaN") を返す
        return float("NaN")


NODE_CLASS_MAPPINGS = {"MyProcessingNode": MyProcessingNode}
NODE_DISPLAY_NAME_MAPPINGS = {"MyProcessingNode": "My Processing Node"}
```

### versioned API を使った実装（comfy_api）
```python
from comfy_api.v0_0_1 import ImageOutput, ImageInput  # 配布時は固定バージョン

class MyTypedNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"image": ImageInput()}}

    RETURN_TYPES = (ImageOutput(),)
    FUNCTION = "run"
    CATEGORY = "typed_example"

    def run(self, image):
        return (image,)
```

### REST API でワークフローをキュー投入
```python
import json, urllib.request, urllib.parse

SERVER = "http://127.0.0.1:8188"

def queue_prompt(workflow: dict, client_id: str) -> dict:
    payload = json.dumps({"prompt": workflow, "client_id": client_id}).encode()
    req = urllib.request.Request(f"{SERVER}/prompt", data=payload,
                                headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req).read())

def get_history(prompt_id: str) -> dict:
    with urllib.request.urlopen(f"{SERVER}/history/{prompt_id}") as r:
        return json.loads(r.read())

def get_image(filename: str, subfolder: str, folder_type: str) -> bytes:
    params = urllib.parse.urlencode({
        "filename": filename, "subfolder": subfolder, "type": folder_type,
    })
    with urllib.request.urlopen(f"{SERVER}/view?{params}") as r:
        return r.read()
```

### WebSocket で進捗を受信
```python
import websocket, json, uuid

client_id = str(uuid.uuid4())
ws = websocket.WebSocket()
ws.connect(f"ws://127.0.0.1:8188/ws?clientId={client_id}")

while True:
    msg = json.loads(ws.recv())
    if msg["type"] == "executing":
        if msg["data"]["node"] is None:
            print("全ノード実行完了")
            break
        print(f"実行中: ノード {msg['data']['node']}")
    elif msg["type"] == "progress":
        print(f"進捗: {msg['data']['value']}/{msg['data']['max']}")
    elif msg["type"] == "execution_error":
        print(f"エラー: {msg['data']}")
        break
```

### モデルロードと LoRA 適用（コア API）
```python
import comfy.sd, comfy.model_management, folder_paths

# チェックポイントロード
ckpt_path = folder_paths.get_full_path("checkpoints", "model.safetensors")
model, clip, vae, _ = comfy.sd.load_checkpoint_guess_config(ckpt_path)

# LoRA 適用（非破壊的パッチ）
lora_path = folder_paths.get_full_path("loras", "my_lora.safetensors")
model, clip = comfy.sd.load_lora_for_models(model, clip, lora_path,
                                             strength_model=0.8,
                                             strength_clip=0.8)
```

### ノード情報の取得（デバッグ用）
```bash
# 登録済み全ノードのスキーマを取得
curl -s http://127.0.0.1:8188/object_info | python -m json.tool | head -100

# 特定ノードのスキーマ
curl -s http://127.0.0.1:8188/object_info/KSampler | python -m json.tool

# キューの状態確認
curl -s http://127.0.0.1:8188/queue
```

## ワークフロー例

### 1. カスタムノードを追加してサーバーに認識させる
1. `custom_nodes/my_node/` ディレクトリを作成し `__init__.py` に `NODE_CLASS_MAPPINGS` と `NODE_DISPLAY_NAME_MAPPINGS` を定義
2. `python main.py` でサーバーを起動（起動ログに `Import times for custom nodes` でノード名が出ることを確認）
3. `GET /object_info/MyProcessingNode` でノードのスキーマが返ることを確認
4. フロントエンドの Add Node メニューの `CATEGORY` パスに表示されることを確認
5. 入力を接続して実行し、コンソールにエラーが出ないことを検証

### 2. プログラムからワークフローを実行して画像を取得する
1. フロントエンドで目的のワークフローを組み、**Save (API Format)** で JSON をエクスポート（通常保存形式とは異なるので注意）
2. `queue_prompt(workflow, client_id)` でキューに投入し `prompt_id` を取得
3. WebSocket で `executing` イベントを監視し、`node: null` で完了を検知
4. `get_history(prompt_id)` でアウトプットノードの `filename` / `subfolder` / `type` を取得
5. `get_image(filename, subfolder, type)` でバイナリを取得・保存

### 3. 既存ノードに LoRA サポートを追加する
1. `comfy_extras/nodes_lora.py` の `LoraLoader` を参照してパターンを把握
2. `INPUT_TYPES` に `lora_name`（`folder_paths.get_filename_list("loras")` で選択肢生成）と `strength_model` / `strength_clip` パラメータを追加
3. `comfy.sd.load_lora_for_models` を呼び出してモデルパッチを適用
4. `RETURN_TYPES` に `MODEL`, `CLIP` を含めて下流ノードへ渡す

### 4. img2img + ControlNet パイプラインを API で構築する
1. フロントエンドで img2img + ControlNet ワークフローを組み、API Format で JSON をエクスポート
2. JSON 内の `LoadImage` ノードの `image` フィールドに `input/` ディレクトリに配置した画像名を指定
3. `KSampler` の `denoise` を 0.4〜0.7 の範囲で調整（img2img 用）
4. `queue_prompt()` で投入し、WebSocket で完了を待機して結果を取得

## 注意点
- **テンソル形状**: `IMAGE` 型は `[B, H, W, C]` float32（0〜1）。`LATENT` は `{"samples": Tensor[B,C,H,W]}` の dict。`MASK` は `[B, H, W]`。形状を誤るとサイレントに壊れる
- **タプルの末尾カンマ**: `RETURN_TYPES = ("IMAGE",)` — 末尾カンマを忘れると文字列になりノード登録が壊れる。最も多い初心者エラー
- **ノード登録はモジュールトップレベル**: `NODE_CLASS_MAPPINGS` はモジュールのトップレベルに置く。クラス内・関数内・条件分岐内に書いても読み込まれない
- **キャッシュ無効化**: ランダム性を持つノードは `IS_CHANGED` で `float("NaN")` を返すこと。未実装だと入力が同じ場合に前回の結果がキャッシュから返される
- **GPU メモリ管理**: `comfy.model_management` を通じてモデルのロード/オフロードを行う。直接 `.cuda()` / `.cpu()` を呼ぶと ComfyUI の VRAM 管理と競合してクラッシュする
- **OUTPUT_NODE の設定忘れ**: SaveImage や出力系ノードは `OUTPUT_NODE = True` が必須。False のままだとグラフ末端として認識されず実行されない
- **versioned API の互換性**: `comfy_api/latest/` は破壊的変更が入る。配布するカスタムノードは `v0_0_1/` など固定バージョンを参照する
- **ワークフロー JSON の形式**: フロントエンドの通常保存（UI情報含む）と API Format（ノード実行情報のみ）は異なる。`/prompt` エンドポイントには必ず API Format を使う
- **戻り値はタプル**: `return (result,)` — タプルで返さないと下流ノードへの出力マッピングが壊れる
- **サードパーティ API ノード**: `comfy_api_nodes/` の各ノードは対応する API キーの環境変数が必要。未設定時はノードがエラーを返す（エラーメッセージでキー名を確認）

## 関連スキル
- **pytorch**: モデル推論・テンソル操作・カスタムサンプラー実装の基盤
- **stable-diffusion**: 基盤モデルのアーキテクチャ理解（UNet, VAE, CLIP, scheduler）
- **aiohttp**: サーバー拡張・カスタムエンドポイント追加時に参照
- **docker**: GPU パススルーでの本番デプロイ・`docker-compose` によるマルチサービス構成
- **diffusers**: モデル変換（diffusers ↔ ComfyUI 形式）やサンプラー実装の参考
```

**主な改善点:**

| 項目 | 変更内容 |
|---|---|
| **description** | 具体的なトリガーワード（`NODE_CLASS_MAPPINGS`、テンソル形状）を追加し、押しを強化 |
| **カスタムノード例** | `hidden` 入力、`DESCRIPTION`、`IS_CHANGED`、`tooltip`、mask処理を追加。末尾カンマの注意コメント付き |
| **versioned API** | `latest/` → `v0_0_1/` に修正（配布時のベストプラクティスに合わせた） |
| **WebSocket例** | `execution_error` ハンドリングとノード名表示を追加 |
| **デバッグ用コマンド** | `/object_info`、`/queue` の curl 例を新規追加 |
| **ワークフロー#4** | Alembic DB（ニッチ）→ img2img + ControlNet API パイプライン（実践的）に差し替え |
| **注意点** | 末尾カンマ、`OUTPUT_NODE` 設定忘れ、戻り値タプル、`MASK` 形状を追加（頻出ハマりポイント） |
| **関連スキル** | Alembic/SQLAlchemy を削除し `docker`（GPU デプロイ）を追加 |
| **行数** | 185行 → 約190行（500行以下を維持） |
