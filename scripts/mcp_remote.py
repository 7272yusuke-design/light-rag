#!/usr/bin/env python3
"""LightRAG Remote MCP Server (Streamable HTTP for Claude.ai)"""
import json
import urllib.request
import urllib.parse
import os

# Disable MCP transport security (allows proxy host headers)
os.environ["MCP_DISABLE_TRANSPORT_SECURITY"] = "1"

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("lightrag-knowledge", host="0.0.0.0", port=9622)

LIGHTRAG_URL = os.environ.get("LIGHTRAG_URL", "http://localhost:9621")
LIGHTRAG_USER = os.environ.get("LIGHTRAG_USER", "admin")
LIGHTRAG_PASS = os.environ.get("LIGHTRAG_PASS", "LightRag@2026!")
PROFILE_PATH = os.environ.get("PROFILE_PATH", "/docker/lightrag/config/project_profiles.json")


def get_token():
    data = urllib.parse.urlencode({"username": LIGHTRAG_USER, "password": LIGHTRAG_PASS}).encode()
    req = urllib.request.Request(f"{LIGHTRAG_URL}/login", data=data, method="POST")
    with urllib.request.urlopen(req) as resp:
        return json.load(resp)["access_token"]


def api_request(path, method="GET", body=None):
    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(f"{LIGHTRAG_URL}{path}", data=data, headers=headers, method=method)
    with urllib.request.urlopen(req) as resp:
        return json.load(resp)


def load_profiles():
    try:
        with open(PROFILE_PATH) as f:
            return json.load(f)
    except Exception:
        return {}


@mcp.tool()
def search_knowledge(query: str, mode: str = "hybrid", project: str = "") -> str:
    """Search the LightRAG knowledge base.

    Args:
        query: Search query (e.g. "multi-agent framework", "browser automation")
        mode: Search mode - hybrid (default), local, global, or naive
        project: Optional project filter - openclaw, virtual-protocol, website, webapp, workflow
    """
    search_query = query
    if project:
        profiles = load_profiles()
        if project in profiles:
            keywords = profiles[project].get("keywords", [])
            if keywords:
                search_query = f"{query} {' '.join(keywords[:3])}"
    try:
        result = api_request("/query", method="POST", body={"query": search_query, "mode": mode})
        if isinstance(result, dict) and "response" in result:
            return result["response"]
        return json.dumps(result, ensure_ascii=False)[:4000]
    except Exception as e:
        return f"Search error: {e}"


@mcp.tool()
def list_knowledge() -> str:
    """List all documents stored in the LightRAG knowledge base.
    Returns names, categories, and tags for all indexed knowledge."""
    try:
        result = api_request("/documents")
        items = result.get("statuses", {}).get("processed", [])
        lines = []
        for doc in items:
            summary = doc.get("content_summary", "")
            name = category = tags = ""
            for line in summary.split("\n"):
                line = line.strip()
                if line.startswith("# "):
                    name = line[2:].replace("SKILL: ", "")
                elif line.startswith("- カテゴリ:"):
                    category = line.split(":", 1)[1].strip()
                elif line.startswith("- タグ:"):
                    tags = line.split(":", 1)[1].strip()
            lines.append(f"- {name} [{category}] tags: {tags}")
        return f"Total: {len(items)} documents\n" + "\n".join(lines)
    except Exception as e:
        return f"Error: {e}"


@mcp.tool()
def list_projects() -> str:
    """List available project filters for knowledge search."""
    profiles = load_profiles()
    lines = []
    for name, p in profiles.items():
        desc = p.get("description", "")
        kw = ", ".join(p.get("keywords", []))
        lines.append(f"- {name}: {desc} (keywords: {kw})")
    return "\n".join(lines) if lines else "No project profiles configured."


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
