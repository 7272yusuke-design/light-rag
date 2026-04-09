#!/usr/bin/env python3
"""Obsidian用MDファイル生成"""
import argparse
import json
import os
from datetime import date

def export_md(meta: dict, output_dir: str):
    category = meta.get("category", "uncategorized")
    name = meta.get("name", "untitled")
    
    outdir = os.path.join(output_dir, category)
    os.makedirs(outdir, exist_ok=True)
    outpath = os.path.join(outdir, f"{name}.md")

    tags_str = ", ".join(meta.get("tags", []))
    sub_cats = ", ".join(meta.get("sub_categories", []))

    frontmatter = f"""---
source: {meta.get('source', '')}
category: {category}
sub_categories: [{sub_cats}]
tags: [{tags_str}]
language: {meta.get('language', '')}
ingested: {date.today().isoformat()}
source_updated: {meta.get('source_updated', 'unknown')}
status: active
---"""

    body = meta.get("body", "")
    related = meta.get("related", [])
    related_links = "\n".join(f"- [[{r}]]" for r in related) if related else "- (なし)"

    content = f"""{frontmatter}

# {meta.get('title', name)}

{body}

## 関連ナレッジ
{related_links}
"""
    with open(outpath, "w") as f:
        f.write(content)
    print(f"OK: {outpath}")
    return outpath

def main():
    p = argparse.ArgumentParser()
    p.add_argument("meta_json", help="メタデータJSONファイル")
    p.add_argument("-o", "--output-dir", default="obsidian-export")
    args = p.parse_args()

    meta = json.load(open(args.meta_json))
    export_md(meta, args.output_dir)

if __name__ == "__main__":
    main()
