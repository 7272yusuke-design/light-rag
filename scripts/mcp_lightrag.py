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
    """LightRAGナレッジベースを検索する。GitHub OSS、Claude Code SKILL、技術ドキュメントの構造化知識を横断検索。modeはhybrid/local/global/naiveから選択。projectにopenclaw/virtual-protocol/website/webapp/workflowを指定するとプロジェクト文脈で絞り込む。"""
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

@mcp.tool()
def list_projects() -> str:
    """利用可能なプロジェクトプロファイル一覧を表示する。search_knowledgeのproject引数に使える。"""
    try:
        with open(PROFILE_PATH) as f:
            profiles = json.load(f)
        return "\n".join(f"- {k}: {v['description']}" for k, v in profiles.items())
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    mcp.run(transport="stdio")
