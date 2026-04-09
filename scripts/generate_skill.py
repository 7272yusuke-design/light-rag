#!/usr/bin/env python3
"""メタデータJSONからSKILL.mdを自動生成する"""

import json
import sys
import os
import urllib.request
import urllib.parse

OPENROUTER_KEY = os.environ.get("LLM_BINDING_API_KEY", "")
OPENROUTER_MODEL = os.environ.get("LLM_MODEL", "anthropic/claude-sonnet-4.6")

def load_env():
    """Load .env file if OPENROUTER key not in environment"""
    global OPENROUTER_KEY
    if OPENROUTER_KEY:
        return
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ[k.strip()] = v.strip()
        OPENROUTER_KEY = os.environ.get("LLM_BINDING_API_KEY", "")

def call_llm(prompt: str) -> str:
    load_env()
    payload = json.dumps({
        "model": OPENROUTER_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 4000,
        "temperature": 0.3
    }).encode()
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=payload,
        headers={
            "Authorization": f"Bearer {OPENROUTER_KEY}",
            "Content-Type": "application/json"
        },
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        result = json.loads(resp.read())
    return result["choices"][0]["message"]["content"]

def generate_skill_md(meta: dict) -> str:
    repo_name = meta.get("repo_name", meta.get("name", "unknown"))
    summary = meta.get("summary", "")
    components = meta.get("key_components", [])
    patterns = meta.get("implementation_patterns", [])
    tags = meta.get("tags", [])
    category = meta.get("category", "tool")
    use_cases = meta.get("use_cases", "")
    constraints = meta.get("constraints", "")

    components_text = "\n".join(f"- {c.get('name','?')}: {c.get('role', c.get('description',''))}" for c in components)
    patterns_text = "\n".join(f"- {p.get('name','?')}: {p.get('description', p.get('role',''))}" for p in patterns)

    prompt = f"""以下のリポジトリ情報から、Claude Code Agent Skill (SKILL.md) を生成してください。

リポジトリ: {repo_name}
カテゴリ: {category}
タグ: {', '.join(tags)}

概要:
{summary}

主要コンポーネント:
{components_text}

実装パターン:
{patterns_text}

適用シーン:
{use_cases}

注意点・制約:
{constraints}

以下のフォーマットで出力してください。YAMLフロントマター + Markdown本体のみ。説明や前置きは不要。

---
name: {repo_name}
description: [1-2文でこのスキルがいつトリガーされるべきかを記述。やや押しが強めに。]
---

# {repo_name}

## 概要
[このツール/フレームワークが何をするか、2-3文]

## いつ使うか
[箇条書きで、どういう指示や状況でこのスキルを使うべきか]

## 主要コマンド・API
[実際に使うコマンドやAPI呼び出しの例。コードブロックで]

## ワークフロー例
[典型的な使用手順を番号付きで]

## 注意点
[ハマりポイント、制約、非推奨事項]

## 関連スキル
[組み合わせて使える他のツールやスキル]
"""

    return call_llm(prompt)

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("meta_json", help="メタデータJSONファイルパス")
    parser.add_argument("-o", "--output-dir", default=".", help="SKILL.md出力先ディレクトリ")
    args = parser.parse_args()

    with open(args.meta_json) as f:
        meta = json.load(f)

    repo_name = meta.get("repo_name", meta.get("name", "unknown"))
    print(f"SKILL.md生成中: {repo_name}...")

    skill_md = generate_skill_md(meta)

    # Clean up LLM output (remove markdown fences if present)
    if skill_md.startswith("```"):
        lines = skill_md.split("\n")
        skill_md = "\n".join(lines[1:-1] if lines[-1].strip() == "```" else lines[1:])

    os.makedirs(args.output_dir, exist_ok=True)
    output_path = os.path.join(args.output_dir, f"{repo_name}.SKILL.md")
    with open(output_path, "w") as f:
        f.write(skill_md)

    print(f"OK: {output_path}")
    return output_path

if __name__ == "__main__":
    main()
