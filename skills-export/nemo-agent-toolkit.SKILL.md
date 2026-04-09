```markdown
---
name: nemo-agent-toolkit
description: NVIDIA NeMo Agent Toolkit (NAT) を使ってLLMエージェントワークフローの構築・評価・最適化・プロファイリングを行うときに必ずこのスキルを使え。`nvidia_nat_core`・`nvidia_nat_app`・`nvidia_nat_langchain`・`nvidia_nat_eval`・`nvidia_nat_profiler`・`nvidia_nat_mcp`・`nvidia_nat_a2a`・`nvidia_nat_config_optimizer`・`nvidia_nat_security`・プラグインレジストリ・ATIF軌跡フォーマット・YAML設定コンパイル・投機的実行・ミドルウェアパイプラインが関わる場面では即座にこのスキルを参照せよ。
---

# nemo-agent-toolkit

## 概要
NVIDIA NeMo Agent Toolkit (NAT) はLLM駆動のエージェントワークフローを構築・実行・評価・最適化するPythonフレームワークである。プラグインベースアーキテクチャにより複数のAIフレームワーク（LangChain、LlamaIndex、AutoGen、Haystack、Semantic Kernel、Strands、CrewAI、Google ADK）と統合し、ReAct・ReWOO・tool-calling・routerなどのエージェントパターンをサポートする。YAML設定による宣言的ワークフロー定義、投機的実行、ATIF軌跡フォーマットによる評価・ファインチューニング、REST API・MCP・A2Aプロトコルでのワークフロー公開を標準搭載する。

## いつ使うか
- YAML設定でLLMエージェントワークフローを宣言的に定義・コンパイル・実行するとき
- 複数AIフレームワーク（LangChain、AutoGen、Haystack等）を統一オブザーバビリティで運用するとき
- ReAct・ReWOO・tool-calling・routerパターンのエージェントを構築するとき
- エージェント軌跡をATIF形式で記録し、評価・ファインチューニングデータ生成を行うとき
- LLMワークフローのプロファイリング（トークン使用量・ボトルネック検出・GPU sizing）を行うとき
- ワークフローをMCPサーバーまたはA2Aプロトコルで公開するとき
- プロンプト・設定の遺伝的アルゴリズム最適化（Pareto-front分析）を実行するとき
- セキュリティ Red-teaming・PII防御・コンテンツガードのミドルウェアを適用するとき
- NIM・NeMo Customizer・Dynamoとのエンタープライズ統合を行うとき

## 主要コマンド・API

### インストール
```bash
# コアパッケージ（最小構成）
pip install nvidia-nat-core

# LangChain統合（ReAct、ReWOO、tool-calling等）
pip install nvidia-nat-langchain

# ワークフローコンパイラ・実行エンジン
pip install nvidia-nat-app

# 評価ハーネス
pip install nvidia-nat-eval

# プロファイラ
pip install nvidia-nat-profiler

# MCPサーバー/クライアント
pip install nvidia-nat-mcp
pip install nvidia-nat-fastmcp

# A2Aプロトコル
pip install nvidia-nat-a2a

# セキュリティ（Red-teaming、防御ミドルウェア）
pip install nvidia-nat-security

# 設定オプティマイザ
pip install nvidia-nat-config-optimizer

# 全部入り（開発環境向け）
pip install nvidia-nat-core[all]
```

### CLI基本操作
```bash
# ワークフロー一覧確認
nat list workflows

# YAML設定からワークフローを実行
nat run --config workflow.yaml

# FastAPIサーバーとして公開
nat serve --config workflow.yaml --host 0.0.0.0 --port 8000

# MCPサーバーとして公開
nat serve --config workflow.yaml --frontend mcp

# コンソール対話モード
nat run --config workflow.yaml --frontend console

# プロファイリング実行
nat profile --config workflow.yaml --output profile_report.json
```

### プラグインレジストリ（コア設計パターン）
```python
from nvidia_nat_core.registry import register, get_registry

# カスタムLLMプロバイダーの登録
@register("llm", "my_custom_llm")
class MyCustomLLM:
    def __init__(self, model_name: str, **kwargs):
        self.model_name = model_name

    async def generate(self, prompt: str) -> str:
        # カスタム実装
        return await my_api_call(prompt)

# レジストリからコンポーネントを取得
registry = get_registry()
llm = registry.get("llm", "my_custom_llm")(model_name="my-model")
```

### YAML設定によるワークフロー定義
```yaml
# workflow.yaml
name: research-assistant
description: "リサーチアシスタント: 検索→分析→要約"

llm:
  provider: openai
  model: gpt-4o
  temperature: 0.7

tools:
  - name: web_search
    type: builtin.web_search
  - name: document_reader
    type: builtin.document_reader

agents:
  researcher:
    type: react           # ReActパターン
    llm: ${llm}
    tools: [web_search]
    system_prompt: "あなたはリサーチ専門家です。"

  analyst:
    type: tool_calling     # tool-callingパターン
    llm: ${llm}
    tools: [document_reader]
    system_prompt: "あなたはデータ分析専門家です。"

  summarizer:
    type: react
    llm: ${llm}
    system_prompt: "あなたは要約専門家です。"

workflow:
  # 計算グラフとして定義: ノードとエッジ
  nodes:
    - id: research
      agent: researcher
    - id: analyze
      agent: analyst
    - id: summarize
      agent: summarizer

  edges:
    - from: research
      to: analyze
    - from: analyze
      to: summarize

  entry: research
  exit: summarize

middleware:
  - type: cache
    ttl: 3600
  - type: logging
    level: INFO
  - type: timeout
    seconds: 120

frontend:
  type: fastapi
  port: 8000
```

### LangChain統合エージェント（Python API）
```python
from nvidia_nat_langchain.agents import create_react_agent, create_rewoo_agent
from nvidia_nat_core.llm import get_llm
from langchain_core.tools import tool

@tool
def search(query: str) -> str:
    """ウェブ検索を実行する"""
    return f"「{query}」の検索結果: ..."

@tool
def calculator(expression: str) -> str:
    """数式を計算する"""
    return str(eval(expression))

llm = get_llm(provider="openai", model="gpt-4o")

# ReActエージェント
react_agent = create_react_agent(
    llm=llm,
    tools=[search, calculator],
    system_prompt="あなたは万能アシスタントです。",
)
result = await react_agent.ainvoke({"input": "東京の人口は何人？"})

# ReWOOエージェント（計画→実行を分離、トークン効率が高い）
rewoo_agent = create_rewoo_agent(
    llm=llm,
    tools=[search],
    system_prompt="計画を立ててから実行してください。",
)
result = await rewoo_agent.ainvoke({"input": "AIの最新トレンドを調査して"})
```

### ルーターエージェント（条件分岐）
```python
from nvidia_nat_langchain.agents import create_router_agent

router = create_router_agent(
    llm=llm,
    routes={
        "research": react_agent,
        "calculation": calculator_agent,
        "general": general_agent,
    },
    system_prompt="ユーザーの質問内容に応じて適切な専門エージェントにルーティングしてください。",
)
result = await router.ainvoke({"input": "2+3は？"})
```

### オブザーバビリティパイプライン
```python
from nvidia_nat_core.observability import configure_telemetry

configure_telemetry(
    exporters=[
        {"type": "otlp", "endpoint": "http://jaeger:4317"},
        {"type": "langsmith", "project": "my-project"},
        {"type": "console"},  # デバッグ用
    ],
    trace_llm_calls=True,
    trace_tool_calls=True,
    trace_agent_steps=True,
)
# 以降のエージェント実行はすべて自動的にトレースされる
```

### ATIF軌跡フォーマット（評価・ファインチューニング）
```python
from nvidia_nat_atif import ATIFRecorder, ATIFConverter
from nvidia_nat_eval import evaluate_trajectory

# 軌跡の記録
recorder = ATIFRecorder()
with recorder.trace() as session:
    result = await react_agent.ainvoke({"input": "質問テキスト"})
trajectory = session.get_trajectory()

# ATIF形式で保存
trajectory.save("trajectory.atif.json")

# 軌跡ベースの評価
eval_result = await evaluate_trajectory(
    trajectory=trajectory,
    evaluators=["correctness", "tool_usage", "efficiency"],
    llm=llm,
)
print(eval_result.scores)

# ファインチューニングデータへの変換
converter = ATIFConverter()
training_data = converter.to_sft_dataset(
    trajectories=["trajectory.atif.json"],
    format="openai",  # OpenAI fine-tuning形式
)
training_data.save("training_data.jsonl")
```

### プロファイリング
```python
from nvidia_nat_profiler import Profiler, GPUSizingCalculator

# ワークフロー全体のプロファイリング
profiler = Profiler()
with profiler.profile() as session:
    result = await react_agent.ainvoke({"input": "テスト質問"})
report = session.get_report()

print(f"総トークン数: {report.total_tokens}")
print(f"総レイテンシ: {report.total_latency_ms}ms")
print(f"ボトルネック: {report.bottleneck_node}")

# GPU sizing計算
calculator = GPUSizingCalculator()
recommendation = calculator.estimate(
    model_name="llama-3.1-70b",
    expected_qps=100,
    max_latency_ms=500,
)
print(f"推奨GPU: {recommendation.gpu_type} x {recommendation.gpu_count}")
```

### MCPサーバー公開
```python
from nvidia_nat_mcp import MCPServer

server = MCPServer(
    name="research-agent-mcp",
    workflows={"research": research_workflow},
    tools={"search": search, "calculator": calculator},
)
await server.start(transport="stdio")

# FastMCP（高速MCP実装）
from nvidia_nat_fastmcp import FastMCPServer

fast_server = FastMCPServer(
    name="fast-research-mcp",
    workflows={"research": research_workflow},
)
await fast_server.start(host="0.0.0.0", port=8080)
```

### A2Aプロトコル（エージェント間通信）
```python
from nvidia_nat_a2a import A2AServer, A2AClient

# サーバー側: エージェントをA2Aで公開
a2a_server = A2AServer(
    agent=react_agent,
    name="research-agent",
    description="リサーチ専門エージェント",
)
await a2a_server.start(port=9000)

# クライアント側: リモートエージェントに依頼
client = A2AClient(url="http://research-agent:9000")
result = await client.send_task("AIの最新トレンドを調査して")
```

### セキュリティミドルウェア
```python
from nvidia_nat_security.middleware import (
    PIIGuard,
    ContentGuard,
    OutputVerifier,
)
from nvidia_nat_security.redteam import RedTeamEvaluator

# 防御ミドルウェアの適用
middleware_stack = [
    PIIGuard(actions=["mask"]),          # PII検出・マスク
    ContentGuard(categories=["hate", "violence"]),  # コンテンツフィルタ
    OutputVerifier(schema=output_schema),  # 出力スキーマ検証
]

# Red-teaming評価
evaluator = RedTeamEvaluator(
    attack_strategies=["prompt_injection", "jailbreak", "data_extraction"],
    num_attempts=100,
)
security_report = await evaluator.evaluate(agent=react_agent)
print(f"防御成功率: {security_report.defense_rate:.1%}")
```

### 設定オプティマイザ（遺伝的アルゴリズム）
```python
from nvidia_nat_config_optimizer import ConfigOptimizer

optimizer = ConfigOptimizer(
    base_config="workflow.yaml",
    objectives=["accuracy", "latency", "cost"],
    search_space={
        "llm.temperature": (0.0, 1.0),
        "llm.model": ["gpt-4o", "gpt-4o-mini", "llama-3.1-70b"],
        "agents.researcher.type": ["react", "rewoo", "tool_calling"],
    },
    eval_dataset="eval_dataset.jsonl",
    num_generations=20,
    population_size=50,
)
pareto_front = await optimizer.optimize()

# Pareto最適解の確認
for config in pareto_front:
    print(f"精度={config.accuracy:.2f}, レイテンシ={config.latency_ms}ms, コスト=${config.cost:.4f}")
    config.save(f"optimized_{config.id}.yaml")
```

### ミドルウェアパイプライン（カスタム実装）
```python
from nvidia_nat_core.middleware import Middleware, MiddlewareChain

class CustomRateLimiter(Middleware):
    def __init__(self, max_requests_per_minute: int):
        self.max_rpm = max_requests_per_minute
        self.counter = 0

    async def __call__(self, request, next_handler):
        if self.counter >= self.max_rpm:
            raise RateLimitError("レート制限超過")
        self.counter += 1
        response = await next_handler(request)
        return response

# ミドルウェアチェーン構築（順序が重要: 左から右に実行）
chain = MiddlewareChain([
    CacheMiddleware(ttl=3600),
    CustomRateLimiter(max_requests_per_minute=60),
    LoggingMiddleware(level="INFO"),
    TimeoutMiddleware(seconds=120),
])
```

## ワークフロー例

### ReActエージェント + 評価 + 最適化パイプライン
1. パッケージをインストールする
   ```bash
   pip install nvidia-nat-core nvidia-nat-langchain nvidia-nat-eval nvidia-nat-config-optimizer
   ```
2. YAML設定ファイルでReActエージェントを定義する（上記「YAML設定によるワークフロー定義」参照）
3. CLIでコンソール対話テストする
   ```bash
   nat run --config workflow.yaml --frontend console
   ```
4. ATIF軌跡を記録しながら評価データセットで実行する
   ```bash
   nat eval --config workflow.yaml --dataset eval_dataset.jsonl --output eval_results.json
   ```
5. 設定オプティマイザでパラメータを最適化する
   ```bash
   nat optimize --config workflow.yaml --dataset eval_dataset.jsonl --generations 20
   ```
6. 最適化されたYAML設定でFastAPIサーバーとして本番デプロイする
   ```bash
   nat serve --config optimized_best.yaml --host 0.0.0.0 --port 8000
   ```

### マルチエージェント・ルーターワークフロー
1. 専門エージェント（リサーチャー、分析者、コーダー）をYAML設定で定義する
2. ルーターエージェントを追加し、ユーザー入力に応じた条件分岐エッジを設定する
3. 投機的実行を有効化して全ブランチを並列スケジューリングし、スループットを向上させる
   ```yaml
   workflow:
     execution:
       speculative: true    # ルーター判定前にブランチを投機実行
       max_parallel: 3
   ```
4. オブザーバビリティをJaeger + LangSmithにエクスポートし、ルーティング精度を監視する
5. 不正確なルーティングがあれば、軌跡データからファインチューニングデータを生成し、ルーターLLMを改善する

### MCP + A2Aでのエージェント公開
1. ローカルで動作確認済みのワークフローをMCPサーバーとして公開する
   ```bash
   nat serve --config workflow.yaml --frontend mcp --port 8080
   ```
2. 別のNATインスタンスまたはClaudeDesktop等のMCPクライアントから接続する
3. 複数エージェントをA2Aプロトコルで相互接続し、エージェント間タスク委譲を実装する
4. セキュリティミドルウェア（PII Guard + Content Guard）を適用して外部公開に備える

### セキュリティ評価パイプライン
1. 本番エージェントに対してRed-teaming評価を実行する
   ```bash
   nat security redteam --config workflow.yaml --strategies prompt_injection,jailbreak --attempts 200
   ```
2. 脆弱性が見つかった場合、防御ミドルウェアをYAML設定に追加する
   ```yaml
   middleware:
     - type: pii_guard
       actions: [mask]
     - type: content_guard
       categories: [hate, violence, self_harm]
     - type: output_verifier
       schema: output_schema.json
   ```
3. 防御ミドルウェア適用後に再度Red-teaming評価を実行し、防御率を確認する

## 注意点

### パッケージ管理
- **必要なサブパッケージのみインストールすること**: `nvidia-nat-core[all]` は開発環境向け。本番では `nvidia-nat-core` + 使用するプラグインのみで依存関係を最小化する
- **サブパッケージ間のバージョン整合**: `nvidia-nat-core` と `nvidia-nat-langchain` 等はバージョンを揃える必要がある。不一致は `ImportError` や `RegistryError` の原因になる

### プラグインレジストリ
- **インポート順序が重要**: プラグインは `import` 時に自動登録される。プラグインパッケージを `import` する前にレジストリからコンポーネントを取得しようとすると `KeyError` になる
- **名前衝突**: 同じカテゴリ・名前で2回 `register()` すると後勝ちで上書きされる。カスタムコンポーネントにはプレフィックスを付けること（例: `custom.my_llm`）

### YAML設定コンパイル
- **`${variable}` 参照は同一YAML内のみ有効**: 外部ファイル参照や環境変数展開には別の構文（`$env{VAR_NAME}`等）が必要
- **トポロジーエラーはコンパイル時に検出される**: 循環参照や到達不能ノードがあるとコンパイル時にエラーになる。エッジ定義を確認すること
- **エッジのfrom/toはノードIDと完全一致必須**: タイポがあっても一部はサイレントに無視される場合があるのでログを確認する

### 投機的実行
- **無駄な計算コストが発生する**: ルーター分岐で全ブランチを投機実行するため、選択されなかったブランチのLLM呼び出し分はコストが無駄になる。コスト重視の場合は `speculative: false` に設定する
- **副作用のあるツールとの組み合わせに注意**: 投機実行でDB書き込みやAPI呼び出し等の副作用が複数ブランチで実行される可能性がある。冪等でないツールを含むワークフローでは無効化すること

### ATIF軌跡フォーマット
- **NVIDIA固有フォーマット**: 他社の評価ツール（RAGAS、DeepEval等）に直接渡せない。`ATIFConverter` で変換するか、カスタムアダプターを実装する必要がある
- **軌跡ファイルが大きくなりやすい**: 長い会話やツール呼び出しが多いワークフローでは1軌跡で数MBになることがある。`ATIFRecorder(max_steps=...)` で上限を設定する

### MCP / A2A
- **実験的機能**: MCP・A2Aサポートはまだ experimental マーク。本番環境では追加テストを行うこと
- **MCPのstdioトランスポートはプロセス間通信**: ネットワーク越しに公開する場合は `FastMCPServer` のHTTPトランスポートを使うこと

### ファインチューニング統合
- **外部サービスの認証情報が必要**: NeMo Customizer・OpenPipe ART連携にはそれぞれの認証情報を環境変数で設定する必要がある
- **Dynamo統合は別途デプロイが必要**: Dynamo推論スタックは独立したインフラとしてデプロイし、NAT側からエンドポイントURLで接続する

### ミドルウェア
- **実行順序は定義順**: YAML設定の `middleware` リストの上から順に実行される。キャッシュは最初に配置しないと効果がない
- **防御ミドルウェアのレイテンシ**: PII Guard・Content Guardは各リクエストにオーバーヘッドを追加する。レイテンシ要件が厳しい場合はサンプリング適用を検討する

## 関連スキル
- **langgraph**: LangGraph直接利用。NATのLangChain統合レイヤーを介さず、より細かいグラフ制御が必要な場合に
- **crewai**: 代替マルチエージェントフレームワーク。NATが重厚すぎる場合のロールベース設計向け軽量選択肢
- **lightrag**: RAGバックエンド。NATのリトリーバーインターフェースにLightRAGのナレッジグラフ検索を統合する場合に
- **mastra**: TypeScript製の代替エージェントフレームワーク。フロントエンド統合やエッジデプロイが主目的の場合に
- **servers**: MCPサーバー一覧。NATの `nvidia_nat_mcp` クライアントで接続する外部ツールサーバーを探す際に参照
```
