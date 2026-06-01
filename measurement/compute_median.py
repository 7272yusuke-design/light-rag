#!/usr/bin/env python3
"""5回のrunから中央値(min/median/max)を計算してCSV出力。

Usage: python3 compute_median.py <label> <run1.json> <run2.json> ... <runN.json>
"""
import sys
import json
import statistics
import tiktoken

enc = tiktoken.get_encoding("cl100k_base")

def count(text):
    return len(enc.encode(text))

def extract_content(data):
    """既存 count_tokens.py と同じロジック"""
    result = data.get("result", {})
    content = result.get("content")
    if isinstance(content, list) and content:
        return "\n".join(c.get("text", "") for c in content if isinstance(c, dict))
    if "tools" in result:
        return json.dumps(result["tools"], ensure_ascii=False)
    return json.dumps(result, ensure_ascii=False)

label = sys.argv[1]
files = sys.argv[2:]

full_tokens = []
content_tokens = []
byte_sizes = []

for path in files:
    with open(path, "rb") as f:
        raw = f.read()
    text = raw.decode("utf-8", errors="replace")
    byte_sizes.append(len(raw))
    full_tokens.append(count(text))
    try:
        data = json.loads(text)
        content_tokens.append(count(extract_content(data)))
    except Exception:
        content_tokens.append(-1)

def stats(arr):
    return min(arr), int(statistics.median(arr)), max(arr)

b_min, b_med, b_max = stats(byte_sizes)
f_min, f_med, f_max = stats(full_tokens)
c_min, c_med, c_max = stats(content_tokens)

# 変動率(中央値に対する最大ブレ)
def variation(arr, med):
    if med == 0:
        return 0
    return max(abs(x - med) for x in arr) / med * 100

f_var = variation(full_tokens, f_med)
c_var = variation(content_tokens, c_med)

print(f"label={label}, runs={len(files)}")
print(f"  bytes:           min={b_min}, median={b_med}, max={b_max}")
print(f"  tokens_full:     min={f_min}, median={f_med}, max={f_max} (variation: {f_var:.1f}%)")
print(f"  tokens_content:  min={c_min}, median={c_med}, max={c_max} (variation: {c_var:.1f}%)")
print()
print(f"CSV: {label},{b_med},{f_med},{c_med},{f_var:.1f},{c_var:.1f}")
