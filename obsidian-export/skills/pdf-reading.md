---
source: Claude Code 公式 SKILL
category: skills
sub_categories: []
tags: [pdf, python, ocr, text-extraction, data-extraction]
language: 
ingested: 2026-04-09
source_updated: unknown
status: active
---

# SKILL: pdf-reading

# SKILL: pdf-reading

## 基本情報
- ソース: Claude Code 公式 SKILL
- カテゴリ: tool
- サブカテゴリ: 
- 対象技術: pdf
- タグ: pdf, python, ocr, text-extraction, data-extraction
- 最終確認日: 2026-04-09

## 概要
PDF読み取り・検査・コンテンツ抽出特化スキル。コンテンツインベントリ、ラスタライズ、埋め込み抽出、タイプ別読み取り戦略。

## 使用トリガー
PDF内容確認、テキスト抽出、テーブル抽出、スキャンPDF OCR

## 主要手順
1.pdfinfo+pdftotext 1ページでインベントリ 2.pdfimagesで画像確認 3.pypdf/pdfplumberでテキスト抽出 4.pdftoppmでラスタライズ

## ベストプラクティス
まずpdfinfo+pdftotext 1ページで確認。図表はラスタライズ。スキャンPDFはOCR。

## 関連技術
pypdf, pdfplumber, pdftotext, pdftoppm, pdfinfo


## 関連ナレッジ
- (なし)
