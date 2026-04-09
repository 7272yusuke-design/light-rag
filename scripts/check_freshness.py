#!/usr/bin/env python3
"""鮮度チェック: 6ヶ月以上経過で review-needed"""
import os, re, sys
from datetime import date, timedelta

THRESHOLD_DAYS = 180  # 6ヶ月

def main():
    fix = "--fix" in sys.argv
    vault = "obsidian-export"
    today = date.today()
    stale = []

    for root, dirs, files in os.walk(vault):
        for f in files:
            if not f.endswith(".md") or f.startswith("_"):
                continue
            path = os.path.join(root, f)
            text = open(path).read()
            m_ingested = re.search(r'^ingested: (\d{4}-\d{2}-\d{2})', text, re.MULTILINE)
            m_status = re.search(r'^status: (\S+)', text, re.MULTILINE)
            if not m_ingested:
                continue
            ingested = date.fromisoformat(m_ingested.group(1))
            status = m_status.group(1) if m_status else "unknown"
            age = (today - ingested).days

            if age > THRESHOLD_DAYS and status == "active":
                stale.append({"path": path, "name": f, "ingested": str(ingested), "age": age})
                if fix:
                    new_text = text.replace("status: active", "status: review-needed")
                    open(path, "w").write(new_text)

    if stale:
        print(f"=== 鮮度警告: {len(stale)}件が{THRESHOLD_DAYS}日超過 ===")
        for s in stale:
            flag = " → review-needed に更新" if fix else ""
            print(f"  {s['name']}: 投入{s['ingested']} ({s['age']}日前){flag}")
    else:
        print(f"=== 全ドキュメント鮮度OK（{THRESHOLD_DAYS}日以内） ===")

    # 全ドキュメントの鮮度サマリー
    print(f"\n=== 鮮度サマリー ===")
    for root, dirs, files in os.walk(vault):
        for f in sorted(files):
            if not f.endswith(".md") or f.startswith("_"):
                continue
            path = os.path.join(root, f)
            text = open(path).read()
            m_i = re.search(r'^ingested: (\d{4}-\d{2}-\d{2})', text, re.MULTILINE)
            m_s = re.search(r'^status: (\S+)', text, re.MULTILINE)
            if m_i:
                age = (today - date.fromisoformat(m_i.group(1))).days
                status = m_s.group(1) if m_s else "?"
                print(f"  {f:30} {m_i.group(1)}  ({age:3}日)  [{status}]")

if __name__ == "__main__":
    main()
