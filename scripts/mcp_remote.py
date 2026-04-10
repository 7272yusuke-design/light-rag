#!/usr/bin/env python3
"""LightRAG MCP Server - Fully stateless, no SSE"""
import json
import urllib.request
import urllib.parse
import os

from starlette.applications import Starlette
from starlette.routing import Route
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

LIGHTRAG_URL = os.environ.get("LIGHTRAG_URL", "http://localhost:9621")
LIGHTRAG_USER = os.environ.get("LIGHTRAG_USER", "admin")
LIGHTRAG_PASS = os.environ.get("LIGHTRAG_PASS", "LightRag@2026!")
PROFILE_PATH = os.environ.get("PROFILE_PATH", "/docker/lightrag/config/project_profiles.json")

TOOLS = [
    {
        "name": "search_knowledge",
        "description": "Search the LightRAG knowledge base. Args: query (required), mode (hybrid/local/global/naive), project (openclaw/virtual-protocol/website/webapp/workflow)",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "mode": {"type": "string", "default": "hybrid"},
                "project": {"type": "string", "default": ""}
            },
            "required": ["query"]
        }
    },
    {
        "name": "list_knowledge",
        "description": "List all documents in the LightRAG knowledge base.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "list_projects",
        "description": "List available project filters for knowledge search.",
        "inputSchema": {"type": "object", "properties": {}}
    }
]


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


def do_search(args):
    query = args.get("query", "")
    mode = args.get("mode", "hybrid")
    project = args.get("project", "")
    search_query = query
    if project:
        profiles = load_profiles()
        if project in profiles:
            kw = profiles[project].get("keywords", [])
            if kw:
                search_query = f"{query} {' '.join(kw[:3])}"
    result = api_request("/query/data", method="POST", body={"query": search_query, "mode": mode})
    if isinstance(result, dict) and result.get("status") == "success":
        data = result.get("data", {})
        chunks = []
        for key, items in data.items():
            if isinstance(items, list):
                for item in items[:10]:
                    if isinstance(item, dict):
                        content = item.get("content", item.get("description", str(item)))
                        chunks.append(f"[{key}] {str(content)[:500]}")
                    elif isinstance(item, str):
                        chunks.append(f"[{key}] {item[:500]}")
        return "\n\n".join(chunks) if chunks else json.dumps(data, ensure_ascii=False)[:4000]
    return json.dumps(result, ensure_ascii=False)[:4000]


def do_list_knowledge(args):
    result = api_request("/documents")
    items = result.get("statuses", {}).get("processed", [])
    lines = []
    for doc in items:
        s = doc.get("content_summary", "")
        name = category = tags = ""
        for l in s.split("\n"):
            l = l.strip()
            if l.startswith("# "): name = l[2:].replace("SKILL: ", "")
            elif l.startswith("- カテゴリ:"): category = l.split(":", 1)[1].strip()
            elif l.startswith("- タグ:"): tags = l.split(":", 1)[1].strip()
        lines.append(f"- {name} [{category}] tags: {tags}")
    return f"Total: {len(items)} documents\n" + "\n".join(lines)


def do_list_projects(args):
    profiles = load_profiles()
    lines = []
    for name, p in profiles.items():
        lines.append(f"- {name}: {p.get('description','')} (keywords: {', '.join(p.get('keywords',[]))})")
    return "\n".join(lines) if lines else "No project profiles configured."


HANDLERS = {"search_knowledge": do_search, "list_knowledge": do_list_knowledge, "list_projects": do_list_projects}


def rpc_response(id, result):
    return {"jsonrpc": "2.0", "id": id, "result": result}


async def handle_mcp(request: Request):
    # Reject GET - no server notifications needed
    if request.method == "GET":
        return Response(status_code=405)

    body = await request.json()
    method = body.get("method", "")
    id = body.get("id")
    params = body.get("params", {})

    if method == "initialize":
        return JSONResponse(rpc_response(id, {
            "protocolVersion": "2025-03-26",
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "lightrag-knowledge", "version": "1.0.0"}
        }), headers={"mcp-session-id": "stateless"})

    if method == "notifications/initialized" or method.startswith("notifications/"):
        return Response(status_code=202)

    if method == "tools/list":
        return JSONResponse(rpc_response(id, {"tools": TOOLS}), headers={"mcp-session-id": "stateless"})

    if method == "tools/call":
        tool = params.get("name", "")
        handler = HANDLERS.get(tool)
        if handler:
            try:
                text = handler(params.get("arguments", {}))
                return JSONResponse(rpc_response(id, {"content": [{"type": "text", "text": text}]}), headers={"mcp-session-id": "stateless"})
            except Exception as e:
                return JSONResponse(rpc_response(id, {"content": [{"type": "text", "text": f"Error: {e}"}], "isError": True}))
        return JSONResponse({"jsonrpc": "2.0", "id": id, "error": {"code": -32601, "message": f"Unknown tool: {tool}"}})

    if method == "ping":
        return JSONResponse(rpc_response(id, {}))

    return JSONResponse({"jsonrpc": "2.0", "id": id, "error": {"code": -32601, "message": f"Unknown: {method}"}})


app = Starlette(routes=[Route("/mcp", handle_mcp, methods=["GET", "POST"])])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9622)
