#!/usr/bin/env python3
"""重複・類似ナレッジ検知"""
import os, re, json

def extract_meta(filepath):
    text = open(filepath).read()
    meta = {}
    fm = re.search(r'^---\n(.*?)\n---', text, re.DOTALL)
    if not fm:
        return meta
    for line in fm.group(1).split("\n"):
        if ": " in line:
            k, v = line.split(": ", 1)
            meta[k.strip()] = v.strip()
    return meta

def main():
    vault = "obsidian-export"
    docs = []
    for root, dirs, files in os.walk(vault):
        for f in files:
            if f.endswith(".md") and not f.startswith("_"):
                path = os.path.join(root, f)
                meta = extract_meta(path)
                meta["_path"] = path
                meta["_name"] = f.replace(".md", "")
                docs.append(meta)

    # タグ重複分析
    print("=== タグ使用頻度 ===")
    tag_count = {}
    for d in docs:
        tags_str = d.get("tags", "[]").strip("[]")
        for t in tags_str.split(","):
            t = t.strip()
            if t:
                tag_count[t] = tag_count.get(t, 0) + 1
    for tag, count in sorted(tag_count.items(), key=lambda x: -x[1]):
        print(f"  {tag}: {count}")

    # 同一カテゴリ内の類似ドキュメント
    print("\n=== 同一カテゴリ内ドキュメント ===")
    by_cat = {}
    for d in docs:
        cat = d.get("category", "unknown")
        by_cat.setdefault(cat, []).append(d["_name"])
    for cat, names in sorted(by_cat.items()):
        print(f"  {cat} ({len(names)}): {', '.join(names)}")

    # ソースURL重複チェック
    print("\n=== ソースURL重複チェック ===")
    by_source = {}
    for d in docs:
        src = d.get("source", "")
        if src and src != "Claude Code 公式 SKILL" and src != "Claude Code 公式 SKILL (examples)":
            by_source.setdefault(src, []).append(d["_name"])
    dupes = {k: v for k, v in by_source.items() if len(v) > 1}
    if dupes:
        for src, names in dupes.items():
            print(f"  重複! {src}: {names}")
    else:
        print("  重複なし")

if __name__ == "__main__":
    main()
