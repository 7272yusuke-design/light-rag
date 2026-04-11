#!/usr/bin/env python3
"""KNOWLEDGE-INDEX.md を LightRAG API から自動生成"""
import json, urllib.request, urllib.parse, re

BASE = "http://localhost:9621"

# ログイン
data = urllib.parse.urlencode({"username": "admin", "password": "LightRag@2026!"}).encode()
token = json.loads(urllib.request.urlopen(f"{BASE}/login", data).read())["access_token"]

# ドキュメント一覧取得
req = urllib.request.Request(f"{BASE}/documents", headers={"Authorization": f"Bearer {token}"})
raw = json.loads(urllib.request.urlopen(req).read())
doc_list = raw.get("statuses", {}).get("processed", [])

def parse_content(text):
    """content_summaryからメタ情報を抽出"""
    info = {"name": "", "source": "", "category": "other", "tags": "—", "summary": ""}
    # タイトル行（# で始まる最初の行）
    m = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    if m:
        info["name"] = m.group(1).strip()
    # リポジトリ or ソース
    m = re.search(r"リポジトリ:\s*(https?://github\.com/\S+)", text)
    if m:
        info["source"] = m.group(1).replace("https://github.com/", "")
    m = re.search(r"ソース:\s*(.+)$", text, re.MULTILINE)
    if m and not info["source"]:
        info["source"] = m.group(1).strip()
    # カテゴリ
    m = re.search(r"カテゴリ:\s*(\S+)", text)
    if m:
        info["category"] = m.group(1).strip()
    # タグ
    m = re.search(r"タグ:\s*(.+)$", text, re.MULTILINE)
    if m:
        info["tags"] = m.group(1).strip()
    # 概要（## 概要の次の行）
    m = re.search(r"## 概要\n(.+)", text)
    if m:
        info["summary"] = m.group(1).strip()[:60]
    return info

from collections import defaultdict
categories = defaultdict(list)

for doc in doc_list:
    text = doc.get("content_summary", "")
    fp = doc.get("file_path", "")
    info = parse_content(text)
    if not info["name"]:
        info["name"] = fp.replace("_lightrag.txt", "").replace(".txt", "").replace(".md", "")
    categories[info["category"]].append(info)

count = len(doc_list)

cat_labels = {
    "framework": "フレームワーク・ライブラリ",
    "agent": "エージェント・自動化",
    "tool": "ツール・ユーティリティ",
    "website": "Webサイト・UI",
    "infra": "インフラ・DevOps",
    "workflow": "ワークフロー・パターン",
    "pattern": "パターン集",
    "protocol": "プロトコル",
    "crypto": "仮想通貨・DeFi",
    "other": "その他",
}
cat_order = ["framework", "agent", "tool", "website", "infra", "workflow", "pattern", "protocol", "crypto", "other"]

lines = [
    f"# ナレッジインデックス（LightRAG 蓄積済み 全{count}件）",
    "",
    "> 自動生成ファイル。`python3 scripts/update_knowledge_index.py` で更新。",
    "",
    "## 実装レベル定義",
    "",
    "| レベル | 内容 |",
    "|--------|------|",
    "| 0 | 概要・設計思想のみ |",
    "| 1 | コードサンプルあり（最低3件） |",
    "| 2 | 引数・戻り値・例外が明記 |",
    "| 3 | エラーハンドリング・テスト例・ベストプラクティスあり |",
    "",
    "---",
]

for cat in cat_order:
    if cat not in categories:
        continue
    items = categories[cat]
    label = cat_labels.get(cat, cat)
    lines += ["", f"## {label} ({len(items)}件)", "", "| 名前 | ソース | レベル | タグ | 概要 |", "|------|--------|--------|------|------|"]
    for item in sorted(items, key=lambda x: x["name"].lower()):
        lines.append(f"| {item['name']} | {item['source']} | 0 | {item['tags']} | {item['summary']} |")

output = "\n".join(lines) + "\n"
outpath = "/docker/lightrag/docs/KNOWLEDGE-INDEX.md"
with open(outpath, "w") as f:
    f.write(output)
print(f"Updated {outpath} ({count} docs)")
