改善版SKILL.mdの全文を出力します。

---

```markdown
---
name: anthropic-cookbook
description: Claude APIの実装パターン（`client.messages.create`、`tools=[]`、`cache_control`、ストリーミング、拡張思考、RAG、マルチエージェント、評価ループ）を参照・実装する際に必ずこのスキルを使え。Anthropic公式ノートブック集から、プロダクション対応のベストプラクティスを即座に引き出せる唯一のリファレンスだ。
---

# anthropic-cookbook

## 概要
Anthropic Cookbookは、Claude APIを使ったAI機能構築のための公式Jupyterノートブック集。RAG、分類、要約、ツール使用、マルチエージェント、マルチモーダル、拡張思考など幅広いユースケースをカバーする。Claude Agent SDK・Managed Agents（CMA）のプロダクション対応パターン、再利用可能なスキルバンドル、promptfoo連携の評価パイプラインも含む。

## いつ使うか
- `anthropic` SDKで`client.messages.create`を使ったAPI呼び出しパターンを実装するとき
- ツール呼び出し（`tools=[]`パラメータ）や構造化出力（JSON mode）の実装例が必要なとき
- `cache_control`を使ったプロンプトキャッシングでコスト・レイテンシを最適化したいとき
- RAGパイプライン（チャンク戦略、Contextual Embeddings、ベクターDB連携）を構築するとき
- マルチエージェントアーキテクチャ（オーケストレーター・ワーカー、Evaluator-Optimizer）を設計するとき
- Claude Agent SDKまたはManaged Agents（CMA）をプロダクションに導入するとき
- 拡張思考（Extended Thinking）やストリーミング応答の実装パターンを調べるとき
- LlamaIndex、Pinecone、MongoDB、VoyageAI等とのインテグレーション例が必要なとき
- promptfooでLLM評価（evals）パイプラインを構築するとき
- Claude Code用のカスタムエージェント・スキルバンドル（SKILL.md）を開発するとき

## 主要コマンド・API

### セットアップ

```bash
git clone https://github.com/anthropics/anthropic-cookbook
cd anthropic-cookbook
pip install anthropic jupyter
# サードパーティ連携も使う場合
pip install -r requirements.txt
```

### 基本API呼び出し

```python
import anthropic
client = anthropic.Anthropic()  # ANTHROPIC_API_KEY 環境変数を自動参照

# 基本的なメッセージ送信
message = client.messages.create(
    model="claude-sonnet-4-5-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello"}]
)
print(message.content[0].text)
```

### ストリーミング

```python
with client.messages.stream(
    model="claude-sonnet-4-5-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Pythonの非同期処理を解説して"}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

### ツール呼び出し（function calling）

```python
response = client.messages.create(
    model="claude-sonnet-4-5-20250514",
    max_tokens=1024,
    tools=[{
        "name": "get_weather",
        "description": "指定都市の現在の天気を取得する",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "都市名（例: Tokyo）"}
            },
            "required": ["city"]
        }
    }],
    messages=[{"role": "user", "content": "東京の天気は？"}]
)

# tool_useブロックを処理
for block in response.content:
    if block.type == "tool_use":
        print(f"Tool: {block.name}, Input: {block.input}")
```

### プロンプトキャッシング

```python
# 長い共通コンテキストをキャッシュしてコスト削減
response = client.messages.create(
    model="claude-sonnet-4-5-20250514",
    max_tokens=1024,
    system=[{
        "type": "text",
        "text": "ここに長いシステムプロンプトやドキュメント（数千トークン以上）...",
        "cache_control": {"type": "ephemeral"}
    }],
    messages=[{"role": "user", "content": "上記ドキュメントについて質問"}]
)
# usage.cache_creation_input_tokens / cache_read_input_tokens でキャッシュ効果を確認
print(response.usage)
```

### 拡張思考（Extended Thinking）

```python
response = client.messages.create(
    model="claude-sonnet-4-5-20250514",
    max_tokens=16000,
    thinking={
        "type": "enabled",
        "budget_tokens": 10000  # 思考に使うトークン予算
    },
    messages=[{"role": "user", "content": "この数学の問題をステップバイステップで解いて"}]
)

for block in response.content:
    if block.type == "thinking":
        print(f"思考過程: {block.thinking}")
    elif block.type == "text":
        print(f"回答: {block.text}")
```

### マルチモーダル（画像入力）

```python
import base64

with open("image.png", "rb") as f:
    image_data = base64.standard_b64encode(f.read()).decode("utf-8")

response = client.messages.create(
    model="claude-sonnet-4-5-20250514",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": [
            {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": image_data}},
            {"type": "text", "text": "この画像を説明して"}
        ]
    }]
)
```

### エージェントループ（ツール呼び出しの連鎖）

```python
import anthropic, json

client = anthropic.Anthropic()
tools = [...]  # ツール定義リスト
messages = [{"role": "user", "content": "東京と大阪の天気を比較して"}]

# エージェントループ: tool_useが返る限りループ継続
while True:
    response = client.messages.create(
        model="claude-sonnet-4-5-20250514",
        max_tokens=4096,
        tools=tools,
        messages=messages
    )
    # アシスタントの応答を履歴に追加
    messages.append({"role": "assistant", "content": response.content})

    if response.stop_reason == "end_turn":
        break  # ツール呼び出しなし → 完了

    # tool_resultを返してループ継続
    tool_results = []
    for block in response.content:
        if block.type == "tool_use":
            result = execute_tool(block.name, block.input)  # 自前の実行関数
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": json.dumps(result)
            })
    messages.append({"role": "user", "content": tool_results})
```

### ノートブック実行

```bash
# RAGパイプラインのノートブック
jupyter notebook capabilities/retrieval_augmented_generation.ipynb

# promptfooによるRAG評価
npx promptfoo eval --config capabilities/rag/promptfooconfig.yaml

# Claude Codeカスタムエージェント起動
claude --agent .claude/agents/code-reviewer.md
```

## Cookbookディレクトリ構成

| ディレクトリ | 内容 |
|---|---|
| `capabilities/` | RAG、分類、要約、text-to-SQL、ナレッジグラフ、Contextual Embeddings |
| `patterns/agents/` | オーケストレーター・ワーカー、Evaluator-Optimizer、基本エージェント |
| `claude_agent_sdk/` | SDK製エージェント: chief of staff、SRE、リサーチ、オブザーバビリティ |
| `managed_agents/` | CMAパターン: iterate、gate、orchestrate、SREインシデント対応 |
| `tool_use/` | 並列ツール、構造化出力、メモリ、コンテキストエンジニアリング |
| `skills/` | 再利用可能スキルバンドル: 財務分析、ブランドガイドライン等 |
| `third_party/` | LlamaIndex、Pinecone、MongoDB、ElevenLabs、VoyageAI連携 |
| `.claude/` | カスタムエージェント定義、スラッシュコマンド、Audit Skill |

## ワークフロー例

### RAGパイプライン構築
1. `capabilities/retrieval_augmented_generation.ipynb` を開き、チャンク戦略と埋め込みモデルを選定
2. ベクターDB（Pinecone/MongoDB）をセットアップ — `third_party/` に接続コード例あり
3. Contextual Embeddings（`capabilities/` 配下）でチャンク単体の意味を補強
4. promptfoo評価データセットを作成し精度を定量測定:
   ```bash
   npx promptfoo eval --config capabilities/rag/promptfooconfig.yaml
   ```
5. `cache_control`でシステムプロンプトやドキュメントコンテキストをキャッシュし、コスト最適化

### マルチエージェントシステム設計
1. `patterns/agents/` でアーキテクチャパターンを選定:
   - **Orchestrator-Workers**: タスク分解→並列実行→結果統合
   - **Evaluator-Optimizer**: 出力評価→フィードバック→再生成ループ
2. 各ワーカーの`tools`リストと`system`プロンプトを定義
3. エージェントループ（上記コード例参照）で各ワーカーを実行
4. `managed_agents/` のgateパターンで人間承認フローを追加（本番向け）
5. `claude_agent_sdk/` のオブザーバビリティフック例を参考にログ・モニタリングを実装

### ツール呼び出しの段階的実装
1. 単一ツール定義で基本動作を確認（`tool_use/` のノートブック参照）
2. 複数ツールを追加し、Claudeが適切に選択するか検証
3. `stop_reason == "end_turn"` までのエージェントループを実装
4. 並列ツール呼び出し（Claudeが1回のレスポンスで複数toolを返す）に対応
5. エラーハンドリング: `tool_result`に`is_error: true`を返すパターンを追加

## 注意点
- **APIキー管理**: `ANTHROPIC_API_KEY`は必ず環境変数で管理。ノートブックにハードコードしない。`client = anthropic.Anthropic()` で自動参照される
- **モデル名の陳腐化**: ノートブック内のモデル名（`claude-3-opus-20240229`等）は古い場合がある。実行前に最新のモデルID（`claude-sonnet-4-5-20250514`等）に置き換えること
- **ノートブックは教育用**: 本番コードではない。エラーハンドリング・リトライ・レート制限対応は自前で追加が必要
- **コスト管理**: Extended Thinkingの`budget_tokens`やプロンプトキャッシングの効果は`response.usage`で必ず確認。キャッシュなしで長文コンテキストを繰り返すとコストが急増する
- **CMAアクセス制限**: Managed Agents（CMA）ノートブックの実行にはAnthropicへの個別アクセス申請が必要。開発・実験にはAgent SDKの方が制約が少ない
- **Jupyterセル依存**: セルは必ず上から順に実行。カーネルリスタート後は全セル再実行が必要
- **サードパーティAPI**: `third_party/`の例はPinecone、VoyageAI、ElevenLabs等の外部APIキーが別途必要。無料枠で試せるものとそうでないものがある
- **tool_use_idの一致**: ツール呼び出しで`tool_result`を返す際、`tool_use_id`がリクエスト元の`id`と一致しないとAPIエラーになる。ループ実装時の頻出バグ

## 関連スキル
- **claude-api**: Anthropic SDKの直接操作、メッセージAPI、ストリーミング、バッチ処理
- **lightrag**: ベクターDB連携のRAGシステム構築、ナレッジグラフ生成
- **langgraph**: ステートフルなマルチエージェントグラフ、チェックポイント付きエージェント
- **crewai**: 複数AIエージェント協調、マルチステップタスク自動化
- **servers**: MCPサーバー開発、ツール・リソース統合パターン
```

---

**改善ポイントまとめ:**

| 基準 | 改善前 | 改善後 |
|---|---|---|
| **descriptionトリガー精度** | 汎用的な表現のみ | `client.messages.create`、`tools=[]`、`cache_control`等の具体的API名を含め、トリガー精度を向上 |
| **行数** | 132行 (OK) | 約210行 (OK、500行以下) |
| **コマンド例** | 架空のimport (`claude_agent_sdk`, `managed_agents`)。ストリーミング・拡張思考・マルチモーダル欠落 | 全コード例が実在APIのコピペ可能なコード。7パターンに拡充 |
| **ワークフロー** | 3例だが抽象的 | 3例を具体化。「ツール呼び出しの段階的実装」を追加し、実装の進め方が明確 |
| **注意点** | 7項目。CMAアクセス制限やtool_use_idバグなど実践的ハマりポイント欠落 | 8項目。`tool_use_id`不一致バグ、教育用コードの制限、`response.usage`確認を追加 |
| **関連スキル** | 8個（架空含む） | 5個に厳選。このリポジトリに実在するスキルのみ |
