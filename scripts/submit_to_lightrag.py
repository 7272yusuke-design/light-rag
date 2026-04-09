#!/usr/bin/env python3
"""LightRAG APIへのドキュメント投入ラッパー"""
import argparse
import requests
import sys
import os
import tempfile

API_BASE = os.environ.get("LIGHTRAG_API", "http://localhost:9621")
USERNAME = os.environ.get("LIGHTRAG_USER", "admin")
PASSWORD = os.environ.get("LIGHTRAG_PASS", "LightRag@2026!")

def get_token():
    r = requests.post(f"{API_BASE}/login", data={"username": USERNAME, "password": PASSWORD})
    r.raise_for_status()
    return r.json()["access_token"]

def upload_text(token: str, text: str, filename: str = "document.txt"):
    """テキストをtmpファイル経由でアップロード"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
        f.write(text)
        f.flush()
        tmp = f.name
    try:
        with open(tmp, "rb") as fh:
            r = requests.post(
                f"{API_BASE}/documents/upload",
                headers={"Authorization": f"Bearer {token}"},
                files={"file": (filename, fh, "text/plain")},
            )
        r.raise_for_status()
        return r.json()
    finally:
        os.unlink(tmp)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("input", help="投入するテキストファイル")
    args = p.parse_args()

    text = open(args.input).read()
    if not text.strip():
        print("ERROR: 空のファイル", file=sys.stderr)
        sys.exit(1)

    token = get_token()
    result = upload_text(token, text, os.path.basename(args.input))
    print(f"OK: {result}")

if __name__ == "__main__":
    main()
