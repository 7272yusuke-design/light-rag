```markdown
---
name: obsidian-skills
description: ObsidianのVault上でMarkdownノート・Baseデータベース・Canvasマインドマップを作成・編集・整理する作業が発生したら必ずこのスキルを使え。[[Wikiリンク]]・![[埋め込み]]・コールアウト（> [!type]）・フロントマターYAML・.baseスキーマ・.canvas JSON構造・obsidian:// URIスキームのいずれかを扱う場面では即座に参照せよ。
---

# obsidian-skills

## 概要
ObsidianのVaultファイル（.md / .base / .canvas）をAIエージェントが正確に操作するためのSkillパッケージ。Obsidian Flavored Markdownの固有構文（Wikiリンク・埋め込み・コールアウト）、Bases（.base）のYAMLスキーマ、JSON Canvas（.canvas）のノード・エッジ構造、URIスキームによるVault操作の仕様知識を付与し、標準Markdownとの構文差異による誤生成を防ぐ。

## いつ使うか
- ObsidianのVaultディレクトリ内で `.md` ファイルを新規作成・編集するとき
- `[[Wikiリンク]]`・`![[埋め込み]]`・`[[ノート|エイリアス]]` を含むファイルを生成するとき
- コールアウト（`> [!note]`・`> [!warning]+`）を記述するとき
- フロントマターYAML（`---` で囲まれたメタデータブロック）を操作するとき
- `.base` ファイルのフィルタ・フィールド定義・数式・ビュー設定を記述するとき
- `.canvas` ファイルのノード・エッジ構造をJSON形式で生成・編集するとき
- `obsidian://` URIスキームでVault操作を自動化するとき
- Web記事をMarkdownに変換してVaultに取り込むとき

## 主要コマンド・API

### Obsidian Flavored Markdown 構文

```markdown
---
title: プロジェクト計画
tags: [project, 2025Q1]
aliases: [計画書, plan]
created: 2025-01-15
---

# プロジェクト計画

内部リンク: [[議事録/2025-01-15]]
エイリアス付き: [[議事録/2025-01-15|先週の議事録]]
見出しリンク: [[設計書#API仕様]]
ブロックリンク: [[設計書#^block-id]]

画像埋め込み: ![[assets/diagram.png]]
ノート埋め込み: ![[設計書#API仕様]]
PDF埋め込み:  ![[report.pdf#page=3]]
サイズ指定:   ![[diagram.png|400]]

> [!note] 補足情報
> 通常のコールアウト。常に展開状態で表示される。

> [!warning]- 折りたたみ（デフォルト閉じ）
> マイナス記号で閉じた状態がデフォルトになる。

> [!tip]+ 折りたたみ（デフォルト開き）
> プラス記号で開いた状態がデフォルトになる。

> [!abstract]
> [!todo]
> [!success]
> [!question]
> [!failure]
> [!danger]
> [!bug]
> [!example]
> [!quote]

コメント: %% これはObsidian内でのみ表示されるコメント %%
ハイライト: ==ハイライトテキスト==
タスク: - [ ] 未完了タスク
完了:   - [x] 完了タスク
```

### フロントマターの書き方

```yaml
---
# 必須ではないが推奨されるフィールド
title: ノートのタイトル
tags: [tag1, tag2]           # リスト形式
aliases: [別名1, 別名2]      # Wikiリンクの別名解決に使用
created: 2025-01-15
cssclasses: [wide-page]      # カスタムCSS適用

# Dataview等プラグインで使うカスタムフィールド
status: in-progress
due: 2025-03-01
priority: 1
---
```

### .base ファイル（Obsidian Bases）

```yaml
# projects.base — プロジェクト管理データベース
filters:
  and:
    - field: tags
      operator: contains
      value: project
    - field: status
      operator: is-not
      value: done
fields:
  - name: title
    type: text
  - name: status
    type: select
    options: [todo, in-progress, review, done]
  - name: priority
    type: number
  - name: due
    type: date
formulas:
  days_left: "dateDiff(due, now(), 'days')"
  score: "priority * 10 + days_left"
views:
  - type: table
    name: 全プロジェクト
    sort:
      - field: priority
        direction: desc
  - type: board
    name: カンバン
    group_by: status
```

### .canvas ファイル（JSON Canvas）

```json
{
  "nodes": [
    {
      "id": "k7m2x9p4",
      "type": "text",
      "text": "# 中心テーマ\n\nプロジェクトの全体像",
      "x": 0,
      "y": 0,
      "width": 250,
      "height": 100,
      "color": "1"
    },
    {
      "id": "n3f8w1q6",
      "type": "file",
      "file": "Projects/設計書.md",
      "subpath": "#API仕様",
      "x": 350,
      "y": -120,
      "width": 250,
      "height": 100
    },
    {
      "id": "r5t0v2j8",
      "type": "link",
      "url": "https://example.com/docs",
      "x": 350,
      "y": 120,
      "width": 250,
      "height": 100
    }
  ],
  "edges": [
    {
      "id": "e1a2b3c4",
      "fromNode": "k7m2x9p4",
      "fromSide": "right",
      "toNode": "n3f8w1q6",
      "toSide": "left",
      "color": "3",
      "label": "詳細設計"
    },
    {
      "id": "e5d6f7g8",
      "fromNode": "k7m2x9p4",
      "fromSide": "right",
      "toNode": "r5t0v2j8",
      "toSide": "left",
      "label": "参考資料"
    }
  ]
}
```

### obsidian:// URIスキーム

```bash
# 既存ノートを開く（ファイルパスはURLエンコード必須）
open "obsidian://open?vault=MyVault&file=Projects%2F%E8%A8%AD%E8%A8%88%E6%9B%B8"

# 新規ノートを作成して開く
open "obsidian://new?vault=MyVault&name=%E6%96%B0%E8%A6%8F%E3%83%8E%E3%83%BC%E3%83%88&content=%E6%9C%AC%E6%96%87"

# 検索を実行
open "obsidian://search?vault=MyVault&query=tag%3Aproject"

# 日次ノートを開く（Daily Notesプラグイン）
open "obsidian://daily-note?vault=MyVault"

# Advanced URI プラグイン利用時
open "obsidian://adv-uri?vault=MyVault&filepath=Projects/設計書.md&heading=API仕様"
```

## ワークフロー例

### Wikiリンク付きノートの新規作成

1. フロントマターYAMLを `---` で囲んで先頭に記述する
   ```yaml
   ---
   title: 週次レビュー 2025-01-20
   tags: [weekly-review, 2025Q1]
   created: 2025-01-20
   ---
   ```
2. 本文で `[[リンク先]]` を記述する際、Vault内のファイル一覧を `find vault/ -name "*.md"` で取得し、実在パスと照合する
3. サブディレクトリ内のファイルへのリンクは `[[subfolder/ファイル名]]` ではなく `[[ファイル名]]` で記述する（Obsidianはファイル名で自動解決する）。同名ファイルが複数ある場合のみフルパスを指定
4. コールアウトを使う場合、型名を `note` `warning` `tip` `info` `success` `error` `bug` `example` `quote` `abstract` `todo` `question` `failure` `danger` から選択する。存在しない型名を書くと通常の引用ブロックとして描画される（エラーは出ない）
5. バリデーション：フロントマター閉じ `---` の存在、`%%コメント%%` の閉じ忘れ、Wikiリンク先の存在を確認

### Baseデータベースの設計・作成

1. 管理したいデータの構造を決める：フィールド名・型（`text` `number` `select` `date` `checkbox`）・選択肢
2. `.base` ファイルを作成し、`filters` → `fields` → `formulas` → `views` の順でYAMLを組み立てる
3. フィルタの `operator` は型により使えるものが異なる：
   - text: `is` `is-not` `contains` `starts-with` `ends-with`
   - number: `is` `is-not` `gt` `gte` `lt` `lte`
   - select: `is` `is-not`
   - date: `is` `is-before` `is-after` `is-on-or-before` `is-on-or-after`
4. インデントは**スペース2つ**で統一する（タブを使うとパースエラー）
5. 数式内でフィールド名を参照する場合、フィールド名にスペースがあればバッククォートで囲む

### Canvasマインドマップの生成

1. ノードIDを8文字の英数字ランダム文字列で生成する（`uuidgen | cut -c1-8` や `openssl rand -hex 4` で生成可能）
2. 中心ノードを `x:0, y:0` に配置する
3. 周辺ノードを放射状に配置する目安：
   - 右方向: `x:350, y:-120` / `x:350, y:0` / `x:350, y:120`
   - 左方向: `x:-350, y:-120` / `x:-350, y:0` / `x:-350, y:120`
   - ノード間隔は最低120px確保する
4. ノード `type` は `text`（Markdown記述可）・`file`（Vault内ファイル参照）・`link`（外部URL）・`group`（グループ化枠）から選択
5. `color` は `"1"`〜`"6"` の文字列で指定（数値ではない）
6. エッジの `fromSide` / `toSide` は `top` `bottom` `left` `right` から選択
7. バリデーション：ノードIDの重複なし、エッジの `fromNode`/`toNode` が実在するノードIDを参照、`type: file` のパスがVault内に存在

### Web記事のVault取り込み

1. Web記事のHTMLを取得し、Markdown形式に変換する（Readability系ツールやブラウザ拡張で本文抽出）
2. フロントマターを付与する：
   ```yaml
   ---
   title: 記事タイトル
   source: https://example.com/article
   created: 2025-01-20
   tags: [clipping]
   ---
   ```
3. Markdown内の標準リンク `[text](url)` のうち、Vault内ノートへの参照に変換できるものを `[[ノート名]]` に置換する
4. 画像はローカルにダウンロードして `assets/` に保存し、`![[assets/image.png]]` に書き換える

## 注意点

- **`[[Wikiリンク]]` はObsidian固有構文**：GitHub・VS Code等では認識されずリテラル表示される。ポータビリティが必要なら `[表示名](ファイル.md)` を併用すること
- **フロントマターの `---` 閉じ忘れ**：ファイル全体がYAMLとして誤認識され、本文が一切表示されなくなる致命的バグ。エラーメッセージは出ない（無音の失敗）
- **コールアウト型名のスペルミス**：`[!noe]` のように間違えても通常の引用ブロックとして描画されるだけでエラーにならない。型名は大文字小文字不問だがスペルは正確に
- **`![[埋め込み]]` のパス解決**：Obsidianの設定（「新しいリンクの形式」）により相対パス・最短パス・絶対パスの挙動が変わる。デフォルトは最短パス（ファイル名のみ）
- **`.base` ファイルのタブインデント**：YAMLパーサーが無言でフィールドを無視する。必ずスペース2つを使用すること
- **Canvas `type: file` ノード**：Vault外のパスや存在しないファイルを指定しても**エラーは出ず空ノードが表示される**（無音の失敗）
- **Canvas ノードID**：重複すると一方のノードが消える。エッジが参照する `fromNode`/`toNode` が存在しないIDの場合、そのエッジは無言で無視される
- **Canvas `color` の型**：文字列 `"1"` であり数値 `1` ではない。数値で書いてもObsidianは読み込むが、保存時に文字列に変換されるためdiffが発生する
- **`obsidian://` URIのエンコード**：日本語・スペース・スラッシュはすべてURLエンコード必須（`%20` `%2F` `%E6%97%A5`）。エンコード漏れはリンクが機能しない
- **`%%コメント%%` の閉じ忘れ**：以降のテキストがすべて非表示になる（エディタモードでのみ確認可能）
- **フロントマターの `tags` フィールド**：文字列（`tags: "tag1"`）とリスト（`tags: [tag1, tag2]`）の両方を受け付けるが、リスト形式を推奨。ネストされたタグは `tags: [parent/child]` でスラッシュ区切り
- **`==ハイライト==` 構文**：標準Markdownではサポートされない。GitHub等にエクスポートする場合は `<mark>` タグに変換すること

## 関連スキル
- **defuddle**: Web記事のMarkdown変換とVault取り込みワークフロー
- **git**: VaultをGitリポジトリとして管理する場合のバージョン管理（`.obsidian/` を `.gitignore` に含めるか要判断）
- **dataview**: Dataviewプラグインのクエリ言語によるノートの動的集約・テーブル表示
- **templater**: Templaterプラグインによるノートテンプレートの自動展開・日付挿入
- **mermaid**: Obsidianが標準サポートするMermaid図（フローチャート・シーケンス図）の記述
```
