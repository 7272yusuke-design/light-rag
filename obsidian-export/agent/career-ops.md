---
source: https://github.com/santifer/career-ops
category: agent
sub_categories: [workflow, tool]
tags: [job-search, AI-agent, claude, go, nodejs, bubbletea, CV-generation, ATS-optimization]
language: 
ingested: 2026-04-11
source_updated: unknown
status: active
---

# career-ops

# career-ops

## 基本情報
- リポジトリ: https://github.com/santifer/career-ops
- カテゴリ: agent
- サブカテゴリ: workflow, tool
- タグ: job-search, AI-agent, claude, go, nodejs, bubbletea, CV-generation, ATS-optimization
- 最終確認日: 2026-04-11

## 概要
Career-Ops is an AI-powered job search command center that uses Claude as an agent to evaluate job offers, generate tailored ATS-optimized CVs, scan job portals, and track applications. It supports single-offer evaluation, batch processing with parallel workers, and a full pipeline from JD ingestion to PDF generation and tracker updates. A Go-based TUI dashboard provides visual pipeline management.

## 設計思想
The system follows a mode-routing architecture where a single skill dispatcher delegates to specialized mode files (_shared.md + mode-specific prompt), keeping concerns separated between routing logic, shared context, and mode behavior. Data flows unidirectionally: JD input → evaluation → report.md → PDF → TSV tracker line → applications.md merge. Worker prompts are self-contained to enable headless parallel execution via 'claude -p'. User-layer files (cv.md, config/profile.yml) are read-only to the agent; all writes go through dedicated output paths with integrity verification scripts.

## 主要コンポーネント
- modes/*.md: Prompt modules defining behavior for each operation mode (evaluate, scan, batch, apply, etc.)
- batch/batch-runner.sh: Bash orchestrator launching parallel claude -p workers, managing state/retries via TSV
- batch/batch-prompt.md: Self-contained worker prompt template with placeholder substitution for batch jobs
- generate-pdf.mjs: Node.js script using Puppeteer/Playwright to render ATS-optimized CV HTML to PDF
- merge-tracker.mjs: Merges batch TSV tracker additions into the canonical applications.md tracker
- dashboard/: Go TUI application (Bubble Tea) for visualizing and managing the job application pipeline
- templates/cv-template.html: HTML template with placeholder tokens for tailored CV generation
- modes/_shared.md: Shared context loaded by most modes: archetype table, North Star, negotiation scripts

## 実装パターン
- Mode Router Pattern: A single entry-point skill dispatches to specialized mode files based on argument detection, enabling a unified /career-ops interface with deeply modular behavior
- Self-Contained Worker Prompt: Batch workers receive a fully resolved prompt with all context embedded, enabling stateless parallel execution via headless claude -p without external dependencies
- TSV Append + Merge: Workers write atomic TSV lines to individual files in tracker-additions/, which are later merged by merge-tracker.mjs to avoid concurrent write conflicts on applications.md
- 5-Tier URL Enrichment: Dashboard enriches application records with job URLs via a cascade: report header → batch ID lookup → state file mapping → scan history → company name fallback
- Archetype-Adaptive Framing: Job descriptions are classified into one of 6 role archetypes, and all downstream outputs (CV bullets, STAR stories, PDF summary) are reframed to match the detected archetype without fabricating experience

## 適用シーン
Ideal for active job seekers who want AI-assisted evaluation of multiple offers simultaneously, automated ATS-tuned CV generation per application, structured interview preparation, and a persistent tracked pipeline. Particularly useful for technical professionals applying to 10+ roles in parallel who need consistent scoring, PDF output, and status tracking without manual effort.

## 注意点・制約
Requires Claude Code (claude CLI) with sufficient subscription for parallel workers; batch processing with high parallelism consumes significant API usage. PDF generation depends on Playwright/Chromium being installed. The system is entirely local with no hosted backend—all data lives in local files. The cv.md and profile.yml files must be manually maintained as the source of truth; the agent never writes to them. Posting freshness verification is unavailable in batch mode (no Playwright in headless workers). Multi-language modes (de/fr/ja/pt/ru) are provided but may have less polish than the English baseline.


## 関連ナレッジ
- (なし)
