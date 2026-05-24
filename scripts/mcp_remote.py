#!/usr/bin/env python3
"""LightRAG MCP Server - Fully stateless, no SSE"""
import json
import urllib.request
import urllib.parse
import os
import subprocess

from starlette.applications import Starlette
from starlette.routing import Route
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from middleware.compression import compress_response

LIGHTRAG_URL = os.environ.get("LIGHTRAG_URL", "http://localhost:9621")
LIGHTRAG_USER = os.environ.get("LIGHTRAG_USER", "admin")
LIGHTRAG_PASS = os.environ.get("LIGHTRAG_PASS", "LightRag@2026!")
PROFILE_PATH = os.environ.get("PROFILE_PATH", "/docker/lightrag/config/project_profiles.json")

TOOLS = [
    {
        "name": "search_knowledge",
        "description": "Search LightRAG knowledge.",
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
        "description": "List all docs.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "list_projects",
        "description": "List project filters.",
        "inputSchema": {"type": "object", "properties": {}}
    },
    {
        "name": "upload_document",
        "description": "Upload doc to LightRAG.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "file_name": {"type": "string", "description": "File name e.g. skill-docx-l3.txt"},
                "content": {"type": "string", "description": "Doc text"},
                "overwrite": {"type": "boolean", "default": False, "description": "Overwrite if exists"}
            },
            "required": ["file_name", "content"]
        }
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
        output = []
        limits = {"entities": (5, 200), "relationships": (5, 200), "chunks": (3, 300)}
        for key, items in data.items():
            if not isinstance(items, list):
                continue
            max_items, max_chars = limits.get(key, (3, 200))
            seen = set()
            for item in items:
                if len(seen) >= max_items:
                    break
                if isinstance(item, dict):
                    text = item.get("content", item.get("description", ""))
                elif isinstance(item, str):
                    text = item
                else:
                    continue
                short = str(text)[:max_chars]
                if short not in seen:
                    seen.add(short)
                    output.append(f"[{key}] {short}")
        ref_items = data.get("references", [])
        if isinstance(ref_items, list):
            for ref in ref_items[:10]:
                if isinstance(ref, dict):
                    output.append(f"[references] {json.dumps(ref, ensure_ascii=False)}")
        text = "\n\n".join(output) if output else json.dumps(data, ensure_ascii=False)[:2000]
        return compress_response(text, level="off")
    return compress_response(json.dumps(result, ensure_ascii=False)[:2000], level="off")


def do_list_knowledge(args):
    # SQL側で必要項目のみ抽出(本文内改行による行分裂を回避)
    sql = """
SELECT
  ds.file_path,
  COALESCE((regexp_match(df.content, E'^# (.+)$', 'n'))[1], '') AS name,
  COALESCE((regexp_match(df.content, E'^- カテゴリ: ?(.+)$', 'n'))[1], '') AS category,
  COALESCE((regexp_match(df.content, E'^- タグ: ?(.+)$', 'n'))[1], '') AS tags
FROM lightrag_doc_status ds JOIN lightrag_doc_full df ON ds.id = df.id
ORDER BY ds.file_path;
""".strip()
    cmd = ["docker", "compose", "exec", "-T", "postgres",
           "psql", "-U", "lightrag", "-d", "lightrag", "-tAF", "\x1f", "-c", sql]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30, cwd="/docker/lightrag")
        rows = [r for r in result.stdout.split("\n") if r.strip()]
    except Exception as e:
        return f"DB query failed: {e}"
    lines = []
    for row in rows:
        parts = row.split("\x1f")
        if len(parts) < 4:
            continue
        file_path, name, category, tags = parts[0], parts[1].replace("SKILL: ", ""), parts[2], parts[3]
        lines.append(f"- {name} [{category}] tags: {tags}")
    return f"Total: {len(rows)} documents\n" + "\n".join(lines)


def do_list_projects(args):
    profiles = load_profiles()
    lines = []
    for name, p in profiles.items():
        lines.append(f"- {name}: {p.get('description','')} (keywords: {', '.join(p.get('keywords',[]))})")
    return "\n".join(lines) if lines else "No project profiles configured."



def do_upload_document(args):
    file_name = args.get("file_name", "")
    content = args.get("content", "")
    overwrite = args.get("overwrite", False)
    if not file_name or not content:
        return "Error: file_name and content are required"
    token = get_token()
    # overwrite: delete existing
    if overwrite:
        try:
            result = api_request("/documents")
            items = result.get("statuses", {}).get("processed", [])
            for doc in items:
                if doc.get("file_path", "") == file_name:
                    req = urllib.request.Request(
                        f"{LIGHTRAG_URL}/documents/{doc['id']}",
                        headers={"Authorization": f"Bearer {token}"},
                        method="DELETE"
                    )
                    urllib.request.urlopen(req)
                    import time; time.sleep(3)
                    token = get_token()
                    break
        except Exception as e:
            return f"Error deleting old doc: {e}"
    # multipart upload
    boundary = "----MCP_UPLOAD_BOUNDARY_2026"
    body = f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{file_name}\"\r\nContent-Type: text/plain\r\n\r\n{content}\r\n--{boundary}--\r\n".encode("utf-8")
    req = urllib.request.Request(
        f"{LIGHTRAG_URL}/documents/upload",
        data=body,
        headers={"Authorization": f"Bearer {token}", "Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST"
    )
    with urllib.request.urlopen(req) as resp:
        result = json.load(resp)
    status = result.get("status", "unknown")
    msg = result.get("message", "")
    return f"Status: {status} | {msg} | Size: {len(content)} bytes"

HANDLERS = {"search_knowledge": do_search, "list_knowledge": do_list_knowledge, "list_projects": do_list_projects, "upload_document": do_upload_document}


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
