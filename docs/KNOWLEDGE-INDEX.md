# KNOWLEDGE-INDEX.md — LightRAGナレッジベース インデックス

> 最終更新: 2026-05-01（整理・再棚卸しセッション）  
> 総数: **157件**（全processed、エラー0件）  
> 最適レンジ: 80-120件 → **超過状態**（160件水準で運用中、レンジ再定義検討余地あり）

## レイヤー構成サマリー（2026-05-01 v3最新）

| レイヤー | 件数 | 割合 | 目標 | 前回(04-18) | 増減 |
|---------|------|------|------|------|------|
| L3（実装） | 103 | 65.6% | 50-60% | 48 | **+55** |
| L2（検証済みパターン） | 18 | 11.5% | 20-25% | 16 | +2 |
| L2c（候補パターン） | 19 | 12.1% | 新設レイヤー | 9 | +10 |
| L1-Infra | 1 | 0.6% | 最小限 | 1 | ±0 |
| L1-Ops | 2 | 1.3% | 最小限 | 2 | ±0 |
| L1-old（旧形式） | 1 | 0.6% | リネーム対象 | - | +1 |
| other（旧形式） | 13 | 8.3% | リネーム対象 | 28 | -15 |
| **合計** | **157** | 100% | - | 104 | **+53** |

## 整合性指標（2026-05-01）
- doc_full = doc_status = **157**（一致、ゴースト除去済み）
- バックアップ: `/docker/lightrag/backups/pre-reinventory-20260501-011545.sql` (251MB)

---

## L3: 実装ナレッジ（103件）

### 開発フレームワーク・ライブラリ
- nextjs-l3
- hono-l3
- drizzle-orm-l3
- better-auth-l3
- supabase-l3
- vercel-l3
- turborepo-l3
- fumadocs-l3
- reflex-l3
- remotion-l3
- motion (旧形式 → other枠、リネーム対象)

### 決済・メール・SaaSコンポーネント
- stripe-sdk-l3
- resend-react-email-l3
- cal-diy-l3

### LLM・AIフレームワーク
- claude-agent-sdk-python-l3
- claude-code-action-l3
- ai (Vercel AI SDK、旧形式 → other枠)
- dspy-l3
- inspect-ai-l3
- openllmetry-l3
- langfuse-l3
- posthog-l3

### マルチエージェントフレームワーク
- langgraph-l3
- crewai-l3
- mastra-l3
- autogen-l3
- smolagents-l3
- letta-code-l3
- agent-zero-l3
- open-interpreter-l3
- copilotkit-l3
- claude-octopus-l3
- openclaude-l3
- wshobson-agents-l3
- everything-claude-code-l3
- gbrain-l3
- paseo-l3

### Coding Agent / IDE拡張
- gstack-garrytan-l3
- daymade-skills-l3
- antigravity-awesome-skills-l3
- agile-studio-l3
- mvp-builder-l3
- impeccable-l3
- trellis-mindfold-l3 ← **2026-05-01 新規**

### ワークフローエンジン
- n8n-l3
- n8n-as-code-l3
- inngest-l3
- trigger-dev-l3
- gh-aw-agentic-workflows-l3

### MCP・CLIツール
- mcp-servers-l3
- mcp2cli-l3
- officecli-l3
- rtk-l3
- markitdown-l3
- skillui-l3
- graphify-l3
- playwright-cli-l3
- gh-cli (旧形式 → other枠)
- stripe-cli (旧形式 → other枠)
- gws-cli (Google Workspace CLI、旧形式 → other枠)
- ui (shadcn-ui、旧形式 → other枠)

### Web/コンテンツ収集
- crawl4ai-l3
- firecrawl-l3
- browser-use-l3
- ffmpeg-l3
- notebooklm-cli-full-l3

### RAG・ナレッジ管理
- rag-anything-l3
- deeptutor-l3
- flowise-l3

### 仮想通貨・取引
- ccxt-l3
- freqtrade-l3

### スマートコントラクト・Web3
- foundry-l3
- openzeppelin-contracts-l3
- virtual-protocol-org-l3
- virtuals-game-framework-l3

### 音声・リアルタイム通信
- pipecat-l3
- livekit-agents-l3
- voxcpm-openbmb-l3 ← **2026-05-01 新規**

### 画像生成・ComfyUI
- comfyui-api-server-l3
- comfyui-graph-execution-l3

### SNS・SaaS API
- tweepy-l3
- instagrapi-l3

### テスト
- vitest-l3

### スキル: 公式Anthropic
- skill-docx-l3
- skill-pdf-l3
- skill-pdf-reading-l3
- skill-pptx-l3
- skill-xlsx-l3
- skill-frontend-design-l3
- skill-file-reading-l3
- skill-product-self-knowledge-l3
- skill-creator-l3

### スキル: コミュニティ
- skill-deep-research-l3
- skill-content-cascade-l3
- skill-yt-pipeline-l3
- skill-hooks-kallaway-l3
- skill-site-teardown-l3
- skill-dream-l3
- skill-page-cro-l3
- skill-ai-seo-l3
- skill-optimization-methods-l3
- sns-writing-rules-l3
- taste-skill-l3
- five-whys-skill-l3
- pm-skills-deanpeters-l3
- prd-skill-johnnychauvet-l3

### その他
- art-openpipe-l3（Agent Reinforcement Trainer）
- anthropic-cookbook-l3

### LightRAG関連
- (lightrag 旧形式 → other枠)

---

## L2: 検証済みパターン（18件）

| # | ファイル名 | 主要用途 |
|---|---|---|
| 1 | skill-design-patterns-l2 | スキル設計アーキタイプ |
| 2 | gsd-spec-driven-dev-l2 | スペック駆動開発 |
| 3 | superpowers-full-l2 | エージェント開発フレームワーク |
| 4 | superpowers-workflow-l2 | エージェント開発ワークフロー |
| 5 | claude-code-agent-teams-parallel-dev-l2 | git worktree並列開発 |
| 6 | multi-agent-design-patterns-l2 | LangGraph/CrewAI/Mastra使い分け |
| 7 | rag-pipeline-patterns-l2 | RAGパイプライン構築 |
| 8 | rag-application-design-patterns-l2 | RAGアプリ設計（dual-loop） |
| 9 | multi-tenant-saas-design-pattern-l2 | Supabase RLS マルチテナント |
| 10 | durable-execution-hitl-approval-l2 | Inngest HITLワークフロー |
| 11 | n8n-workflow-design-patterns-l2 | n8nワークフロー設計 |
| 12 | n8n-to-webapp-migration-pattern-l2 | n8n→Webアプリ移行判断 |
| 13 | ai-document-generation-pipeline-l2 | AI文書生成4段階アーキ |
| 14 | auto-design-scout-l2 | 競合デザイン自動偵察 |
| 15 | competitive-intelligence-pipeline-l2 | 全方位競合偵察 |
| 16 | creative-ideation-lens-l2 | クリエイティブ評価レンズ |
| 17 | systematic-debugging-l2 | 4段階デバッグ手法 |
| 18 | adr-templates-l2 | Architecture Decision Records |

---

## L2c: 候補パターン（19件、未検証）

| # | ファイル名 | 由来 | 検証状態 |
|---|---|---|---|
| 1 | agent-routing-l2c | openclaude | 未検証 |
| 2 | tool-loop-mcp-l2c | openclaude | 未検証 |
| 3 | openai-compat-abstraction-l2c | openclaude | 未検証 |
| 4 | text-first-on-demand-visuals-l2c | video-use/browser-use | 未検証 |
| 5 | llm-token-reduction-proxy-l2c | rtk | 未検証 |
| 6 | schema-driven-lazy-cli-l2c | mcp2cli | 未検証 |
| 7 | trinity-council-deliberation-l2c | OpenClaw | L1から昇格 |
| 8 | n8n-self-improving-workflow-agent-l2c | SNS Autopilot | L1から昇格 |
| 9 | claude-md-driven-content-generation-l2c | git-art | L1から昇格 |
| 10 | acp-agent-commerce-protocol-l2c | Virtual Protocol | 未検証 |
| 11 | agentic-os-design-pattern-l2c | Agent OS | 未検証 |
| 12 | agentic-saas-boilerplate-l2c | OSS reference arch | 未検証 |
| 13 | claude-obsidian-wiki-pattern-l2c | Karpathy Wiki | 未検証 |
| 14 | claude-skill-manager-design-patterns-l2c | スキルマネージャ4類型 | 未検証 |
| 15 | instinct-based-continuous-learning-l2c | hooks-driven学習 | 未検証 |
| 16 | llm-council-pattern-l2c | Karpathy LLM Council | 未検証 |
| 17 | miniclaw-sandbox-pattern-l2c | サンドボックス4層防御 | 未検証 |
| 18 | multi-tool-skills-sharing-l2c | symlink統一供給 | 未検証 |
| 19 | rag-retrieval-quality-l2c | ノイズ・位置・数の3因子 | 未検証 |

---

## L1-Infra（1件）

| ファイル名 | 内容 |
|---|---|
| dev-environment-workflow-v2-l1-infra | 開発環境前提・ワークフローv2 |

## L1-Ops（2件）

| ファイル名 | 内容 |
|---|---|
| lightrag-infra-ops-l1-ops | LightRAGインフラ運用ログ |
| lightrag-knowledge-ops-l1-ops | LightRAGナレッジ管理運用知見 |

## L1-old（1件、リネーム検討）

| ファイル名 | 推奨アクション |
|---|---|
| awesome-agent-skills-l1 | L3にリネーム検討（カタログ系コンテンツ） |

---

## other: 旧形式（13件、リネーム対象）

ファイル名にレイヤーサフィックスがない旧形式。中身はL2/L3品質。次セッションでリネーム再投入を計画。

### L3にリネーム予定（10件）
| 現ファイル名 | 推奨新ファイル名 | 内容 |
|---|---|---|
| ai_lightrag.txt | vercel-ai-sdk-l3 | Vercel AI SDK |
| awesome-design-md_lightrag.txt | awesome-design-md-l3 | デザインシステム |
| codex-plugin-cc_lightrag.txt | codex-plugin-cc-l3 | OpenAI Codex × CC連携 |
| gh-cli_lightrag.txt | gh-cli-l3 | GitHub CLI |
| gws-cli_lightrag.txt | google-workspace-cli-l3 | Google Workspace CLI（Rust） |
| lightrag_lightrag.txt | lightrag-l3 | LightRAG本体 |
| motion_lightrag.txt | motion-framer-l3 | Reactアニメーション |
| stripe-cli_lightrag.txt | stripe-cli-l3 | Stripe CLI |
| ui_lightrag.txt | shadcn-ui-l3 | shadcn/ui |
| obsidian-skills_lightrag.txt | obsidian-skills-l3 | Obsidian × Agent Skills |
| agency-agents_lightrag.txt | agency-agents-l3 | エージェント初期設定参考 |

### L2にリネーム予定（2件）
| 現ファイル名 | 推奨新ファイル名 | 内容 |
|---|---|---|
| awesome-compose_lightrag.txt | awesome-compose-l2 | Docker Composeリファレンス |
| building-llm_lightrag.txt | building-llm-applications-l2 | Building LLM-Powered Apps |

> 注: ⚠️ リネームには「旧版psql削除 + 新ファイル名で再upload_document」の手順が必要。次セッションで計画的に実施。

---

## 目標達成度（2026-05-01）

| 指標 | 現状 | 目標 | 達成率 |
|---|---|---|---|
| L3比率 | 65.6% | 50-60% | 超過 |
| L2比率 | 11.5% | 20-25% | 50% |
| L2c件数 | 19 | - | 順調 |
| 旧形式件数 | 14 | 0 | 撲滅必要 |
| エラー件数 | 0 | 0 | ✅達成 |
| doc整合性 | 157=157 | 一致 | ✅達成 |

---

## セッション履歴

### 2026-05-01: 整理・再棚卸し
- doc_fullゴースト21件削除（chunks 71件 + vdb_chunks 71件巻き込み）
- 全157件のレイヤー別棚卸し実施
- 新規L3投入2件: trellis-mindfold-l3, voxcpm-openbmb-l3
- 見送り判断1件: docker-android (budtmo)
- INDEX.md / RESUME.md / GSD-PLAN.md / DECISIONS.md を157件状態に同期更新
- 旧形式13件のリネーム計画を明文化

### 2026-04-19: Phase 3 無サフィックス再投入
- Phase 1a 重複24件削除
- バッチ1-3で計13件再投入、26件純減
- vdb_entities 約800件のノイズ除去
- 検索精度向上を6テストクエリで確認

### 2026-04-18: L1 v3再設計 + L2c拡充
- L1から10件削除（プロジェクト固有情報を全除外）
- L1維持3件をL1-Infra/L1-Opsにリネーム（計227レコードUPDATE）
- L2cを9件に拡充
- KNOWLEDGE-DECISIONS.md新設

### 2026-04-17
- openclaude-l3新規投入
- L2c候補3パターン記録（Agent Routing / Tool-loop+MCP / OpenAI互換抽象化）

### 2026-04-15
- Phase 1-3 大規模リファクタリング
- combination-architect / knowledge-navigator スキル3レイヤー化

---

## 次のアクション（2026-05-01時点）

1. **OpenRouter APIキーローテーション**（最優先・セキュリティ）
2. **旧形式13件のリネーム再投入**（other 13件、計画は本INDEX.md記載）
3. **L1-old 1件のリネーム**（awesome-agent-skills-l1 → l3化検討）
4. **entity_chunks/relation_chunks のゴースト要素クリーンアップ**（LightRAG公式手順調査が必要）
5. **L2c → L2 昇格候補の検証**（実装による検証実施）
6. **L2拡充**（現18件 → 目標25件）
7. **検索モード使い分け指針の明文化**（hybrid/local/global/naive）
8. **2段階クエリ戦略のスキル化**（用途③発信用途向け）

---

## 運用ルール（再確認用）

### 投入経路
- 本体ナレッジ: Claude.ai（LightRAGプロジェクト）→ upload_document のみ
- 管理ファイル: VPS上で直接編集（INDEX/DECISIONS/RESUME/SCHEMA）

### ファイル名規約
- L3: `[name]-[author]-l3_lightrag.txt`
- L2: `[name]-l2_lightrag.txt`
- L2c: `[name]-l2c_lightrag.txt`
- L1-Infra: `[name]-l1-infra_lightrag.txt`
- L1-Ops: `[name]-l1-ops_lightrag.txt`

### 削除原則
- DELETE API禁止（全消しバグ）
- psql直接操作 + 必ずpg_dumpバックアップ
- BEGIN/ROLLBACK でドライラン → COMMIT で本番

### 投入評価
- 新規リソース評価時は必ず KNOWLEDGE-DECISIONS.md に記録
- 4カテゴリ: L3投入 / L2c投入 / 保留 / 見送り
