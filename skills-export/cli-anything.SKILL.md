改善したSKILL.md全文を出力します。

---

```markdown
---
name: cli-anything
description: GUIアプリケーション（GIMP・Blender・Audacity等）をAIエージェントがCLI経由で制御するためのハーネスを構築・拡張するとき、またはClickベースのPython CLIでデスクトップアプリのAPI/自動化インターフェースをREPL+JSON出力でラップしたいときに使うスキル。HARNESS.md規約に準拠したCLIハーネスの設計・実装・テスト・SKILL.md生成まで全工程をカバーする。
---

# cli-anything

## 概要
CLI-Anythingは、GUIアプリケーション向けのステートフルなCLIハーネスを構築するフレームワーク。ClickベースのPython CLIでアプリのAPIや自動化インターフェースをラップし、REPLモードとJSON出力によってAIエージェントがGIMP・Blender・Audacity等30以上のツールを一貫したインターフェースで操作できるようにする。HARNESS.mdが定義する統一パターンに従い、各ハーネスは`core/`（ドメインロジック）、`utils/`（バックエンドアダプター＋REPL skin）、`skills/SKILL.md`（エージェント向けケイパビリティ記述）、CLIエントリーポイントの4層構造を持つ。

## いつ使うか
- AIエージェントにGIMPで画像編集・Blenderで3Dモデリング・Audacityで音声処理などをさせたいとき
- GUIしか持たないソフトウェアに対してCLI抽象レイヤーを新規構築したいとき
- 既存のCLIハーネスに新コマンドを追加、またはバックエンドアダプターを別アプリ向けに実装するとき
- エージェントパイプラインで`--json`出力をパースしながら複数ツールを連鎖実行させたいとき
- REPLモードとワンショットコマンドの両方を同一CLIで提供したいとき

## 主要コマンド・API

### ハーネスのディレクトリ構造
```
myapp-harness/
├── myapp_cli.py          # Clickベースのエントリーポイント
├── myapp_backend.py      # アプリAPIとの通信を隔離するアダプター
├── core/                 # ドメインロジック
├── utils/
│   └── repl_skin.py      # 共有REPL UI（ブランディング・テーブル・色付き出力）
├── skills/
│   └── SKILL.md          # エージェント向けケイパビリティ記述
├── tests/
│   └── test_myapp.py     # バックエンドモックによるユニットテスト
└── registry.json         # CLI-Hubへの登録情報
```

### バックエンドアダプター（*_backend.py）
```python
# gimp_backend.py: 全てのアプリAPI呼び出しをここに隔離する
class GimpBackend:
    def __init__(self, host="localhost", port=10008):
        self.connection = self._connect(host, port)

    def open_image(self, path: str) -> dict:
        """GIMPのScript-Fu経由で画像を開く"""
        result = self._execute(f'(gimp-file-load RUN-NONINTERACTIVE "{path}" "{path}")')
        return {"image_id": result, "filename": path, "status": "ok"}

    def apply_filter(self, image_id: int, filter_name: str, **params) -> dict:
        """フィルター適用。パラメータはフィルターごとに異なる"""
        cmd = self._build_filter_command(filter_name, image_id, params)
        self._execute(cmd)
        return {"image_id": image_id, "filter": filter_name, "status": "ok"}

    def list_layers(self, image_id: int) -> dict:
        layers = self._execute(f"(gimp-image-get-layers {image_id})")
        return {"layers": layers, "count": len(layers), "status": "ok"}
```

### CLIエントリーポイント（Clickベース）
```python
# gimp_cli.py
import json
import click
from utils.repl_skin import start_repl
from gimp_backend import GimpBackend

@click.group()
@click.option("--host", default="localhost", help="GIMP Script-Fu console host")
@click.option("--port", default=10008, help="GIMP Script-Fu console port")
@click.pass_context
def cli(ctx, host, port):
    ctx.ensure_object(dict)
    ctx.obj["backend"] = GimpBackend(host=host, port=port)

@cli.command()
@click.argument("path", type=click.Path(exists=True))
@click.option("--json", "as_json", is_flag=True, help="JSON output for agent consumption")
@click.pass_context
def open_image(ctx, path, as_json):
    """画像ファイルを開く"""
    result = ctx.obj["backend"].open_image(path)
    click.echo(json.dumps(result) if as_json else f"Opened: {result['filename']}")

@cli.command()
@click.argument("image_id", type=int)
@click.argument("filter_name")
@click.option("--radius", type=float, default=5.0)
@click.option("--json", "as_json", is_flag=True)
@click.pass_context
def apply_filter(ctx, image_id, filter_name, radius, as_json):
    """フィルターを適用"""
    result = ctx.obj["backend"].apply_filter(image_id, filter_name, radius=radius)
    click.echo(json.dumps(result) if as_json else f"Applied {filter_name}")

@cli.command()
@click.pass_context
def repl(ctx):
    """インタラクティブREPLを起動"""
    start_repl(cli, ctx, prompt="gimp> ", banner="GIMP Harness v1.0")

@cli.command()
def version():
    """バージョン情報を表示（HARNESS.md必須コマンド）"""
    click.echo(json.dumps({"name": "gimp-harness", "version": "1.0.0"}))

@cli.command()
@click.pass_context
def status(ctx):
    """接続状態を確認（HARNESS.md必須コマンド）"""
    ok = ctx.obj["backend"].is_connected()
    click.echo(json.dumps({"connected": ok, "status": "ok" if ok else "disconnected"}))
```

### ワンショット実行とREPL
```bash
# ワンショット実行（エージェントパイプライン向け）
python gimp_cli.py open-image /path/to/image.png --json
# => {"image_id": 1, "filename": "/path/to/image.png", "status": "ok"}

python gimp_cli.py apply-filter 1 blur --radius 5.0 --json
# => {"image_id": 1, "filter": "blur", "status": "ok"}

# パイプライン連携
python gimp_cli.py open-image photo.png --json \
  | jq -r '.image_id' \
  | xargs -I{} python gimp_cli.py apply-filter {} unsharp-mask --radius 2.0 --json

# インタラクティブREPL（履歴・補完付き）
python gimp_cli.py repl
gimp> open-image photo.png
gimp> apply-filter 1 blur --radius 3
gimp> status
```

### repl_skin.pyの共有UIコンポーネント
```python
from utils.repl_skin import start_repl, print_table, print_success, print_error

# テーブル形式で出力（レイヤー一覧等）
print_table(
    headers=["ID", "Name", "Visible", "Opacity"],
    rows=[(1, "Background", True, 100), (2, "Layer 1", True, 80)]
)

# 色付きステータス出力
print_success("Filter applied successfully")
print_error("Connection to GIMP lost")

# REPLセッション開始
start_repl(cli, ctx, prompt="gimp> ", banner="GIMP Harness v1.0")
```

### registry.jsonへの登録
```json
{
  "harnesses": [
    {
      "name": "gimp",
      "description": "GNU Image Manipulation Program harness",
      "entry": "gimp_cli.py",
      "skill": "skills/SKILL.md",
      "tags": ["image", "editing", "creative"],
      "requires": ["gimp >= 2.10"]
    }
  ]
}
```

### バックエンドのモックテスト
```python
# tests/test_gimp.py
from unittest.mock import MagicMock, patch
from click.testing import CliRunner
from gimp_cli import cli

def test_open_image_json():
    runner = CliRunner()
    with patch("gimp_cli.GimpBackend") as MockBackend:
        MockBackend.return_value.open_image.return_value = {
            "image_id": 1, "filename": "test.png", "status": "ok"
        }
        result = runner.invoke(cli, ["open-image", "test.png", "--json"])
        assert '"image_id": 1' in result.output
        assert result.exit_code == 0

def test_apply_filter():
    runner = CliRunner()
    with patch("gimp_cli.GimpBackend") as MockBackend:
        MockBackend.return_value.apply_filter.return_value = {
            "image_id": 1, "filter": "blur", "status": "ok"
        }
        result = runner.invoke(cli, ["apply-filter", "1", "blur", "--json"])
        assert '"status": "ok"' in result.output
```

## ワークフロー例

### 新規ハーネスの構築（例: Inkscape）
1. **HARNESS.mdを読む** — 統一パターンの構造・命名規則・必須コマンド（`repl`, `version`, `status`）を確認
2. **バックエンドアダプターを作成** — `inkscape_backend.py`にInkscapeのD-Bus APIまたはCLIラッパーを実装。全てのアプリ通信をここに隔離
3. **CLIエントリーポイントを作成** — `inkscape_cli.py`でClickグループとサブコマンドを定義。全コマンドに`--json`フラグを付与
4. **repl_skin.pyをutils/にコピー** — 既存ハーネスから**そのまま**コピー（改変不可・単一ソースオブトゥルース制約）
5. **テストを書く** — `CliRunner` + `unittest.mock.patch`でバックエンドをモックしたテストを作成
6. **skills/SKILL.mdを生成** — `python skill_generator.py --harness inkscape_cli.py --output skills/SKILL.md`
7. **registry.jsonに登録** — `requires`フィールドにInkscapeのバージョン要件を明記

### エージェントによるGIMP画像処理パイプライン
1. エージェントが`skills/SKILL.md`を読んで利用可能なコマンドを把握
2. `python gimp_cli.py status --json`で接続を確認（`{"connected": true}`）
3. `python gimp_cli.py open-image photo.png --json`で画像を開き`image_id`を取得
4. `python gimp_cli.py list-layers 1 --json`でレイヤー構造を確認
5. `python gimp_cli.py apply-filter 1 unsharp-mask --radius 2.0 --json`でシャープネス適用
6. `python gimp_cli.py export 1 --format png --output result.png --json`でエクスポート
7. 各ステップのJSON出力をパースして次コマンドの引数に渡す。エラー時は`status`フィールドで分岐

### 複数ハーネスの連携（画像→音声パイプライン）
1. `python gimp_cli.py open-image frame.png --json` → 画像処理
2. `python gimp_cli.py export 1 --format png --output processed.png --json`
3. `python audacity_cli.py import-audio narration.wav --json` → 音声にエフェクト追加
4. `python audacity_cli.py apply-effect 1 normalize --json`
5. `python blender_cli.py import-image processed.png --json` → 3Dシーンに合成
6. 各ハーネスの`--json`出力を`jq`でパースして次のハーネスに渡す

## 注意点
- **バックエンドの隔離は絶対** — `*_backend.py`以外でアプリAPIを直接呼ぶとモックテストが成立しなくなる。`core/`やCLIレイヤーからのAPI直接呼び出しは禁止
- **`--json`フラグは全コマンド必須** — エージェントが出力をパースするため、一つでも欠けるとパイプラインが止まる。後付けは困難なので初期実装時に必ず入れる
- **実アプリの起動が前提** — バックエンドは実際のアプリケーションインスタンスと通信する。CI環境やアプリ未インストール環境では必ずバックエンドをモックする。Docker経由でアプリを起動するE2Eテストパターンもある
- **repl_skin.pyは改変不可** — 全ハーネスで同一ファイルをコピーして使う単一ソースオブトゥルース制約がある。ハーネス固有のカスタマイズをrepl_skinに入れるとUI一貫性が崩壊する
- **セッション状態はREPL内のみ** — ワンショット実行間で状態は引き継がれない。エージェントが複数コマンドを跨いで状態を使うには`image_id`等の識別子を明示的にJSON経由で渡す
- **アプリバージョン依存** — ハーネスは特定のアプリバージョンのAPI/自動化インターフェースに依存する。アプリ更新時にバックエンドの動作確認が必要
- **HARNESS.md必須コマンドを省かない** — `repl`、`version`、`status`は規約上必須。省略するとCLI-Hubバリデーションで弾かれる

## 関連スキル
- **click** — CLIエントリーポイントの基盤。グループ・サブコマンド・オプション設計の中心
- **GIMP Script-Fu / Blender bpy / Audacity mod-script-pipe** — バックエンドアダプターが呼び出す各アプリ固有のAPI
- **pytest + unittest.mock + click.testing.CliRunner** — バックエンドモックとCLI出力のテスト手法
- **jq** — エージェントパイプラインでJSON出力をフィルタ・変換する際に使用
- **browser-use** — GUIアプリのCLI化が困難な場合の代替手段としてブラウザ経由の操作を検討
```

---

**改善ポイントの要約:**

| 基準 | 元の評価 | 改善内容 |
|---|---|---|
| 1. description精度 | 「迷わずこれを使え」が空虚 | 具体的な技術トリガー（Click, REPL, JSON, HARNESS.md）を列挙し、何をカバーするか明示 |
| 2. 500行以下 | 160行 OK | 200行弱。テストコードとディレクトリ構造を追加しても範囲内 |
| 3. コマンド例 | 存在しないスラッシュコマンド(`/build-harness`等)あり | 全削除。実在するパターンのみに限定。コマンド引数を具体化（`image_id`を明示的に渡す等） |
| 4. ワークフロー | 概念的すぎた | `status`確認→open→処理→exportの具体的フロー。複数ハーネス連携例を追加 |
| 5. 注意点 | repl_skinの単一ソース制約・アプリバージョン依存が欠落 | ソース資料から2つの重要なハマりポイントを追加 |
| 6. 関連スキル | `python-subprocess / pyautogui`は的外れ | 削除。`browser-use`を代替手段として追加、テスト手法を`CliRunner`まで具体化 |
