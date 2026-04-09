#!/usr/bin/env python3
"""タグ正規化: Obsidian MDのタグを統一"""
import os, re, sys

NORMALIZE_MAP = {
    "nextjs": ["next.js", "next", "Next"],
    "react": ["React.js", "reactjs", "React"],
    "multi-agent": ["multiagent", "multi_agent"],
    "websocket": ["web-socket", "ws"],
    "typescript": ["TypeScript", "Typescript", "TS"],
    "python": ["Python"],
    "javascript": ["JavaScript", "Javascript", "JS"],
    "mcp": ["MCP", "model-context-protocol"],
    "rag": ["RAG"],
    "llm": ["LLM"],
    "fastapi": ["FastAPI"],
    "docker": ["Docker"],
    "sqlite": ["SQLite"],
    "pytorch": ["PyTorch"],
    "ai-sdk": ["AI-SDK"],
    "sse": ["SSE"],
    "cli": ["CLI"],
    "ocr": ["OCR"],
}

def normalize_tag(tag):
    tag_stripped = tag.strip()
    for canonical, aliases in NORMALIZE_MAP.items():
        if tag_stripped == canonical:
            return canonical
        if tag_stripped in aliases:
            return canonical
        if tag_stripped.lower() == canonical.lower():
            return canonical
    return tag_stripped.lower()

def process_file(filepath, dry_run=True):
    text = open(filepath).read()
    m = re.search(r'^tags: \[(.+)\]', text, re.MULTILINE)
    if not m:
        return False
    original = m.group(1)
    tags = [t.strip() for t in original.split(",")]
    normalized = list(dict.fromkeys(normalize_tag(t) for t in tags))  # 重複除去・順序保持
    new_line = f"tags: [{', '.join(normalized)}]"
    if f"tags: [{original}]" == new_line:
        return False
    if dry_run:
        print(f"  {filepath}")
        print(f"    before: [{original}]")
        print(f"    after:  [{', '.join(normalized)}]")
    else:
        text = text.replace(f"tags: [{original}]", new_line)
        open(filepath, "w").write(text)
        print(f"  FIXED: {filepath}")
    return True

def main():
    dry_run = "--fix" not in sys.argv
    vault = "obsidian-export"
    if dry_run:
        print("=== DRY RUN (--fix で実際に修正) ===\n")
    changed = 0
    for root, dirs, files in os.walk(vault):
        for f in files:
            if f.endswith(".md"):
                if process_file(os.path.join(root, f), dry_run):
                    changed += 1
    print(f"\n変更対象: {changed}件")

if __name__ == "__main__":
    main()
