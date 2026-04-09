#!/usr/bin/env python3
"""LightRAG MCP Server using official SDK"""

import json
import urllib.request
import urllib.parse
import os
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("lightrag")

LIGHTRAG_URL = os.environ.get("LIGHTRAG_URL", "http://localhost:9621")
LIGHTRAG_USER = os.environ.get("LIGHTRAG_USER", "admin")
LIGHTRAG_PASS = os.environ.get("LIGHTRAG_PASS", "LightRag@2026!")

def get_token():
    data = urllib.parse.urlencode({"username": LIGHTRAG_USER, "password": LIGHTRAG_PASS}).encode()
    req = urllib.request.Request(f"{LIGHTRAG_URL}/login", data=data, method="POST")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())["access_token"]

@mcp.tool()
def search_knowledge(query: str, mode: str = "hybrid") -> str:
    """LightRAGナレッジベースを検索する。GitHub OSS、Claude Code SKILL、技術ドキュメントの構造化知識を横断検索。modeはhybrid/local/global/naiveから選択。"""
    token = get_token()
    payload = json.dumps({"query": query, "mode": mode}).encode()
    req = urllib.request.Request(
        f"{LIGHTRAG_URL}/query",
        data=payload,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())
    return result.get("response", str(result))

@mcp.tool()
def list_knowledge() -> str:
    """LightRAGに蓄積されたドキュメント一覧を表示する。"""
    token = get_token()
    req = urllib.request.Request(
        f"{LIGHTRAG_URL}/documents",
        headers={"Authorization": f"Bearer {token}"},
    )
    with urllib.request.urlopen(req) as resp:
        docs = json.loads(resp.read())
    if isinstance(docs, list):
        return "\n".join(f"- {d.get('id','?')}: {d.get('name', d.get('metadata',{}).get('file_name','?'))}" for d in docs[:50])
    return str(docs)

if __name__ == "__main__":
    mcp.run(transport="stdio")
