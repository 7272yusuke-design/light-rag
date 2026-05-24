#!/usr/bin/env python3
"""Count tokens in MCP JSON-RPC response files using tiktoken (cl100k_base)."""
import sys
import json
import tiktoken

enc = tiktoken.get_encoding("cl100k_base")

def count(text):
    return len(enc.encode(text))

def extract_content(data):
    """Extract relevant text from MCP response."""
    result = data.get("result", {})
    content = result.get("content")
    if isinstance(content, list) and content:
        return "\n".join(c.get("text", "") for c in content if isinstance(c, dict))
    if "tools" in result:
        return json.dumps(result["tools"], ensure_ascii=False)
    return json.dumps(result, ensure_ascii=False)

print("file,bytes,tokens_full_json,tokens_content_only")
for path in sys.argv[1:]:
    with open(path, "rb") as f:
        raw = f.read()
    text = raw.decode("utf-8", errors="replace")
    tk_full = count(text)
    try:
        data = json.loads(text)
        tk_content = count(extract_content(data))
    except Exception:
        tk_content = -1
    print(f"{path},{len(raw)},{tk_full},{tk_content}")
