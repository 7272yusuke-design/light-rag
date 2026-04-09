---
source: Claude Code 公式 SKILL
category: skills
sub_categories: []
tags: [file-handling, python, cli, data-extraction]
language: 
ingested: 2026-04-09
source_updated: unknown
status: active
---

# SKILL: file-reading

# SKILL: file-reading

## 基本情報
- ソース: Claude Code 公式 SKILL
- カテゴリ: tool
- サブカテゴリ: 
- 対象技術: 全ファイル形式
- タグ: file-handling, python, cli, data-extraction
- 最終確認日: 2026-04-09

## 概要
ファイル拡張子に基づき最適な読み取り方法をディスパッチするルータースキル。PDF,DOCX,XLSX,CSV,JSON,画像,アーカイブ対応。

## 使用トリガー
/mnt/user-data/uploads/パス、uploaded_filesブロック

## 主要手順
1.拡張子判定 2.statでサイズ確認 3.最小限読み取り 4.専用SKILLへハンドオフ

## ベストプラクティス
catで直接読まない。バイナリは専用ツール。大きいファイルはサンプリング。

## 関連技術
pandoc, pdfinfo, openpyxl, pandas, jq


## 関連ナレッジ
- (なし)
