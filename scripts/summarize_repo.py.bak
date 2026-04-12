#!/usr/bin/env python3
"""Repomix出力 → OpenRouter LLM → 構造化要約生成"""
import argparse
import json
import os
import re
import sys
import requests

OPENROUTER_API = "https://openrouter.ai/api/v1/chat/completions"

def get_api_key():
    key = os.environ.get("OPENROUTER_API_KEY", "")
    if not key:
        envfile = os.path.join(os.path.dirname(__file__), "..", ".env")
        if os.path.exists(envfile):
            for line in open(envfile):
                if line.startswith("LLM_BINDING_API_KEY="):
                    key = line.split("=", 1)[1].strip().strip('"')
    if not key:
        print("ERROR: OpenRouter APIキーが見つかりません", file=sys.stderr)
        sys.exit(1)
    return key

CLASSIFY_PROMPT = """あなたは技術ナレッジの分類エキスパートです。
以下のリポジトリ情報を分析し、JSON形式で出力してください。JSONのみを出力し、他のテキストは含めないでください。

## カテゴリ（以下から最も適切な1つを選択）
framework, pattern, tool, protocol, infra, crypto, website, webapp, agent, workflow

## サブカテゴリ（該当するものを0〜3個選択）
上記カテゴリリストから選択

## タグ（3〜8個を自由に生成）
- 言語タグ（必須）
- 技術・ライブラリ名
- 実装パターン名
- ドメイン名

禁止: 汎用的すぎるタグ(code, development, programming)、3単語以上のタグ、カテゴリ名と同一のタグ

## 出力JSON
{
  "category": "...",
  "sub_categories": ["..."],
  "tags": ["..."],
  "summary": "1-3文でリポジトリの目的を説明",
  "design_philosophy": "アーキテクチャや設計哲学",
  "key_components": [{"name": "...", "role": "..."}],
  "implementation_patterns": [{"name": "...", "description": "..."}],
  "use_cases": "どういうプロジェクトに役立つか",
  "caveats": "制限・注意点",
  "code_examples": [{"title": "例のタイトル", "code": "コードスニペット", "explanation": "説明"}],
  "error_handling": [{"scenario": "エラーシナリオ", "code": "対処コード", "explanation": "説明"}],
  "best_practices": ["ベストプラクティス1", "ベストプラクティス2"],
  "gotchas": ["注意点・ハマりポイント1", "注意点2"]
}

## code_examples について
リポジトリの主要な使い方を示すコードサンプルを最低5件生成してください。
- 基本的な初期化・セットアップ
- メインのユースケース（2-3件）
- 高度なユースケース
- エラーハンドリング例
コードはそのまま実行可能な形式で、引数・戻り値・型を明記してください。

## error_handling について
よくあるエラーシナリオと対処法を最低2件生成してください。
- 例外クラスの階層（あれば）
- リトライ戦略
- フォールバック処理

## best_practices について
本番環境で使う際のベストプラクティスを5件以上挙げてください。

## gotchas について
初心者がハマりやすいポイントを3件以上挙げてください。

---
リポジトリ情報:
"""

def call_llm(api_key: str, prompt: str, model: str = "anthropic/claude-sonnet-4.6") -> str:
    r = requests.post(
        OPENROUTER_API,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"model": model, "max_tokens": 4096, "messages": [{"role": "user", "content": prompt}]},
        timeout=120,
    )
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]

def extract_json(text: str) -> dict:
    """JSONを抽出。失敗時はNoneを返す"""
    try:
        m = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
        if m:
            return json.loads(m.group(1))
        return json.loads(text)
    except (json.JSONDecodeError, AttributeError):
        return None

def build_lightrag_text(repo_url: str, meta: dict) -> str:
    """DATA-SCHEMAテンプレートに沿ったLightRAG投入テキスト"""
    components = "\n".join(f"- {c['name']}: {c['role']}" for c in meta.get("key_components", []))
    patterns = "\n".join(f"- {p['name']}: {p['description']}" for p in meta.get("implementation_patterns", []))
    tags = ", ".join(meta.get("tags", []))
    sub_cats = ", ".join(meta.get("sub_categories", []))
    from datetime import date
    
    return f"""# {repo_url.rstrip('/').split('/')[-1]}

## 基本情報
- リポジトリ: {repo_url}
- カテゴリ: {meta.get('category', '')}
- サブカテゴリ: {sub_cats}
- タグ: {tags}
- 最終確認日: {date.today().isoformat()}

## 概要
{meta.get('summary', '')}

## 設計思想
{meta.get('design_philosophy', '')}

## 主要コンポーネント
{components}

## 実装パターン
{patterns}

## 適用シーン
{meta.get('use_cases', '')}

## 注意点・制約
{meta.get('caveats', '')}

## コード例
{chr(10).join(f"### {ex.get('title','例')}{chr(10)}{chr(10)}    {ex.get('code','').replace(chr(10), chr(10) + '    ')}{chr(10)}{chr(10)}{ex.get('explanation','')}" for ex in meta.get('code_examples', []))}

## エラーハンドリング
{chr(10).join(f"### {ex.get('scenario','')}{chr(10)}{chr(10)}    {ex.get('code','').replace(chr(10), chr(10) + '    ')}{chr(10)}{chr(10)}{ex.get('explanation','')}" for ex in meta.get('error_handling', []))}

## ベストプラクティス
{chr(10).join(f"- {bp}" for bp in meta.get('best_practices', []))}

## 注意点・ハマりポイント
{chr(10).join(f"- {g}" for g in meta.get('gotchas', []))}
"""

def main():
    p = argparse.ArgumentParser()
    p.add_argument("repomix_file", help="Repomix出力ファイル")
    p.add_argument("--repo-url", required=True, help="GitHubリポジトリURL")
    p.add_argument("--model", default="anthropic/claude-sonnet-4.6")
    p.add_argument("--output-dir", default="/tmp")
    p.add_argument("--graph-report", default="", help="graphify GRAPH_REPORT.mdのパス")
    args = p.parse_args()

    # Repomix出力を読み込み（大きすぎる場合は先頭を切り詰め）
    text = open(args.repomix_file).read()
    max_chars = 80000  # ~20kトークン目安
    if len(text) > max_chars:
        print(f"WARN: 入力を{max_chars}文字に切り詰め ({len(text)} → {max_chars})", file=sys.stderr)
        text = text[:max_chars]

    api_key = get_api_key()
    
    print("LLMで構造化要約を生成中...", file=sys.stderr)
    graph_context = ""
    if args.graph_report and os.path.exists(args.graph_report):
        graph_text = open(args.graph_report).read()[:8000]
        graph_context = f"\n\n## コード構造解析（graphify）\n{graph_text}\n"
        print("graphify GRAPH_REPORT.mdを追加コンテキストとして使用", file=sys.stderr)
    prompt = CLASSIFY_PROMPT + graph_context + text
    meta = None
    for attempt in range(3):
        try:
            raw = call_llm(api_key, prompt, args.model)
            meta = extract_json(raw)
            if meta:
                break
            print(f"WARN: JSON解析失敗 (attempt {attempt+1}/3), リトライ...", file=sys.stderr)
        except Exception as e:
            print(f"WARN: LLM呼び出し失敗 (attempt {attempt+1}/3): {e}", file=sys.stderr)
    
    if not meta:
        print("WARN: LLM要約失敗。READMEベースのフォールバック生成", file=sys.stderr)
        repo_name = args.repo_url.rstrip("/").split("/")[-1].lower()
        meta = {
            "category": "tool",
            "sub_categories": [],
            "tags": [],
            "summary": text[:200].replace("\n", " "),
            "design_philosophy": "",
            "key_components": [],
            "implementation_patterns": [],
            "use_cases": "",
            "caveats": "自動要約に失敗したため簡易版。手動でレベルアップ推奨。",
        }

    # リポジトリ名
    repo_name = args.repo_url.rstrip("/").split("/")[-1].lower()
    meta["name"] = repo_name
    meta["source"] = args.repo_url

    # LightRAG投入テキスト生成
    lightrag_text = build_lightrag_text(args.repo_url, meta)
    lightrag_path = os.path.join(args.output_dir, f"{repo_name}_lightrag.txt")
    with open(lightrag_path, "w") as f:
        f.write(lightrag_text)

    # Obsidian用メタデータJSON
    meta["body"] = lightrag_text
    meta["title"] = repo_name
    meta_path = os.path.join(args.output_dir, f"{repo_name}_meta.json")
    with open(meta_path, "w") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    print(f"LightRAGテキスト: {lightrag_path}", file=sys.stderr)
    print(f"メタデータJSON: {meta_path}", file=sys.stderr)
    
    # パス情報をstdoutに出力（シェルスクリプトで拾う）
    print(json.dumps({"lightrag_text": lightrag_path, "meta_json": meta_path}))

if __name__ == "__main__":
    main()
