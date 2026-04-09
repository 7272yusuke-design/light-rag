Now I have a clear picture. Let me produce the improved SKILL.md.

---

```markdown
---
name: langgraph
description: LangGraphを使ったステートフルなマルチエージェントAIアプリケーション・グラフベースワークフローを構築する際に必ずこのスキルを使え。`StateGraph`・`@entrypoint`・`@task`・`ToolNode`・`add_messages`・`interrupt`・`Command`・`RemoteGraph`・`MemorySaver`・`PostgresSaver`などLangGraph固有のAPIが関わる場面では即座にこのスキルを参照せよ。
---

# langgraph

## 概要
LangGraphはグラフベースの実行モデル（Pregelエンジン）を用いてステートフルなマルチエージェントAIアプリケーションを構築するPythonフレームワークである。宣言的な`StateGraph` APIとデコレータベースのFunctional API（`@entrypoint`/`@task`）の2スタイルを提供し、どちらも同一のPregelランタイムにコンパイルされる。チェックポイント永続化、ヒューマン・イン・ザ・ループ、リモートグラフ合成、CLIによるDockerデプロイを標準サポートする。

## いつ使うか
- `StateGraph`・`add_node`・`add_edge`・`add_conditional_edges`でグラフを構築するとき
- `@entrypoint`・`@task`デコレータでFunctional APIワークフローを書くとき
- `MemorySaver`・`PostgresSaver`・`SqliteSaver`でチェックポイントを永続化するとき
- `interrupt()`・`Command(resume=...)`でヒューマン・イン・ザ・ループを実装するとき
- `ToolNode`・`InjectedState`でLLMツール呼び出しを構築するとき
- 複数エージェント協調（スーパーバイザー、階層チーム、並列エージェント）を設計するとき
- `langgraph dev`・`langgraph build`・`langgraph up`でデプロイするとき
- `RemoteGraph`で分散グラフを合成するとき

## 主要コマンド・API

### インストール
```bash
pip install langgraph

# チェックポインタ（必要に応じて）
pip install langgraph-checkpoint-postgres
pip install langgraph-checkpoint-sqlite

# CLI（デプロイ用）
pip install langgraph-cli

# クライアントSDK
pip install langgraph-sdk
```

### StateGraph API（宣言的スタイル）
```python
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI

class State(TypedDict):
    messages: Annotated[list, add_messages]

llm = ChatOpenAI(model="gpt-4o")

def chatbot(state: State) -> dict:
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

builder = StateGraph(State)
builder.add_node("chatbot", chatbot)
builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)

graph = builder.compile(checkpointer=MemorySaver())

# 実行（thread_id でセッション管理）
config = {"configurable": {"thread_id": "session-1"}}
result = graph.invoke(
    {"messages": [{"role": "user", "content": "こんにちは"}]},
    config=config,
)
print(result["messages"][-1].content)
```

### 条件付きエッジ（ツールループ）
```python
from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool

@tool
def search(query: str) -> str:
    """ウェブ検索を実行する"""
    return f"「{query}」の検索結果: ..."

tools = [search]
llm_with_tools = ChatOpenAI(model="gpt-4o").bind_tools(tools)

def agent(state: State) -> dict:
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

def should_continue(state: State) -> str:
    last = state["messages"][-1]
    return "tools" if last.tool_calls else END

builder = StateGraph(State)
builder.add_node("agent", agent)
builder.add_node("tools", ToolNode(tools=tools))
builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", should_continue)
builder.add_edge("tools", "agent")

graph = builder.compile(checkpointer=MemorySaver())
```

### Functional API（デコレータスタイル）
```python
from langgraph.func import entrypoint, task
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import RetryPolicy

@task(retry=RetryPolicy(max_attempts=3))
async def fetch_data(query: str) -> str:
    return await some_api_call(query)

@entrypoint(checkpointer=MemorySaver())
async def my_workflow(query: str) -> dict:
    data = await fetch_data(query)
    return {"result": data}

config = {"configurable": {"thread_id": "session-1"}}
result = await my_workflow.ainvoke("LangGraphとは", config=config)
```

### ToolNode と InjectedState
```python
from langgraph.prebuilt import ToolNode, InjectedState
from langchain_core.tools import tool
from typing import Annotated

@tool
def get_context(
    query: str,
    state: Annotated[dict, InjectedState],  # LLMスキーマから隠蔽される
) -> str:
    """コンテキストを取得する"""
    msg_count = len(state.get("messages", []))
    return f"query={query}, history={msg_count}件"

tool_node = ToolNode(tools=[get_context])
builder.add_node("tools", tool_node)
```

### チェックポインタ（PostgreSQL）
```python
from langgraph.checkpoint.postgres import PostgresSaver

with PostgresSaver.from_conn_string(
    "postgresql://user:pass@localhost:5432/langgraph"
) as checkpointer:
    checkpointer.setup()  # 初回のみ：テーブル作成
    graph = builder.compile(checkpointer=checkpointer)
    result = graph.invoke(input_data, config=config)
```

### ヒューマン・イン・ザ・ループ（interrupt）
```python
from langgraph.types import interrupt, Command

def human_review(state: State) -> dict:
    decision = interrupt({
        "question": "この内容を承認しますか？",
        "draft": state["messages"][-1].content,
    })
    return {"approved": decision == "yes"}

builder.add_node("review", human_review)

# --- 実行側 ---
config = {"configurable": {"thread_id": "review-1"}}
# 1. interrupt で一時停止
result = graph.invoke(input_data, config=config)
# 2. ユーザー判断後に再開
result = graph.invoke(Command(resume="yes"), config=config)
```

### ストリーミング
```python
# イベントストリーム（トークン単位）
async for event in graph.astream_events(input_data, config=config, version="v2"):
    if event["event"] == "on_chat_model_stream":
        print(event["data"]["chunk"].content, end="", flush=True)

# 状態スナップショットのストリーム
for chunk in graph.stream(input_data, config=config, stream_mode="values"):
    print(chunk["messages"][-1].content)
```

### RemoteGraph（リモートグラフ合成）
```python
from langgraph.pregel.remote import RemoteGraph

remote = RemoteGraph(
    "research-agent",
    url="http://langgraph-server:8123",
    api_key="lgs_...",
)
builder.add_node("researcher", remote)
```

### CLI（デプロイメント）
```bash
# 開発サーバー起動（ホットリロード付き）
langgraph dev

# Docker イメージビルド
langgraph build -t my-agent:latest

# Docker Compose で本番起動
langgraph up

# 新規プロジェクトのスキャフォールド
langgraph new my-project
```

### SDK（クライアントからのリモート実行）
```python
from langgraph_sdk import get_client

client = get_client(url="http://localhost:8123")

thread = await client.threads.create()
async for chunk in client.runs.stream(
    thread["thread_id"],
    "my-agent",
    input={"messages": [{"role": "user", "content": "調査して"}]},
    stream_mode="events",
):
    print(chunk)
```

## ワークフロー例

### ReActエージェント（ツール呼び出しループ）の構築
1. ツールを定義する
   ```python
   @tool
   def calculator(expression: str) -> str:
       """数式を計算する"""
       return str(eval(expression))
   ```
2. LLMにツールをバインドし、`StateGraph`でagent→tools→agentのループを構築する（上記「条件付きエッジ」パターン参照）
3. `MemorySaver`付きでコンパイルし、`thread_id`を指定して実行する
4. 会話を継続する場合は同じ`thread_id`で`invoke`を繰り返す

### スーパーバイザー型マルチエージェント
1. 各専門エージェント（リサーチャー、ライター等）をサブグラフとして定義する
2. スーパーバイザーノードで「次にどのエージェントに振るか」を条件付きエッジで制御する
   ```python
   def supervisor(state: State) -> str:
       # LLMにルーティング判断させる
       response = llm.invoke(state["messages"])
       return response.tool_calls[0]["args"]["next"]

   builder.add_conditional_edges("supervisor", supervisor, {
       "researcher": "researcher",
       "writer": "writer",
       "FINISH": END,
   })
   ```
3. 各サブエージェントの出力をスーパーバイザーに戻すエッジを追加する

### ヒューマン承認付きワークフロー
1. 処理ノード → `interrupt()`承認ノード → 実行ノードの順でグラフを構築する
2. `interrupt()`で承認データ（差分、要約等）をユーザーに提示する
3. ユーザーが`Command(resume="approved")`で再開、または`Command(resume="rejected")`で別分岐に進む

### 本番デプロイ
1. `langgraph.json`を作成する
   ```json
   {
     "dependencies": ["."],
     "graphs": {
       "my_agent": "./agent.py:graph"
     }
   }
   ```
2. `langgraph dev`でローカル検証する
3. `langgraph build -t my-agent:latest`でDockerイメージをビルドする
4. `langgraph up`で起動し、SDKクライアントから接続する

## 注意点

### 状態設計（最頻出のバグ原因）
- **`Annotated[list, add_messages]`を使わずにメッセージリストを定義すると、ノードの出力で全メッセージが上書きされる**。メッセージ蓄積には必ず`add_messages`リデューサーを指定すること
- 並列ノードが同じチャンネルに書き込む場合、リデューサーが未定義だと後勝ちで上書きされる。`operator.add`等のリデューサーを明示的に設定すること
- 状態にファイルハンドル・DB接続等の非シリアライズ可能オブジェクトを含めるとチェックポイント保存が失敗する

### チェックポイント
- **`thread_id`を`config`に渡さないと状態が永続化されない**（毎回新規セッション扱い）
- `PostgresSaver`は初回に`checkpointer.setup()`を呼ばないとテーブル不在エラーになる
- `MemorySaver`はインメモリのためプロセス終了で消える。本番では`PostgresSaver`か`SqliteSaver`を使うこと

### ヒューマン・イン・ザ・ループ
- `interrupt()`で停止後の再開は、同じ`thread_id`で`Command(resume=value)`を渡す。`thread_id`が違うと新規実行になる
- `interrupt()`はノード関数内でのみ有効。エッジ関数やグラフ外で呼ぶとエラーになる

### ToolNode
- `ToolNode`はLLMが生成した`tool_calls`を自動ディスパッチする。未登録ツール名が`tool_calls`に含まれるとエラーになる
- `InjectedState`で注入されるパラメータはLLMのスキーマから自動的に隠蔽される。LLMが指定する必要はない

### Functional API
- `@task`は`@entrypoint`の内部から呼ばないとただの関数として動作し、チェックポイント・リトライが効かない
- `RetryPolicy`・`CachePolicy`は`@task`デコレータに指定する。`@entrypoint`には指定できない

### CLI・デプロイ
- `langgraph up`はDockerが必要。Docker Desktopが起動していることを確認すること
- `langgraph.json`の`graphs`キーの値は`"./module.py:variable_name"`形式。コンパイル済みグラフ変数を指す必要がある

## 関連スキル
- **crewai**: 代替マルチエージェントフレームワーク。ロールベース設計が得意で、LangGraphはグラフベース設計が得意
- **ai**: Vercel AI SDK。TypeScript/フロントエンド統合が主目的の場合はこちら
- **lightrag**: RAGバックエンド。LangGraphのノード内でナレッジ検索を統合する場合に使用
- **supabase**: PostgreSQLバックエンド。`PostgresSaver`のホスティング先やベクトル検索との統合に
- **browser-use**: ブラウザ操作ツール。LangGraphエージェントのツールとしてブラウザ自動化を組み込む場合に使用
```
