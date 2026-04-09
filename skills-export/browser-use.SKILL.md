```markdown
---
name: browser-use
description: LLMエージェントにWebブラウザを自律操作させたい、またはフォーム入力・データ抽出・多段階ナビゲーション・動的ページのスクレイピングなどのWebタスクを自然言語で自動化したい場合に必ずこのスキルを使え。Playwright/CDPベースのブラウザ制御とLLM推論ループを統合するPythonフレームワークである。
---

# browser-use

## 概要
browser-useはLLMがWebブラウザをCDP（Chrome DevTools Protocol）経由で自律制御するPythonフレームワークである。OpenAI・Anthropic・Geminiなど15以上のLLMプロバイダーと統合し、DOMスナップショット取得→LLM推論→アクション実行のループでWebタスクを遂行する。フォーム入力、データ抽出、マルチサイトナビゲーション、動的コンテンツのスクレイピングを自然言語の指示だけで実現できる。

## いつ使うか
- 「〜のWebサイトで〇〇を検索して結果を取得して」という指示が来たとき
- フォーム入力・ログイン・ボタンクリックなどの反復的なWebタスクを自動化したいとき
- 動的JavaScriptコンテンツを含むページからデータをスクレイピングしたいとき
- 自然言語の指示でQAテストやE2Eテストを実行したいとき
- 複数サイトをまたぐ多段階のエージェントワークフローを構築したいとき
- 価格監視・求人応募・フォーム一括送信などの反復業務を自動化したいとき
- ブラウザを操作するAIアシスタントやCopilotを実装したいとき

## 主要コマンド・API

### インストール
```bash
pip install browser-use
playwright install chromium
```

### 環境変数の設定
```bash
# 使用するLLMプロバイダーに応じて設定
export OPENAI_API_KEY=sk-...
export ANTHROPIC_API_KEY=sk-ant-...
export GOOGLE_API_KEY=...
```

### 最小構成での実行
```python
import asyncio
from browser_use import Agent
from langchain_openai import ChatOpenAI

async def main():
    agent = Agent(
        task="Go to hacker news and summarize the top 3 stories",
        llm=ChatOpenAI(model="gpt-4o"),
    )
    result = await agent.run()
    print(result)

asyncio.run(main())
```

### Anthropic / Gemini での実行
```python
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI

# Anthropic（pip install langchain-anthropic）
agent = Agent(task="...", llm=ChatAnthropic(model="claude-sonnet-4-20250514"))

# Gemini（pip install langchain-google-genai）
agent = Agent(task="...", llm=ChatGoogleGenerativeAI(model="gemini-2.0-flash"))
```

### BrowserSession のカスタマイズ
```python
from browser_use import Agent, BrowserSession

session = BrowserSession(
    headless=False,                      # ブラウザUIを表示
    user_data_dir="~/.chrome-profile",   # 既存プロファイル（ログイン状態保持等）
    viewport={"width": 1280, "height": 800},
)

agent = Agent(
    task="Fill out the contact form at example.com/contact",
    llm=llm,
    browser_session=session,
)
await agent.run(max_steps=15)
await session.close()  # 必ず明示的にクローズ
```

### 機密データのマスキング
```python
from browser_use import Agent
from browser_use.agent.views import SensitiveData

agent = Agent(
    task="Login to example.com with my credentials and download the report",
    llm=llm,
    sensitive_data=SensitiveData(
        username="myuser@example.com",
        password="s3cr3tpassword",
    ),
)
# LLMには <username>, <password> プレースホルダーが渡され
# ブラウザ操作時に実値に復元される → LLMに生の認証情報が送信されない
```

### カスタムアクションの登録
```python
from browser_use.controller.service import Controller

controller = Controller()

@controller.action("Save extracted data to a CSV file")
async def save_to_csv(data: str, filename: str):
    with open(filename, "w") as f:
        f.write(data)
    return f"Saved {len(data)} chars to {filename}"

agent = Agent(task="...", llm=llm, controller=controller)
```

### 実行ステップ数の制限
```python
# タスクの複雑さに応じて設定（未指定だとデフォルト上限まで実行）
result = await agent.run(max_steps=20)
```

## ワークフロー例

### Webサイトからのデータ抽出
```python
import asyncio
from browser_use import Agent, BrowserSession
from langchain_openai import ChatOpenAI

async def scrape_prices():
    session = BrowserSession(headless=True)
    agent = Agent(
        task=(
            "Go to example-shop.com, search for 'wireless mouse', "
            "extract the top 5 results with name and price, "
            "and return them as a JSON array."
        ),
        llm=ChatOpenAI(model="gpt-4o"),
        browser_session=session,
    )
    result = await agent.run(max_steps=15)
    await session.close()
    return result

data = asyncio.run(scrape_prices())
print(data)
```

### ログイン→操作→ログアウトの一連フロー
```python
from browser_use.agent.views import SensitiveData

agent = Agent(
    task=(
        "Login to dashboard.example.com, "
        "go to Settings > Billing, "
        "download the latest invoice as PDF, "
        "then logout."
    ),
    llm=llm,
    sensitive_data=SensitiveData(
        email="admin@example.com",
        password="hunter2",
    ),
    browser_session=BrowserSession(
        headless=False,
        user_data_dir="/tmp/dash-profile",
    ),
)
result = await agent.run(max_steps=25)
```

### カスタムアクション付きパイプライン
```python
from browser_use.controller.service import Controller
import json

controller = Controller()

@controller.action("Append result to local JSON file")
async def append_result(item: str, filepath: str):
    try:
        with open(filepath) as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []
    data.append(json.loads(item))
    with open(filepath, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return f"Appended to {filepath}, total {len(data)} items"

agent = Agent(
    task="Search for Python developer jobs on example-jobs.com and save each result",
    llm=llm,
    controller=controller,
)
await agent.run(max_steps=30)
```

## 注意点
- **非同期必須**: すべてのAPIが `async/await` ベース。スクリプトでは `asyncio.run(main())` で実行。Jupyter Notebookでは `await` を直接使用可能
- **Playwrightインストール忘れ**: `pip install browser-use` の後に `playwright install chromium` が必須。これを忘れるとランタイムエラーになる
- **max_steps を必ず設定**: 未指定だとタスクが終わらない場合にステップを消費し続ける。単純タスクは10-15、複雑なフローは25-30が目安
- **機密データは必ず SensitiveData 経由**: タスク文字列にパスワードを直接書くとLLMに送信される。`SensitiveData` を使えばプレースホルダーに置換される
- **headlessモードのブロック**: 一部サイトはheadlessブラウザを検知してブロックする。`headless=False` にするか、`user_data_dir` で既存プロファイルを使うことで回避
- **LLM APIコスト**: 1ステップごとにLLM呼び出しが発生する。20ステップのタスクは20回のAPI呼び出し。GPT-4oで1タスク$0.1〜$1程度を見込むこと
- **DOMスナップショットのサイズ**: 複雑なページではDOMが巨大になりLLMのコンテキストを圧迫する。MessageManagerが自動圧縮するが、重要な指示はタスク文字列に明記しておくこと
- **長時間セッションの不安定性**: CDP接続は長時間で切断されることがある。タスクを分割して短いセッションにすることを推奨
- **Watchdogの誤検知**: CAPTCHA検知などのWatchdogが誤反応する場合がある。問題が起きたらWatchdog設定を確認して切り分けること

## 関連スキル
- **playwright**: browser-useの基盤。エージェント不要の決定的ブラウザ操作にはPlaywrightを直接使う方が適切
- **langchain**: LLMクライアントの提供元。`BaseChatModel` 互換であればどのプロバイダーも使用可能
- **crewai / langgraph**: 複数のbrowser-useエージェントをオーケストレーションする場合のマルチエージェントフレームワーク
```
