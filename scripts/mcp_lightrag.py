#!/usr/bin/env python3
"""LightRAG MCP Server using official SDK"""
import json
import urllib.request
import urllib.parse
import os
import signal
import sys
from mcp.server.fastmcp import FastMCP

# Auto-exit when parent process (Claude Code) dies
try:
    import ctypes
    libc = ctypes.CDLL("libc.so.6")
    libc.prctl(1, signal.SIGHUP)
except Exception:
    pass
signal.signal(signal.SIGHUP, lambda *_: sys.exit(0))

mcp = FastMCP("lightrag")

LIGHTRAG_URL = os.environ.get("LICHTRAG_URL", "http://localhost:9621")
LIGHTRAG_USER = os.environ.get("LICHTRAG_USER", "admin")
LIGHTRAG_PASS = os.environ.get("LICHTRAG_PASS", "LightRag@2026!")
PROFILE_PATH = os.environ.get("PROFILE_PATH", "/docker/lightrag/config/project_profiles.json")

def get_token():
    data = urllib.parse.urlencode({"username": LIGHTRAG_USER, "password": LIGHTRAG_PASS}).encode()
    req = urllib.request.Request(f"{LIGHTRAG_URL}/login", data=data, method="POST")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read())["access_token"]

def load_project_context(project: str) -> str:
    try:
        with open(PROFILE_PATH) as f:
            profiles = json.load(f)
        p = profiles.get(project, {})
        return p.get("context", "")
    except Exception:
        return ""

@mcp.tool()
def search_knowledge(query: str, mode: str = "hybrid", project: str = "") -> str:
    """LightRAGナレッジベースを検索する。GitHub OSS、Claude Code SKILL、抖術ドキュメントの構造化知讚を横断検索。modeはhybrid/local/global/naiveから選択8projectにopenclaw/virtual-protocol/website/webapp/workflowを指定するとプロジェクト文興で絞り込む。"""
    if project:
        ctx = load_project_context(project)
        if ctx:
            query = f"[プロジェクト文脈: {ctx}] {query}"
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
    """LightRAGに蓄秝されたドキュメント一覧を表示する。"""
    token = get_token()
    req = urllib.request.Request(
        f"{LIGHTRAG_URL}/documents",
        headers={"Authorization": f"Bearer {token}"},
    )
    with urllib.request.urlopen(req) as resp:
        docs = json.loads(resp.read())
    if isinstance(docs, list):
        lines = []
        for d in docs[:50]:
            did = d.get('id', '?')
            name = d.get('name', d.get('metadata', {}).get('file_name', '?'))
            lines.append(f"- {did}: {name}")
        return "\n".join(lines)
    return str(docs)

@mcp.tool()
def list_projects() -> str:
    """利用可能なプロジェクトプロファイル一覧を表示する。search_knowledgeのproject引数に使える。"""
    try:
        with open(PROFILE_PATH) as f:
            profiles = json.load(f)
        lines = []
        for k, v in profiles.items():
            lines.append(f"- {k}: {v['description']}")
        return "\n".join(lines)
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    mcp.run(transport="stdio")
