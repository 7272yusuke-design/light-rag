---
source: Claude Code 公式 SKILL
category: skills
sub_categories: [webapp]
tags: [docx, word, document-generation, javascript, xml]
language: 
ingested: 2026-04-09
source_updated: unknown
status: active
---

# SKILL: docx-creation

# SKILL: docx-creation

## 基本情報
- ソース: Claude Code 公式 SKILL
- カテゴリ: tool
- サブカテゴリ: webapp
- 対象技術: docx
- タグ: docx, word, document-generation, javascript, xml
- 最終確認日: 2026-04-09

## 概要
Word文書(.docx)の作成・読み取り・編集・操作スキル。docx-jsによる新規作成、XML直接編集、pandocによるテキスト抽出、LibreOfficeによる変換をカバー。

## 使用トリガー
Word doc, .docx, レポート, メモ, レター等のWord文書リクエスト

## 主要手順
新規作成はdocx-js(npm)。既存編集はunpack→XML編集→repack。読み取りはpandoc。バリデーションはvalidate.py。ページサイズはDXA単位で明示指定必須。

## ベストプラクティス
ページサイズ明示指定。作成後validate.py検証。.docはLibreOfficeで変換後処理。

## 関連技術
pandoc, LibreOffice, docx-js, XML


## 関連ナレッジ
- (なし)
