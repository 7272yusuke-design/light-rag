#!/usr/bin/env python3
"""record_decision — KNOWLEDGE-DECISIONS.md追記 + git commit/push
C-2実装。C-1(Claude Codeスキル化)からも流用可能な独立モジュール。
安全方針: 追記のみ / 事前バックアップ / 例外時復元 / git失敗でも追記は保持
"""
import os
import shutil
import subprocess
from datetime import date

DECISIONS_PATH = os.environ.get("DECISIONS_PATH", "/docker/lightrag/docs/KNOWLEDGE-DECISIONS.md")
REPO_DIR = os.environ.get("REPO_DIR", "/docker/lightrag")
BACKUP_PATH = DECISIONS_PATH + ".bak-rd"

VALID_TYPES = ["L3投入", "L2c投入", "保留", "見送り"]

TOOL_DEF = {
    "name": "record_decision",
    "description": "Append a decision entry to KNOWLEDGE-DECISIONS.md and git commit/push.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "decision_type": {"type": "string", "enum": VALID_TYPES},
            "name": {"type": "string", "description": "e.g. zerolang-l3"},
            "repo": {"type": "string", "description": "Repository URL"},
            "reason": {"type": "string", "description": "投入根拠/見送り理由"},
            "reeval_triggers": {"type": "string", "description": "再検討条件(改行区切りで複数可、具体ビジネスイベント形式)"},
            "related": {"type": "string", "description": "cross-ref/関連ナレッジ(任意)"},
            "notes": {"type": "string", "description": "注記(任意)"},
            "date": {"type": "string", "description": "YYYY-MM-DD(省略時は当日)"}
        },
        "required": ["decision_type", "name", "repo", "reason", "reeval_triggers"]
    }
}


def _format_entry(a):
    d = a.get("date") or date.today().isoformat()
    lines = [
        "",
        "---",
        "",
        f"## {d}: {a['name']} — {a['decision_type']}",
        "",
        f"- **対象:** {a['repo']}",
        f"- **判断:** {a['decision_type']}({a['name']})",
        f"- **根拠:** {a['reason']}",
    ]
    if a.get("notes"):
        lines.append(f"- **注記:** {a['notes']}")
    if a.get("related"):
        lines.append(f"- **関連:** {a['related']}")
    lines.append("- **再検討条件:**")
    triggers = [t.strip() for t in a["reeval_triggers"].splitlines() if t.strip()]
    for i, t in enumerate(triggers, 1):
        lines.append(f"  {i}. {t}")
    lines.append("")
    return "\n".join(lines)


def _git(arglist):
    return subprocess.run(["git"] + arglist, capture_output=True,
                          text=True, timeout=30, cwd=REPO_DIR)


def do_record_decision(args):
    missing = [k for k in ("decision_type", "name", "repo", "reason", "reeval_triggers")
               if not args.get(k)]
    if missing:
        return f"Error: missing required args: {', '.join(missing)}"
    if args["decision_type"] not in VALID_TYPES:
        return f"Error: decision_type must be one of {VALID_TYPES}"
    if not os.path.exists(DECISIONS_PATH):
        return f"Error: {DECISIONS_PATH} not found"

    entry = _format_entry(args)

    # 安全装置1: 事前バックアップ
    shutil.copy2(DECISIONS_PATH, BACKUP_PATH)

    # 安全装置2: 追記モードのみ(既存内容を書き換える経路が存在しない)
    try:
        with open(DECISIONS_PATH, "a", encoding="utf-8") as f:
            f.write(entry)
    except Exception as e:
        shutil.copy2(BACKUP_PATH, DECISIONS_PATH)  # 安全装置3: 復元
        return f"Error: append failed, restored from backup: {e}"

    # git(失敗しても追記は残す。commit対象はDECISIONSのみに限定)
    r = _git(["add", "docs/KNOWLEDGE-DECISIONS.md"])
    if r.returncode != 0:
        return f"Appended OK | git add failed: {r.stderr.strip()[:200]}"
    r = _git(["commit", "-m", f"docs(decisions): record {args['name']} ({args['decision_type']})"])
    if r.returncode != 0:
        return f"Appended OK | git commit failed: {r.stderr.strip()[:200]}"
    commit = _git(["rev-parse", "--short", "HEAD"]).stdout.strip()
    r = _git(["push", "origin", "HEAD"])
    if r.returncode != 0:
        return f"Appended + committed ({commit}) | push failed (retry later): {r.stderr.strip()[:200]}"
    return f"Recorded: {args['name']} ({args['decision_type']}) | commit {commit} | pushed"
