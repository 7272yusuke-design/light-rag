# KNOWLEDGE-DECISIONS.md

## このドキュメントについて

リポジトリ/ツール/パターンの投入判断ログ。L3投入・L2c投入・保留・見送りの全判断を記録する。

再評価時は必ずこのログを参照し、重複判断を避ける。新規評価時は末尾に追記。

### 判断カテゴリ（DATA-SCHEMA.md準拠）

| カテゴリ | 意味 |
|---|---|
| L3投入 | 実装ナレッジとして蓄積（LightRAG本体へupload_document済み） |
| L2c投入 | 候補パターンとして蓄積（LightRAG本体へupload_document済み） |
| L2c候補 | DECISIONSに記録のみ、LightRAG本体未投入（要投入） |
| 保留 | 領域は合うが時期尚早 |
| 見送り | 現在のビジネス領域から外れる |

### 再検討条件の書き方

- ❌ 漠然（「案件時」「実装時」）
- ✅ 具体ビジネスイベント（「OpenClaw本格化時」「電子署名案件受注時」）

---

## 判断ログ

### 2026-04-17

#### openclaude
- **判断**: L3投入
- **出典URL**: https://github.com/Gitlawb/openclaude
- **理由**: マルチプロバイダーCoding Agent CLI、21k stars、Yusukeさんのn8n自動化・エージェント開発・LLMコスト最適化ニーズに直撃。Agent Routing / Tool-loop+MCP / OpenAI互換抽象化の3パターンが学べる。
- **注意事項**: Claude Code派生・商標グレー、v0.2.x系で若いためAPI安定性低い可能性あり
- **ファイル名**: openclaude-l3_lightrag.txt
- **再検討条件**: —
- **関連L2c候補**: Agent Routing / Tool-loop+MCP / OpenAI互換API抽象化

#### rtk
- **判断**: L3投入 + L2c候補（本体未投入）
- **出典URL**: （前回セッションで記載済み、別途確認）
- **理由**: LLMトークン削減プロキシ、OpenClaw公式プラグインあり、Yusukeさん事業に直結
- **ファイル名**: rtk-l3_lightrag.txt
- **再検討条件**: 自環境にrtkを導入・動作確認後、L2c→L2昇格
- **昇格トリガー**: 自環境rtk導入完了時

#### Documenso
- **判断**: 見送り
- **出典URL**: https://github.com/documenso/documenso
- **理由**: 電子署名OSS（12.6k stars、高品質）だが、ドメインが狭く現在の主軸（n8n/エージェント/OpenClaw）と距離がある。tRPC+Prisma+ReactRouter構成は参考になるが、同目的ならcreate-t3-app等のほうが汎用性高い
- **再検討条件**: 電子署名機能を含む顧客案件を受注したとき

#### MiniCode
- **判断**: 保留
- **出典URL**: （前回セッションで記載済み）
- **理由**: Coding Agent学習用。openclaudeと機能が重複するため、openclaudeを優先
- **再検討条件**: 自前Coding Agentを実装する段階に進んだとき（openclaudeで物足りなさを感じた時点）

#### video-use
- **判断**: L2c候補（本体未投入）
- **出典URL**: https://github.com/browser-use/video-use
- **理由**: browser-use公式、68 stars開発初期。設計パターン「Text-first + On-demand visuals」に価値あり（大きなメディアをLLMに扱わせる設計）。browser-use L2投入済みのため類似パターンとして記録
- **抽出候補パターン名**: Text-first + On-demand visuals パターン
- **再検討条件**: 動画編集自動化案件受注時、または自プロジェクトで大規模データ（動画・長文・巨大DOM）をLLMに扱わせる設計を実装するとき

#### JeecgBoot
- **判断**: 見送り
- **出典URL**: （前回セッションで記載済み）
- **理由**: 45.4k stars巨大Java/SpringBoot低代码プラットフォーム。Yusukeさんの技術スタック（TypeScript/Python中心）と言語が合わず、ドメインも企業向け低代码と距離がある
- **再検討条件**: Javaエンタープライズ案件を受注したとき、または業界別Skill戦略の検討に着手したとき

#### Agent Lightning
- **判断**: 保留
- **出典URL**: （前回セッションで記載済み、Microsoft公式）
- **理由**: Microsoft公式、14.1k stars、任意エージェントのRL/APO訓練フレームワーク。現フェーズは「まだ作る段階」で訓練・最適化は次段階
- **再検討条件**: OpenClaw運用開始時、またはエージェント訓練フェーズに着手するとき

---

## 統計

- L3投入: 3件（openclaude, rtk, mcp2cli）
- L2c投入: 6件（5パターン本体投入済 + schema-driven-lazy-cli）
- 保留: 3件（MiniCode, Agent Lightning, smolvm）
- 見送り: 2件（Documenso, JeecgBoot）

**合計**: 9件の評価実績

---

## 次のアクション

1. rtk・video-useのL2c本体投入（LightRAGへupload_document）
2. 未確認のURL（rtk, MiniCode, JeecgBoot, Agent Lightning）を次セッションで補完
3. 新規リソース評価時は本ドキュメント末尾に追記

---

### 2026-04-18

#### L2c本体投入: 5パターン一括

**投入ファイル**:
- agent-routing-l2c_lightrag.txt
- tool-loop-mcp-l2c_lightrag.txt
- openai-compat-abstraction-l2c_lightrag.txt
- text-first-on-demand-visuals-l2c_lightrag.txt
- llm-token-reduction-proxy-l2c_lightrag.txt

**判断**: L2c投入（DATA-SCHEMA.md v2ルール下で初のL2c本体投入）

**経緯**:
- 2026-04-17時点ではKNOWLEDGE-INDEX.mdの「L2抽出候補」セクションにのみ記載されていた
- 2026-04-18のDATA-SCHEMA.md v2でL2cレイヤーが正式化され、LightRAG本体への投入が可能に
- 各パターンはopenclaude/video-use/browser-use/rtkのL3読解ベース

**昇格条件**（個別）:
- Agent Routing: Yusukeさんがn8n案件またはOpenClawで実装しコスト削減効果測定完了時
- Tool-loop+MCP: 自前Coding Agent実装時、またはOpenClawでMCP化した取引操作を1週間安定運用時
- OpenAI互換抽象化: 実案件で2プロバイダー以上の切替を実装し同じアプリが両方で動作確認時
- Text-first+On-demand visuals: 動画編集/Webスクレイピング/PDF処理のいずれかで素朴実装比70%以上のトークン削減を測定時
- LLMトークン削減プロキシ: rtkをClaude Code/OpenClaw環境に1週間以上運用してトークン削減率を実測時

**rtk URL判明**: https://github.com/rtk-ai/rtk（DECISIONS.md上の2026-04-17 rtkエントリのURL補完）

---

### 2026-04-18（追加評価）

#### mcp2cli
- **判断**: L3投入
- **出典URL**: https://github.com/knowsuchagency/mcp2cli
- **理由**: MCPサーバー/OpenAPIを実行時にCLIに変換、コード生成なし。LightRAG MCP（https://mcp.7272yusuke.cloud/mcp）をClaude Codeからbash経由で呼べる最短経路。トークン削減96-99%実測値あり（入力側スキーマ注入の削減）。n8n案件・Yusukeさん事業に直撃。
- **ファイル名**: mcp2cli-l3_lightrag.txt
- **注意事項**: 4 stars、30 commits、開発初期。API破壊的変更リスクあり。評価フェーズから始めて本番依存は避ける
- **再検討条件**: —
- **関連L2c**: schema-driven-lazy-cli-l2c（同時投入）

#### Schema-driven Lazy CLI パターン（L2c）
- **判断**: L2c投入
- **出典**: mcp2cli（L3投入）, CLIHub（Kagan Yilmaz記事）, Anthropic Tool Search
- **理由**: mcp2cliから抽出した「入力側（スキーマ）トークン削減」パターン。rtkの「出力側削減」と対をなす。複数実装（mcp2cli/CLIHub/Anthropic Tool Search）が存在する成熟概念のため、パターン単独の価値も高い
- **ファイル名**: schema-driven-lazy-cli-l2c_lightrag.txt
- **抽出候補パターン名**: Schema-driven CLI + Lazy Tool Discovery
- **再検討条件（昇格条件）**: Yusukeさんが自環境でmcp2cliを導入しLightRAG MCPをClaude Codeから1週間以上運用、もしくはn8n案件で顧客OpenAPIに対してmcp2cli相当を導入しトークン削減率を実測

#### smolvm
- **判断**: 保留
- **出典URL**: https://github.com/smol-machines/smolvm
- **理由**: microVMをローカル実行する軽量ツール（<250msブート、libkrun+Hypervisor.framework/KVM）。領域は将来合う（Coding Agent安全実行、OpenClaw本番運用）が、現フェーズ（Claude Code導入初期・n8n→アプリ開発アップセル検討中）では早すぎる。HostingerのVPSで/dev/kvmが使えるかも未確認。22 stars、Alpha段階（v0.1.7）で破壊的変更リスク大
- **再検討条件**: OpenClaw本番運用着手時、または顧客向けCoding Agentサービス提供を開始するとき（セキュリティ層強化が必要になる段階）


---

### 2026-04-18（L1 v3再設計）

L1 v3ルール導入（DATA-SCHEMA.md）に伴い、プロジェクト固有情報をLightRAGから除外。汎用化可能なパターンはL2cへ昇格させた上で、元L1を削除。

#### L2c昇格 3パターン

##### TrinityCouncil 3エージェント議論型合意形成 パターン
- 判断: L2c投入
- ファイル名: trinity-council-deliberation-l2c_lightrag.txt
- 抽出元: neo-openclaw-project-l1（削除）
- 理由: Bull/Bear/Sage 3エージェントの対立構造による合意形成は、既存 multi-agent-design-patterns-l2（Supervisor型中心）とは独立した汎用パターン。トレーディング以外にも投資判断、コンテンツ戦略、プロダクトレビューに転用可能
- 再検討条件（昇格条件）: OpenClaw本番運用開始時に paper-trading 1週間以上で効果測定、または顧客案件で戦略判断支援ツールに組み込み実測

##### n8n Cron駆動 自己改善ワークフローエージェント パターン
- 判断: L2c投入
- ファイル名: n8n-self-improving-workflow-agent-l2c_lightrag.txt
- 抽出元: sns-autopilot-project-l1（削除）
- 理由: Workflow Evolver Agent構想は、顧客向けn8n案件のアップセル材料として差別化要素あり。納品後も自動改善されるn8nワークフローは既存 n8n-workflow-design-patterns-l2 の上位レイヤー
- 再検討条件（昇格条件）: Yusukeさんの顧客案件でEvaluator Agent相当を導入し1ヶ月以上運用、またはSNS Autopilot復活時にWorkflow Evolverを本番実装

##### CLAUDE.md駆動のコンテンツ自動生成 パターン
- 判断: L2c投入
- ファイル名: claude-md-driven-content-generation-l2c_lightrag.txt
- 抽出元: git-art-workflow-l1 + github-actions-article-patterns-l1（両方削除、統合）
- 理由: Markdownだけで指示するコンテンツパイプラインは、note記事以外にも顧客ドキュメント自動化・社内Wiki自動更新に転用可能。「顧客自身が改修できる自動化」として差別化
- 再検討条件（昇格条件）: Yusukeさんがgit-art相当をセットアップし1ヶ月以上運用、または顧客案件でドキュメント自動生成を導入

#### L1削除 10件

L1 v3ルール適用により、プロジェクト固有情報・低優先プロジェクト・重複ドキュメントを削除。削除前にpg_dump取得（pg_backup_20260418_1226.sql）。psql経由で計6テーブル・計531レコードを削除。

| 削除ファイル | 削除理由 |
|---|---|
| neo-openclaw-project-l1 | プロジェクト固有、TrinityCoundilをL2c抽出済み |
| openclaw-project-l1 | 削除時点で既に不在（過去の重複残骸） |
| jizokuka-ai-project-l1 | 既存 n8n-to-webapp-migration-pattern-l2 でカバー済み |
| sns-autopilot-project-l1 | プロジェクト固有、Workflow EvolverをL2c抽出済み |
| secretary-agent-platform-l1 | 既存L2群（durable-execution-hitl / multi-tenant-saas / ai-document-generation）でカバー済み |
| note-claudecode-monetization-pipeline-l1 | note.com低優先、プロジェクト固有 |
| kiyobin-persona-l1 | ペルソナ情報はClaude.aiプロジェクト側で管理 |
| note-autopost-requirements-l1 | note.com低優先、重複の疑い |
| masterclass-curriculum-l1 | note記事戦略用、低優先 |
| git-art-workflow-l1 | CLAUDE.md駆動コンテンツ生成をL2c抽出済み |
| github-actions-article-patterns-l1 | 同上、L2c統合先 |

注記: 当初19件想定で計画したが、実在確認により10件のみ削除実行。残り9件は既に不在（entity残骸のみLightRAG側に残存、検索実害はないため別タスクで整理予定）。

#### L1リネーム 3件（L1-Infra / L1-Ops化）

DATA-SCHEMA.md v3のサブタイプ規約に沿ってfile_pathをUPDATE（計227レコード）。ドキュメント本体・ベクトル・エンティティは保持したまま、file_pathカラムのみ変更。

| 旧ファイル名 | 新ファイル名 | サブタイプ |
|---|---|---|
| dev-environment-workflow-v2-l1 | dev-environment-workflow-v2-l1-infra | L1-Infra |
| lightrag-infra-ops-log-l1 | lightrag-infra-ops-l1-ops | L1-Ops |
| lightrag-knowledge-ops-l1 | lightrag-knowledge-ops-l1-ops | L1-Ops |


---

## 2026-04-19 — Phase 3（無サフィックス・重複ナレッジの再投入・削除）

### 背景・目的
用途①（設計書出力）②（開発支援）③（情報発信）の精度評価で、以下の問題が判明した:
- 「crewai」検索でcrewai本体がヒットせず、crawl4aiが誤優先される
- skill-creator が 3ファイル重複
- 旧形式（サフィックスなし）ナレッジ群がエンティティ汚染（Tokyo / Gmail / Slack等の周辺語が混入）
- エンティティ純度の低下が検索精度を下げていた

### 真因（エンティティ構造調査で判明）
- `lightrag_full_entities` は 1ドキュメント1レコード、`entity_names` は JSONB 配列
- 旧形式ナレッジ（Repomix等で丸ごと投入したもの）は、サンプルコード内の周辺語までエンティティ化されていた
- L3テンプレートに沿って再投入すると、**固有名詞に絞られたエンティティ**が生成され、検索精度が上がる

### 実施サマリ
- 削除: 39件
- 再投入（L3品質）: 13件
- 純減: **26件**（149→123）
- vdb_entities: ~6000→5200（ノイズ除去約800件）

### Phase 1a: 確実な重複24件削除
skill系の旧版・v2版 × 18件、プロジェクト進捗系 × 2件、旧孤児系 × 4件。

| 削除ファイル | 削除理由 |
|---|---|
| skill-skill-creator_lightrag.txt | skill-creator-l3の旧版 |
| skill-skill-creator-v2_lightrag.txt | 同上 |
| skill-docx_lightrag.txt / skill-docx-v2_lightrag.txt | skill-docx-l3の旧版 |
| skill-file-reading_lightrag.txt / -v2 | skill-file-reading-l3の旧版 |
| skill-frontend-design_lightrag.txt / -v2 | skill-frontend-design-l3の旧版 |
| skill-pdf_lightrag.txt / -v2 | skill-pdf-l3の旧版 |
| skill-pdf-reading_lightrag.txt / -v2 | skill-pdf-reading-l3の旧版 |
| skill-pptx_lightrag.txt / -v2 | skill-pptx-l3の旧版 |
| skill-product-self-knowledge_lightrag.txt / -v2 | skill-product-self-knowledge-l3の旧版 |
| skill-xlsx_lightrag.txt / -v2 | skill-xlsx-l3の旧版 |
| graphify_lightrag.txt | graphify-l3の旧版 |
| playwright-cli_lightrag.txt | playwright-cli-l3の旧版 |
| secretary-agent-p1-progress.txt | プロジェクト進捗、Claude.ai側で管理 |
| secretary-agent-p1-spec.txt | プロジェクト仕様、Claude.ai側で管理 |
| test-upload.txt | テストファイル |
| openclaw_lightrag.txt | openclaw-project-l1の旧版残骸 |

### crewai単独再投入（検証）
| 処理 | ファイル |
|---|---|
| 削除 | crewai_lightrag.txt（103エンティティ、うち汚染多数） |
| 再投入 | crewai-l3_lightrag.txt（L3テンプレート準拠） |

検証結果: 「crewai エージェント オーケストレーション」検索で筆頭ヒット。用途①で設計書素材として使える品質に。

### バッチ1: マルチエージェント3件（削除→再投入）
| 旧 | 新 | 備考 |
|---|---|---|
| langgraph_lightrag.txt | langgraph-l3_lightrag.txt | StateGraph/Checkpointer/HITL詳細化 |
| mastra_lightrag.txt | mastra-l3_lightrag.txt | v1.0リリース情報、Apache 2.0、22k+ Stars反映 |
| n8n_lightrag.txt | n8n-l3_lightrag.txt | 70+AIノード、LangChain統合、500+統合詳細化 |

検証結果: n8n筆頭、LangGraph/CrewAI/Mastraが関連検索で揃う（設計判断時の比較候補が揃う）。

### バッチ2: Web/スクレイピング/SDK 4件削除→3件再投入
| 旧 | 処理 | 判断理由 |
|---|---|---|
| firecrawl_lightrag.txt | → firecrawl-l3_lightrag.txt | 110k+ Stars、MCP Server・Claude Codeプラグイン反映 |
| browser-use_lightrag.txt | → browser-use-l3_lightrag.txt | 28.8k+ Stars、10+LLMプロバイダー対応 |
| ffmpeg_lightrag.txt | → ffmpeg-l3_lightrag.txt | Remotion/ComfyUI連携、n8n統合パターン詳細化 |
| llmfit_lightrag.txt | **削除のみ** | 用途不明、検索ヒットなし、事業との関連度低 |

### バッチ3: 最終7件削除→6件再投入
| 旧 | 処理 | 判断理由 |
|---|---|---|
| anthropic-cookbook_lightrag.txt | → anthropic-cookbook-l3_lightrag.txt | Claude API公式レシピ、最重要参照ナレッジ |
| ccxt_lightrag.txt | → ccxt-l3_lightrag.txt | OpenClaw取引エージェントの基盤 |
| freqtrade_lightrag.txt | → freqtrade-l3_lightrag.txt | OpenClaw比較対象、バックテストエンジン |
| n8n-as-code_lightrag.txt | → n8n-as-code-l3_lightrag.txt | GitOps統合、OpenClaw連携明示 |
| supabase_lightrag.txt | → supabase-l3_lightrag.txt | マルチテナントSaaS・pgvector基盤 |
| vercel_lightrag.txt | → vercel-l3_lightrag.txt | Vercel AI SDK（TypeScript抽象化） |
| nemo-agent-toolkit_lightrag.txt | **削除のみ** | NVIDIA GPU前提、現スタック未適合、既存CrewAI/LangGraph/Mastraで代替可 |

### 方法論：安全な削除手順
1. バックアップ取得（pg_dump → `/docker/lightrag/backups/pre-cleanup-*.sql`）
2. 削除対象IDを psql で確認
3. `BEGIN; ... ROLLBACK;` でドライラン実行、件数確認
4. ROLLBACK を COMMIT に置換して本番実行
5. ベースラインエンティティ件数で影響範囲を測定（LangChain/Python/TypeScript/OpenAI/Claude）
6. 再投入後は `status = processed` を確認

### 影響範囲の測定結果（共有エンティティの保護）
削除前後で主要エンティティ件数に有意な減少なし:
- LangChain: 4 → 4（維持）
- TypeScript: 8 → 8（維持）
- OpenAI: 25 → 24（-1、軽微）
- Python: 23 → 22（-1、軽微）
- Claude: 94 → 92（-2、軽微）

→ `file_path LIKE '%xxx_lightrag.txt%'` パターンは実害なし。

### 検証結果（用途①②③への適合性）
| 検証クエリ | 結果 |
|---|---|
| 「crewai エージェント オーケストレーション」 | crewai-l3筆頭、設計書素材OK |
| 「マルチエージェント取引判断」 | TrinityCouncil + LangGraph + openclaude揃う |
| 「仮想通貨 取引 バックテスト 戦略」 | CCXT + Freqtrade + TrinityCouncil揃う（OpenClaw開発即可能） |
| 「next.js supabase saas マルチテナント」 | Supabase筆頭 + Next.js + RAG設計 + マルチテナント設計パターン揃う |
| 「anthropic cookbook claude api パターン」 | 公式パターン + Yusuke事業との接続リレーション抽出 |

### 学び・運用ルール追加
1. **エンティティ純度がRAG検索精度を決める**。サンプルコード丸投げは避け、L3テンプレートで整理投入する
2. **短い固有名詞（4-8文字）での検索は埋め込みベクトルの限界**に当たる（crewai vs crawl4aiの文字列類似問題）。**文脈語を加えた複合クエリが実用上必要**
3. **用途別クエリ戦略**: 用途③（情報発信）では「題材検索」と「発信型検索」を2段階に分けるべき（次タスクでスキル化予定）

### 残タスク（Phase 3後）
1. [ ] 検索モード使い分け指針の明文化（Step 3、本ファイル/DATA-SCHEMA.mdに追記）
2. [ ] 2段階クエリ戦略のスキル化（Step 4、article-architect 類似の発信用スキル設計）
3. [ ] 残ファイル名不整合の点検（_lightrag.txt と -l3_lightrag.txt の混在が解消されたか）
4. [ ] KNOWLEDGE-INDEX.md の詳細一覧を再棚卸し（v3 Phase 3 後反映）

---

# 2026-05-01 セッション: 整理・棚卸し

## 1. 新規L3投入: Trellis (mindfold-ai)
- **カテゴリ**: L3投入
- **リポジトリ**: https://github.com/mindfold-ai/Trellis
- **ファイル**: trellis-mindfold-l3_lightrag.txt
- **判断理由**: マルチプラットフォーム（14ツール: Claude Code/Cursor/OpenCode/Codex/Gemini CLI/GitHub Copilot/Windsurf 等）AIコーディングフレームワーク。spec/tasks/workspaceの3層で規約・タスク・ジャーナルを管理。superpowers/gsd/agent-teams/gstack等の既存ナレッジと領域は重なるが、「ツール横断統合」という独自軸はカバーされていなかった。スター6.2k、AGPL-3.0、現役更新中（v0.4.0が最新）。
- **L2昇格条件**: 
  - 実プロジェクト導入で効果検証
  - n8nコンサルクライアントへの提案実績
  - multi-tool-skills-sharing-l2cとの統合体系化

## 2. 新規L3投入: VoxCPM (OpenBMB)
- **カテゴリ**: L3投入
- **リポジトリ**: https://github.com/OpenBMB/VoxCPM
- **ファイル**: voxcpm-openbmb-l3_lightrag.txt
- **判断理由**: 30言語対応・48kHz・Apache-2.0商用OKのTokenizer-Free TTSモデル。Voice Design（記述だけで声を作る）/ Controllable Cloning / Ultimate Cloning の3モード対応。既存ナレッジ（pipecat/livekit-agents/ffmpeg/yt-pipeline/note-claudecode-monetization-pipeline）との連携シナリオが豊富。OpenClawの音声化、note.com→YouTube自動化、n8nコンサル提案材料として高い価値。スター13.5k、ModelBest/THUHCSI開発、MiniCPM-4ベース。
- **L2昇格条件**:
  - 実パイプライン組込（note→音声→YouTube）
  - VoicePOC実装成立
  - n8n商用提案成約
  - LoRA企業ブランドボイス構築の体系化

## 3. 見送り: docker-android (budtmo)
- **カテゴリ**: 見送り
- **リポジトリ**: https://github.com/budtmo/docker-android
- **判断理由**: noVNC対応Androidエミュレータ in Docker。Yusukeのn8n/エージェント主軸の事業領域とモバイルアプリテストの直接的接点が薄い。Hostinger VPSのKVM対応も不明。具体的な案件発生時に再評価でナレッジ膨張を防ぐ。スター14.3k、Ubuntu OS必須・KVM仮想化必須。
- **再評価条件**:
  - クライアントからモバイルアプリのE2Eテスト/CI環境構築の相談が来た場合
  - Yusuke自身がモバイルアプリ開発に着手した場合

## 4. クリーンアップ: doc_fullゴースト21件削除
- **カテゴリ**: クリーンアップ実施
- **背景**: 2026-04-19 Phase 3 cleanup 後、doc_full(178) vs doc_status(157)で21件の乖離が残存。検索ノイズ源として認識されつつ次セッション送りになっていた積み残しタスク。
- **削除対象（21件のゴーストドキュメント）**:
  - 過去削除済みリポジトリ系（11件）: OpenSpace, ComfyUI-to-Python-Extension, comfyui-api-wrapper, comfy_api_simplified, n8n-mcp, ruflo, claude-peers-mcp, CLI-Anything, servers, autoresearch, notebooklm-py(古い版)
  - L1削除残存系（10件）: git-art, note.com自動投稿, note.com Claude Code記事収益化, きよびん, OpenClaw, Masterclass, GitHub Actions記事生成, 開発環境ワークフロー, career-ops, notebooklm-py(旧版)
- **削除内訳**:
  - lightrag_vdb_chunks_nomic_embed_text_768d: 71件
  - lightrag_doc_chunks: 71件
  - lightrag_doc_full: 21件
- **手順**: pg_dump → ドライラン(BEGIN+ROLLBACK)で件数確認 → 本番実行(BEGIN+COMMIT) → 整合性確認(doc_full=doc_status=157)
- **バックアップ**: /docker/lightrag/backups/pre-reinventory-20260501-011545.sql (251MB)
- **検索精度への期待効果**: ゴーストチャンクが検索ヒットしなくなり、無効リンクのノイズが除去される
- **積み残し**: entity_chunks/relation_chunks のゴーストID配列要素クリーンアップは未実施（LightRAG公式手順の調査が必要なため、別セッションで実施）

## 5. 整理セッションでの発見
- 実際のナレッジ数 = **157件**（メモリ記録/INDEX.md記録の104〜123件から大幅増加）
- L3が48→103件に倍増、L2cが9→19件に倍増
- INDEX.md / RESUME.md / GSD-PLAN.md の3ファイルが**全て古い**状態だったため、これを機に同期更新する

---

## 2026-06-01: Qdrant — L3投入

- **対象:** qdrant/qdrant（https://github.com/qdrant/qdrant、Apache-2.0、31.4k★、v1.18.0）
- **判断:** L3投入（qdrant-l3_lightrag.txt、2451 bytes）
- **種別:** vector-database / vector-search-engine
- **重複チェック:** Qdrant専用エントリなし・競合（Weaviate/Milvus/Chroma）も未投入。本文言及7件（crewai/flowise/mastra/n8n/openllmetry/rowboat/lightrag-framework）はいずれも「対応ベクトルストアの一つ」としての列挙でQdrant主題ではない → 機能的重複なしと判定。
- **投入根拠:** ベクトルDBという技術カテゴリが独立エントリとして存在しなかった。Rust製・高性能・Apache-2.0でL3「部品在庫」定義に合致。加えて公式Agent Skills（qdrant/skills）が量子化/シャーディング/テナント分離/ハイブリッド検索の設計判断をスキル化しており、オリジナルSKILL開発の参考事例としても価値。
- **現時点の位置付け:** LightRAG置き換え対象ではない。検索品質課題はアプリ層（後段キャップ・グラフエッジ）が主因（2026-06-01検証）で、ベクトルエンジン性能の問題ではないため。将来の部品在庫として記録。
- **再検討条件:**
  1. ベクトル検索がLightRAG+pgvectorで性能/スケール頭打ちになった時（数千→数万規模、レイテンシ悪化）
  2. 商品化のマルチテナント設計（Unkey+Supabase RLS）着手時 → 公式Agent Skillsの tenant isolation/sharding 設計を参照
  3. 自前検索にハイブリッド検索の融合戦略（RRF/DBSF）を取り込む検討時 → relationships 5→15 の発展形

---

## 2026-06-01: Qdrant — L3投入

- **対象:** qdrant/qdrant（https://github.com/qdrant/qdrant、Apache-2.0、31.4k★、v1.18.0）
- **判断:** L3投入（qdrant-l3_lightrag.txt、2451 bytes）
- **種別:** vector-database / vector-search-engine
- **重複チェック:** Qdrant専用エントリなし・競合（Weaviate/Milvus/Chroma）も未投入。本文言及7件（crewai/flowise/mastra/n8n/openllmetry/rowboat/lightrag-framework）はいずれも「対応ベクトルストアの一つ」としての列挙でQdrant主題ではない → 機能的重複なしと判定。
- **投入根拠:** ベクトルDBという技術カテゴリが独立エントリとして存在しなかった。Rust製・高性能・Apache-2.0でL3「部品在庫」定義に合致。加えて公式Agent Skills（qdrant/skills）が量子化/シャーディング/テナント分離/ハイブリッド検索の設計判断をスキル化しており、オリジナルSKILL開発の参考事例としても価値。
- **現時点の位置付け:** LightRAG置き換え対象ではない。検索品質課題はアプリ層（後段キャップ・グラフエッジ）が主因（2026-06-01検証）で、ベクトルエンジン性能の問題ではないため。将来の部品在庫として記録。
- **再検討条件:**
  1. ベクトル検索がLightRAG+pgvectorで性能/スケール頭打ちになった時（数千→数万規模、レイテンシ悪化）
  2. 商品化のマルチテナント設計（Unkey+Supabase RLS）着手時 → 公式Agent Skillsの tenant isolation/sharding 設計を参照
  3. 自前検索にハイブリッド検索の融合戦略（RRF/DBSF）を取り込む検討時 → relationships 5→15 の発展形

---

## 2026-06-01: CodeGraph — L3投入（graphify と別エントリ）

- **対象:** colbymchenry/codegraph（https://github.com/colbymchenry/codegraph、MIT、552★、npm @colbymchenry/codegraph）
- **判断:** L3投入（codegraph-l3_lightrag.txt、3200 bytes）
- **種別:** tool / code-intelligence（Claude Code向け事前インデックス型コードナレッジグラフ）
- **重複チェック:** CodeGraph専用エントリなし。同テーマ既存3件: graphify-l3（最近接）/ graphify-mcp2cli-token-reduction-l2c / microsoft-graphrag-l3。
- **判定:** graphify とは「同テーマだが実装スコープが明確に異なる」→ 別エントリ投入 + cross-reference 付与（ルール準拠）。
  - 違い: graphify=Python/PyPI/networkx+Leiden/CLI、CodeGraph=TypeScript/npm/SQLite-FTS5/MCPサーバー統合/impact analysis/19言語/実測92%削減。
- **投入根拠:** Yusukeのフェーズ（Claude Code導入初期、VPS/SSH開発検討中）に直接効く部品。npm/MCP統合でClaude Code環境に組み込みやすい。設計思想（事前グラフ化→走査せず参照）が2026-06-01の relationships 5→15 と同型。
- **再検討条件:**
  1. VPS上でClaude Code本格運用開始時 → 探索トークン削減策として導入検討
  2. 顧客案件で大規模コードベース解析/リファクタリング支援時 → impact analysis が事前リスク評価に有効
  3. 議題2（L2充実）着手時 → graphify+CodeGraph の共通パターンを「事前グラフ化トークン削減」L2c候補として切り出し検討
- **将来検討候補メモ:** 「事前グラフ化によるエージェント探索コスト削減」L2c候補（2実装から帰納、議題2着手時）。

---

## 2026-06-01: AirLLM — 見送り

- **対象:** lyogavin/airllm（https://github.com/lyogavin/airllm、Apache-2.0、18.1k★）
- **判断:** 見送り（投入しない）
- **正体:** GPUのVRAM不足を補う推論技術。モデルをレイヤー単位に分割しディスク保存→推論時に1レイヤーずつGPUにロードして70Bを4GB GPUで動かす。本来GPU(CUDA)前提。
- **見送り理由:**
  1. 環境不一致: Yusuke環境はHostinger KVM2（2vCPU/8GB RAM、GPUなし）。AirLLMが解決する問題（VRAM不足）がGPUなし環境には存在しない。CPUでは構造上むしろ激遅（レイヤーのディスクI/Oが律速）で実用にならない。
  2. 事業接続なし: n8n自動化・エージェント開発の現方針と接続する再検討条件が立てにくい。現状はOpenRouter経由のクラウドClaudeが最適。
  3. 商品化方針（既存ナレッジ磨き込み優先・新規収集最小化）に逆行。
- **再検討条件:** GPU搭載環境を本格的に持つ計画が具体化した時のみ再評価。
- **学習上の代替メモ:** CPUローカルLLMの検証/学習が目的なら、AirLLMではなく llama.cpp + GGUF量子化モデル、または既存Ollamaへの小型モデル追加（ollama pull llama3.2:3b 等）が適切。これらは「CPUローカルLLM運用」テーマとしてL3評価の余地あり（プライバシー重視顧客向け提案材料になりうる）。

---

## 2026-06-01: goose — L3投入

- **対象:** aaif-goose/goose（https://github.com/aaif-goose/goose、Apache-2.0、45.2k★、v1.34.0、旧block/goose→Linux Foundation AAIF移管）
- **判断:** L3投入（goose-l3_lightrag.txt、2688 bytes）
- **種別:** agent / framework（汎用AIエージェント、デスクトップ+CLI+API、Rust製）
- **重複チェック:** goose専用エントリなし。同カテゴリ（エージェントCLI/フレームワーク）に letta-code/claude-agent-sdk/opencode-anomalyco/everything-claude-code/anthropic-claude-code 等があるが全て別実装 → 「テーマ重複だが実装スコープが異なる」→ 別エントリ+cross-reference（CodeGraphと同じ扱い）。
- **投入根拠:** Yusukeの3関心に同時に刺さる稀なリポジトリ。(1)OpenRouter/Ollama公式対応で現環境(KVM2)に乗るClaude Code代替候補、(2)evals/open-model-gym + goose-self-test.yaml がエージェント評価の実装事例＝評価プラットフォーム企画の参考、(3)recipe + Custom Distros がスキル/MCP提供プラットフォームの先行事例。45.2k★・財団管理で信頼性十分。
- **再検討条件:**
  1. VPSでClaude Code以外のエージェント選択肢を本格評価する時 → 比較候補として検証
  2. スキル/MCP提供プラットフォーム企画を具体設計する時 → recipe共有・Custom Distros を競合/先行事例として分析
  3. エージェント評価軸（客観スコア）を設計する時 → open-model-gym / self-test の評価方式を参照
  4. 顧客にブランド付きエージェント配布を提案する時 → Custom Distributions が直接の実装手段
- **関連:** NVIDIA発「評価サービス」想像（2026-06-01ブレスト）、評価軸を差別化に使う企画レンズと地続き。

---

## 2026-06-06 リポジトリ評価バッチ（6件）

### L3投入（5件）

- **ecc-l3** (affaan-m/ECC) — クロスハーネス型エージェント性能最適化システム。63 agents/249 skills/instinct学習/AgentShield。【投入根拠】skills/MCP提供プラットフォーム構想の「客観評価スコア付与」差別化角度の最重要先行事例（AgentShieldのA-F評価・CIゲート、Goose open-model-gymと並ぶ評価系参照）。continuous-learning-v2のinstinct学習はL2/L0抽出に波及。【注記】README上のStar数主張（182K/205k）は誇張の可能性、機能事実ベースで扱う。【再評価トリガー】skills/MCP評価系設計に着手する時。
- **quant-mind-l3** (LLMQuant/quant-mind) — 定量金融向けナレッジ抽出・検索フレームワーク（NeurIPS 2025採択）。arXiv→構造化KB→RAG/DeepResearch/Data MCPの2段階疎結合アーキ。【投入根拠】自社LightRAG「外部脳」パイプラインと構造酷似。EDINET DB（日本株財務）との組み合わせで日本市場向け定量金融ナレッジ抽出の独自展開余地。【再評価トリガー】定量金融/日本株向けナレッジMCP設計着手時。
- **vimax-l3** (HKUDS/ViMax) — マルチエージェント動画生成（Director/Screenwriter/Producer/Generator統合）。OpenRouter/MiniMax対応、RAGベース長尺脚本、生成→並列→VLM検証→ベスト選択。【投入根拠】OpenRouter標準構成で自社環境親和性高。asset-sheet-extractor/property-completion-prompt-builderとのL2組み合わせ余地。【再評価トリガー】動画/素材生成パイプライン企画着手時。
- **viga-l3** (Fugtemypt123/VIGA) — Vision-as-Inverse-Graphicsエージェント（arXiv:2601.11109）。analysis-by-synthesis、Generator/Verifier自己反省ループ、finetuning不要。【投入根拠】「生成→検証→修正」自己反省ループ原理（ECC verification-loop/ViMaxと共通）、進化するコンテキストメモリ（L0-006具体例）の学習価値。【注記】GPU必須でKVM2実行不可、設計思想参照用L3。【再評価トリガー】自己反省/検証ループ系L2抽出時、GPU環境確保時。
- **odysseus-l3** (pewdiepie-archdaemon/odysseus) — セルフホスト型AIワークスペース。opencodeベース、FastAPI+ChromaDB memory、Cookbook(llmfit)、DeepResearch、AIトリアージEmail。【投入根拠】opencode系フルスタック実装＋self-hosted運用設計＋VRAM-awareモデル選定の参照。n8n→エージェント駆動オフィス自動化アップセルのUX参照。【注記】ローカルモデルサーブはGPU前提でKVM2では限定的（API接続前提なら可）。【再評価トリガー】self-hostedエージェントワークスペース実装着手時。

### 見送り（1件）

- **PDFCraftTool/pdfcraft** — ブラウザ完結型PDFツールキット（90+ツール、WASM、Next.js15、AGPL-3.0）。【見送り理由】完成度は高いがブラウザ完結のエンドユーザー向けツールで、エージェント開発・組み合わせ思考への波及が薄い。「WASMクライアントサイドPDF処理」の実装パターン1点のみ価値があるが、L3全体投入の優先度は低い。【再評価トリガー】クライアントサイドPDF処理を要する具体案件が発生した場合。


---

## 2026-06-06 リポジトリ評価バッチ2（統合記録）

### L3投入（7件）

- **syncthing-l3** (syncthing/syncthing) — P2P継続ファイル同期（Go、MPL-2.0）。self-hosted同期基盤。ローカルPC⇔VPSのObsidian Vaultミラー（Receive Only+Staggered Versioning）。【注記】同期≠バックアップ（削除伝播）、世代復元はrestic/borg併用、クラウドはrclone。
- **understand-anything-l3** (Lum1104/Understand-Anything) — コード/wiki→インタラクティブナレッジグラフ化の学習特化Claude Codeプラグイン（TS、MIT、14.7k star）。LightRAGのUX/可視化面を補完。graphify/codegraph/microsoft-graphragと差別化（学習・オンボーディング特化）cross-ref済み。
- **listmonk-l3** (knadh/listmonk) — self-hostedニュースレター/メール管理（Go、AGPL-3.0、21.3k star）。n8n連携・transactional email基盤。【注記】AGPL、顧客提供時はライセンス検討。
- **postiz-l3** (gitroomhq/postiz-app) — self-hosted agentic SNS投稿スケジューリング（NextJS/NestJS、28+チャンネル）。n8n公式custom node、postiz-agentでClaude/OpenClaw連携。listmonkと対の配信基盤。【注記】ライセンス要確認。
- **ppt-master-l3** (hugohe3/ppt-master) — 文書→編集可能PPTX生成スキルパック（Python、MIT、2.1k star）。SVG→PPTX、7ロール設計（Strategist=L0-002具体例）、CRAP自動適用。skill-pptx等と差別化cross-ref済み。
- **composio-l3** (ComposioHQ/composio) — エージェントツール統合基盤（1000+ toolkits、MIT、28.6k star）。Rube(MCP)はskills/MCP事業の比較対象。全エージェントFW対応。【注記】コア機能はホステッドバックエンド依存、完全self-hostではない。
- **mattpocock-skills-l3** (mattpocock/skills) — 実エンジニア向け日常運用スキル集（MIT、117k star）。grilling(=L0-002実装)/CONTEXT.md(L1運用)/caveman(コスト最適化)。software fundamentals裏付けの設計哲学。skill-creator等と差別化cross-ref済み。

### L2c投入（1件）

- **domain-skillpack-productized-service-l2c** — ドメイン特化スキルパックのproductized service化パターン。一次事例zubair-trabzada/ai-recruiter-claude＋11業種横展開。「業務分解×評価スコア×PDF成果物×段階価格×横展開」5要素。status:unverified。技術ではなく事業設計の参照。【昇格条件】1業種で実装・成果物化、またはn8nアップセルで1件設計。

### 見送り（4件）

- **anus-dev/ANUS** — Grok製ターミナルAIエージェント（6.4k star）。成熟度低（commit 15）、既存CLIエージェントL3群と重複、L3支配悪化。参考: AI-First Contribution ProtocolはL0-009対極事例。
- **cporter202/API-mega-list** — APIディレクトリ（awesome-list、ライセンス不明）。グラフ構造化不適、Apifyアフィリエイト性格、鮮度命で静的投入陳腐化。
- **codecrafters-io/build-your-own-x** — 技術自作チュートリアルリンク集（CC0、497k star）。awesome-list型で学習リソース、事業ドメイン外、web検索代替可。
- **zubair-trabzada/ai-recruiter-claude（リポ単体L3）** — 成熟度低・既存skillパターン重複で技術L3価値弱。価値はビジネス設計のため上記L2cパターンとして抽出。

### 調査のみ（投入なし）

- **エージェント×企業プロフィール・マッチングエンジン** — ピンポイントの成熟OSSは稀少（商用SaaS支配）。候補: b2pair / b2b-sdr-agent-template(5軸スコアリング) / openfang(ICP探索) / recsys-agent(LangGraph)。EDINET DB（日本上場約3,800社プロフィール保有）×エージェントで自作が現実解。L2c企画候補として保留。


---

## 2026-06-06 L2c企画投入（combination-architect、3件）

> 本日のL3投入から組み合わせた企画。いずれもstatus:unverified（未実装）。

- **self-hosted-multichannel-distribution-l2c** — 自社ホスト型マルチチャネル配信基盤（listmonk+Postiz+n8n）。メール＋SNSをn8nでオーケストレーションし外部SaaS（Mailchimp+Buffer）を自社VPSで代替。n8nアップセルの配信代行商材。【昇格条件】自社VPSにデプロイしn8nで生成→両チャネル配信→イベント回収を1本動作、または顧客案件1件。【注記】listmonk(AGPL)/Postiz(要確認)のライセンスを商品化前に解消必須。
- **company-profile-matching-engine-l2c** — 企業プロフィール・マッチングエンジン（EDINET DB×エージェント）。日本上場約3,800社プロフィールをembedding化＋LLM再ランク＋5軸スコアリング。成熟OSS稀少な領域をEDINET DB（独自データ資産）で自作・差別化。【昇格条件】EDINET DBプロフィールをembedding化し類似企業マッチング＋理由生成を1クエリ動作、またはマッチングPDFレポート1件。【参考OSS未投入】b2b-sdr-agent-template/openfang/recsys-agent。
- **document-to-sns-image-pipeline-l2c** — 文書→SNS画像→配信パイプライン（ppt-master+asset-sheet-extractor+Postiz）。文書1本からデザイン済みSNS画像を生成し28媒体配信。note発信のSNS展開・顧客コンテンツマーケ自動化。【昇格条件】文書からppt-masterでSNS画像生成しPostizで1媒体配信、またはnote記事1本でパイプライン通し。


---

## 2026-06-13: paperclip-l3 — L3投入

- **対象:** https://github.com/paperclipai/paperclip
- **判断:** L3投入(paperclip-l3)
- **根拠:** エージェント組織管理の制御プレーン(67.4k★、MIT、TS)。フレームワーク層(CrewAI/openswarm等)と異なるオーケストレーション層で既存ナレッジと差別化明確。OpenClawをファーストクラス統合対象とし、承認ゲート+予算ハードストップ+heartbeat委譲はL0-009/L0-002/L0-005の実装例。エージェント開発アップセル最終段の運用基盤商材候補
- **注記:** record_decision初回実行(C-2試運転)。Hermes連携論点はpaperclip-l3本文に記載済み
- **関連:** agentic-os-design-pattern-l2c / openswarm-vrsen-l3 / rowboat-l3 / goose-l3 / durable-execution-hitl-approval-l2 / L0-009 / L0-002
- **再検討条件:**
  1. OpenClawプロジェクトで複数エージェント運用を開始する時
  2. エージェント開発アップセルで運用基盤の商材設計に着手する時
  3. Hermes Agent等の常駐型エージェントとの連携検証時(スケジューラ一元化・責任境界の設計が前提)

---

## 2026-06-13: hermes-agent-l3 — L3投入

- **対象:** https://github.com/NousResearch/hermes-agent
- **判断:** L3投入(hermes-agent-l3)
- **根拠:** Nous Researchの常駐型自己改善エージェント(v0.14.0、MIT)。OpenClaw直接競合かつ公式移行パス(hermes claw migrate)を持ち、OpenClawプロジェクトの技術選定判断材料として参照価値が高い。トランスポート抽象化(ProviderTransport ABC)・マルチプラットフォームゲートウェイ・永続キュレーション型メモリ・スキル自動生成/自己改善ループはL3「作り方を知る」の典型。agentskills.io標準互換はスキル/MCPプラットフォーム事業の標準動向把握に直結。重複チェック(naive 2クエリ)済み: 単独エントリなし、paperclip-l3内の言及はcross-refとして処理。
- **注記:** 姉妹リポジトリ hermes-agent-self-evolution(DSPy+GEPA、ICLR 2026 Oral)は次の評価候補キューに積む(Yusuke委任によるアシスタント判断、今回未投入)。本件はrecord_decision新フロー(C-2)のコネクタ再接続後初の通し検証を兼ねる。
- **関連:** paperclip-l3(多層委譲構成でHermes言及、cross-ref)、skill-design-patterns-l2、agentic-os-design-pattern-l2c、open-interpreter-l3
- **再検討条件:**
  1. OpenClawからの移行を実際に検討するプロジェクトが発生した時(hermes claw migrateの実地検証)
  2. skill-verifier/客観スコアリング構想の実装に着手し自己改善ループの先行事例調査が必要になった時(self-evolution別件評価とセット)
  3. クライアント案件でメッセージング統合常駐エージェントの構築依頼が来た時

---

## 2026-06-14: ai-sales-team-claude — 保留

- **対象:** https://github.com/zubair-trabzada/ai-sales-team-claude
- **判断:** 保留(ai-sales-team-claude)
- **根拠:** 業種特化型Claude Codeスキルパック（営業支援）。orchestrator SKILL + 13サブスキル + 5並列subagent + Pythonスクリプト + テンプレート + 加重合成スコア(0-100) + client-ready PDF + ワンコマンド配布という共通アーキテクチャを持つ。BANT+MEDDICの定量スコアリングとクロススキル連携（prospect→outreach/prep/proposalのデータ受け渡し）が明文化されており、4件中で最も成熟（717★/256fork）。Yusukeのアップセルモデル（n8n→Claude Code→アプリ→エージェント）のClaude Code層の商品テンプレートに直結するため、汎用部品在庫としてのL3即投入ではなく、実案件で営業支援パックを組む際に self検証を経てL3/L2c化する想定で保留。
- **注記:** 作者zubair-trabzada(AI Workshop)。スキルパック4件は同一アーキテクチャ。スコアリング方法論・クロススキル連携図はREADMEに明示。LLM分析のみで外部API非依存。
- **関連:** ai-marketing-claude（同一作者・同系統で保留）, dataforseo-claude/ai-legal-claude（同系統で見送り）, wshobson-agents-l3, claude-agent-sdk-python-l3
- **再検討条件:**
  1. 営業支援系の実案件（リード獲得・商談支援の自動化）を受注し、Claude Codeスキルパックとして構築する時
  2. combination-architectで「業種特化×並列subagent×PDF納品」の縦型商品を企画する時
  3. 4件共通の構成パターンをL2c「業種特化Claude Codeスキルパック構成パターン」として抽出する判断をする時

---

## 2026-06-14: ai-marketing-claude — 保留

- **対象:** https://github.com/zubair-trabzada/ai-marketing-claude
- **判断:** 保留(ai-marketing-claude)
- **根拠:** 業種特化型Claude Codeスキルパック（マーケティング支援）。ai-sales-teamと同一アーキテクチャ（orchestrator + 14サブスキル + 5並列subagent + Pythonスクリプト + テンプレート + 加重合成スコア + PDF納品 + ワンコマンド配布）。Webサイト・LP・コピー・広告領域を扱い、YusukeのWebサイト/Webアプリ開発領域と重なる。スコアリング方法論が6次元加重で明文化されている点が設計リファレンスとして価値が高い。汎用部品在庫としてのL3即投入ではなく、実案件でマーケ支援パックを組む際にself検証を経てL3/L2c化する想定で保留。
- **注記:** 作者zubair-trabzada(AI Workshop)。6次元加重スコア（Content25/Conversion20/SEO20/Competitive15/Brand10/Growth10）が表で明文化。email系列・提案書・コンテンツカレンダー等のテンプレート資産が厚い。LLM分析のみで外部API非依存。697★/286fork。
- **関連:** ai-sales-team-claude（同一作者・同系統で保留）, dataforseo-claude/ai-legal-claude（同系統で見送り）, postiz-l3, wshobson-agents-l3
- **再検討条件:**
  1. マーケティング/LP/コンテンツ支援系の実案件をClaude Codeスキルパックとして構築する時
  2. combination-architectで「Webサイト監査×並列subagent×PDF納品」の縦型商品を企画する時
  3. 4件共通の構成パターンをL2c「業種特化Claude Codeスキルパック構成パターン」として抽出する判断をする時

---

## 2026-06-14: dataforseo-claude — 見送り

- **対象:** https://github.com/zubair-trabzada/dataforseo-claude
- **判断:** 見送り(dataforseo-claude)
- **根拠:** 業種特化型Claude Codeスキルパック（SEO監査）。アーキテクチャは同系統だが、唯一外部有料API（DataForSEO）依存で、APIキー・課金が前提。手本としての参照価値（外部有料APIをスキルに統合し、LLM分析でなくreal dataを返すパターンの実例）は認めるが、汎用部品在庫としてのL3には不適。Star少・スポンサー連携色が強く、実案件で組む蓋然性も保留2件より低い。商品設計の対比素材（API依存型 vs LLM分析型）として外部参照に留め、現時点では投入しない。
- **注記:** 作者zubair-trabzada(AI Workshop)。DataForSEOとのスポンサー連携で構築。13スキル+5subagent。他3件と異なり外部有料API（DataForSEO、従量課金 ~$0.10-0.30/audit）に依存する「real data型」。2★/0fork、6 commitsと新しくコミュニティ実績は薄い。
- **関連:** ai-sales-team-claude/ai-marketing-claude（同一作者・同系統で保留）, ai-legal-claude（同系統で見送り）
- **再検討条件:**
  1. SEO/検索順位データを扱う実案件で、外部SEO APIをClaude Codeスキルに統合する必要が生じた時
  2. 「外部有料APIをスキルパックに統合する」パターンをL2c化する判断をする時
  3. DataForSEO以外も含めたSEO API統合の比較検討が実案件で必要になった時

---

## 2026-06-14: ai-legal-claude — 見送り

- **対象:** https://github.com/zubair-trabzada/ai-legal-claude
- **判断:** 見送り(ai-legal-claude)
- **根拠:** 業種特化型Claude Codeスキルパック（法務支援）。アーキテクチャは同系統だが、契約レビュー・法的判断の体裁を持つ出力は日本の弁護士法・士業規制（非弁行為）と直接抵触しうる領域で、そのまま商品化しにくい。ディスクレーマ設計・リスク領域での出力の作り方の素材としては参照価値があるが、汎用部品在庫としてのL3には不適。規制論点を含むため、商品設計の参照素材（リスク領域での出力設計事例）として外部参照に留め、現時点では投入しない。
- **注記:** 作者zubair-trabzada(AI Workshop)。契約レビュー/リスク分析/NDA生成/コンプラ監査。13スキル+5subagent+加重Contract Safety Score。READMEに「法的助言ではない」ディスクレーマ明記。5★/4fork、2 commits、claudeがcontributor。
- **関連:** ai-sales-team-claude/ai-marketing-claude（同一作者・同系統で保留）, dataforseo-claude（同系統で見送り）
- **再検討条件:**
  1. 法務/契約関連の実案件で、規制を踏まえた出力設計（ディスクレーマ・免責・士業連携）を検討する必要が生じた時
  2. 日本の非弁規制を踏まえたうえで契約レビュー補助ツールの商品化可否を本格検討する時
  3. リスク領域（法務・医療・金融助言等）での出力設計パターンをL0/L2c化する判断をする時

---

## 2026-06-15: agno — L3投入

- **対象:** https://github.com/agno-agi/agno
- **判断:** L3投入(agno)
- **根拠:** エージェントプラットフォームの構築・運用・管理を行うPython SDK。単体のエージェント構築フレームワークではなく、プロダクション運用基盤（control plane）を含む点が独自。任意フレームワークで構築→tracing/scheduling/RBAC付きサービス化→単一control planeで管理という3軸構造。既存のエージェント在庫と直接の重複ポジションがなく、「プロダクション運用層を持つPython製エージェントSDK」という空きを埋める。アップセルモデル最終段（エージェント開発）の自前プラットフォーム基盤候補であり、かつL0-PRODUCT-CONSTRAINTS.mdの複数制約の参照実装になる: JWTベースRBAC/マルチテナント分離→憲章Article6、Human approvalループ→L0-002/L0-009、Observability/監査ログ→L0-010、Context Providers(MCP対応)→LightRAG MCPのcontext source組み込み。参照価値が突出して高く、安定性も十分なためL3投入。
- **注記:** file_name: agno-l3_lightrag.txt（3079 bytes, upload成功・background処理中）。Apache-2.0、Python 99.7%、40.4k★/5.4k fork、5642 commits、192 releases（最新v2.6.9）。重複チェック: naive 2クエリ実施、Agno自体の既存なし（類似はCrewAI/Agent Zero/OpenSwarm/Vercel AI SDK/Paperclip等だがポジション重複なし）。
- **関連:** crewai-l3, agent-zero-l3, openswarm-vrsen-l3, vercel-ai-sdk-l3, paperclip-l3, claude-agent-sdk-python-l3, agentic-os-design-pattern-l2c
- **再検討条件:**
  1. エージェント開発の実案件で自前運用プラットフォーム基盤を選定する時（Agnoを第一候補として技術検証）
  2. Human approval/RBAC/監査ログの実装をL0-002/L0-009/L0-010の実装リファレンスとして参照する時
  3. LightRAG MCPをエージェントのcontext sourceとして組み込む構成を設計する時
  4. メジャーバージョン更新で破壊的変更や機能追加があった時（最終確認日2026-06-16の鮮度更新）

---

## 2026-06-15: SurfSense — L3投入

- **対象:** https://github.com/MODSetter/SurfSense
- **判断:** L3投入(SurfSense)
- **根拠:** チーム向けOSS NotebookLM代替（データ無制限・self-host・プライバシー重視）。27+コネクタ、100+LLM/6000+embedding（vLLM/Ollama対応）、Hybrid Search（セマンティック+全文+階層インデックス+RRF）、LangChain Deep Agentsベースのagentic構成、引用付きレポート多形式出力、スケジュール/イベントトリガー自動化+コネクタwrite-back、RBAC付きリアルタイム協働を一体化。Yusukeが自作中のLightRAGナレッジ管理と同ドメインの「完成した実装リファレンス」であり、方向性は異なる（汎用NotebookLM代替 vs 開発ナレッジ外部脳+MCP）ため置換対象ではなく設計参照元として価値が高い。具体的参照点: Hybrid Search→LightRAG検索最適化の比較対象、コネクタ+write-back+自動化→アップセル「アプリ層」完成形の手本、RBAC+マルチテナント→L0-PRODUCT-CONSTRAINTS Article6参照実装、Deliverable Studio→ナレッジ成果物生成の商品機能手本。既存在庫に同種なし・コアドメイン直撃のためL3投入。ただしv0.0.26・本番未対応のため注意タグ付き（設計参照に留め本番採用は時期尚早）。
- **注記:** file_name: surfsense-l3_lightrag.txt（3375 bytes, upload成功・background処理中）。Apache-2.0、Python66.7%/TS30.5%、14.4k★/1.4k fork、6232 commits。★v0.0.26でREADME自身が「プロダクション未対応」明記＝注意タグ付きで投入。重複チェック: naive 2クエリ実施、SurfSense自体の既存なし（RAG在庫lightrag/rag-patterns等はあるが統合NotebookLM代替アプリは未在庫）。
- **関連:** lightrag-framework-l3, rag-application-design-patterns-l2, rag-pipeline-patterns-l2, rag-retrieval-quality-l2c, agno-l3, supabase-l3, langgraph-l3, deeptutor-l3
- **再検討条件:**
  1. LightRAGの検索品質改善（L2比率・検索精度）でHybrid Search/階層インデックス/RRFの実装を参照する時
  2. アップセル「アプリ層」でコネクタ統合・成果物生成・自動化を持つナレッジアプリを設計する時
  3. SurfSenseが安定版（1.0系）に到達し本番採用可否を再検討する時（現v0.0.26・本番未対応）
  4. LangChain Deep Agentsの実運用パターンを参照する時
  5. 最終確認日2026-06-16から時間が経ち高速開発で構成が変わった可能性がある時（鮮度更新）

---

## 2026-06-15: Novu — L3投入

- **対象:** https://github.com/novuhq/novu
- **判断:** L3投入(Novu)
- **根拠:** オープンソースの通知インフラ。In-App/Inbox・Email・SMS・Push・Chatのマルチチャネル配信を単一APIに統合し、埋め込み可能な<Inbox/>コンポーネント、Notification Workflow Engine、Digest Engine、ノーコードメールエディタ、購読者設定コンポーネントを提供。Email19/SMS37/Push8/Chat12プロバイダ対応。既存在庫に通知インフラ層がなく（Resendはメール単体でNovuに内包される関係）、アップセル「アプリ層/Webアプリ開発」で通知機能を一括搭載する標準部品として参照価値が高い。認証=Clerk、メール=Resendと並ぶ「通知=Novu」の位置。埋め込みInboxでSaaS型アプリに即通知センターを付与でき案件工数を削減、n8n/Inngestと組み合わせてイベント駆動マルチチャネル配信が組める、エージェント成果物のラストワンマイル配信部品にもなる。39k★・MIT(コア)・成熟度十分のためL3投入。ただしOpen Coreのライセンス境界（EE範囲の商用利用）の注意タグ付き。
- **注記:** file_name: novu-l3_lightrag.txt（2503 bytes, upload成功・background処理中）。TypeScript97%、39k★/4.3k fork、21852 commits、117 releases。★Open Core（コアMIT / enterprise・ee配下はEEライセンス）＝ライセンス境界の注意タグ付き。重複チェック: naive 2クエリ実施、Novu自体の既存なし（通知系在庫はResend単体/Inngestのみ、マルチチャネル通知インフラは未在庫。ResendはNovuのEmailプロバイダの1つに内包される関係）。
- **関連:** resend-react-email-l3, inngest-l3, nextjs-l3, shadcn-ui-l3, supabase-l3, agno-l3, surfsense-l3
- **再検討条件:**
  1. Webアプリ/SaaS案件で通知センター・マルチチャネル通知を実装する時（Novuを標準部品として第一候補に）
  2. n8n/Inngestのイベント駆動と通知配信を連携させる構成を設計する時
  3. エージェント成果物をユーザーへ通知配信するラストワンマイルを設計する時
  4. self-hostで商用利用する際にMIT範囲/EE範囲のライセンス境界を確認する必要が生じた時
  5. 最終確認日2026-06-16から時間が経ちプロバイダ・SDK対応（Vue/Angular/RN等）が変わった時（鮮度更新）

---

## 2026-06-15: jellyfin — 見送り

- **対象:** https://github.com/jellyfin/jellyfin
- **判断:** 見送り(jellyfin)
- **根拠:** フリーソフトウェアのメディアサーバー（Plex/Emby代替、Emby 3.5.2を.NETへ移植）。映画・音楽・写真を専用サーバーから各デバイスへ配信する。極めて成熟・大規模なOSSだが、Yusukeの開発領域（Website/Webアプリ/AIエージェント/n8nワークフロー）およびLightRAGの「ナレッジ活用エージェント」構想のいずれにも該当しないドメイン外。スタックもC#/.NET中心でYusukeのPython/TypeScript中心スタックと外れる。トランスコード観点は既存のffmpeg-l3でカバー済みで補完性もない。ナレッジ投入境界v3（汎用スキル・パターンのみ／気になる技術スタックの部品在庫）に照らし、L3投入はL3純度（Yusukeスタックの部品在庫という性質）を薄めるため非推奨。ドメイン外・スタック外として見送り記録。
- **注記:** C# 99.6%、GPL-2.0、51.8k★/4.8k fork、28933 commits、105 releases（最新v10.11.9 / 2026-05）。.NET 10 SDK + ffmpeg前提。重複チェック: naive 2クエリ実施、Jellyfin自体の既存なし。トランスコード観点は既存のffmpeg-l3でカバー済み。
- **関連:** ffmpeg-l3, docmost-l3, cal-diy-l3, odysseus-l3
- **再検討条件:**
  1. 自宅またはVPSでメディアサーバー（動画・音楽配信）をself-host運用する個人案件・実需が具体化した時
  2. C#/.NETスタックの大規模プラグインアーキテクチャを設計参照したい具体ニーズが出た時
  3. メディアストリーミング/配信領域がYusukeの開発領域・商品ドメインに加わった時

---

## 2026-06-15: ponytail — L3投入

- **対象:** https://github.com/DietrichGebert/ponytail
- **判断:** L3投入(ponytail)
- **根拠:** AIコーディングエージェントの過剰実装を抑制するルールセット＋スキルパック（最良のコードは書かなかったコード）。怠惰の梯子（YAGNI→標準ライブラリ→ネイティブ機能→既存依存→1行→最小実装）でコード生成前に最初に成り立つ段で止める。「怠惰だが手抜きではない」（trust境界バリデーション/データ損失対応/セキュリティ/アクセシビリティは削らない）、取った近道はponytail:コメントで明示。13エージェント対応（Claude Code/Codex/Copilot/pi/OpenCode/Gemini/Antigravityのプラグイン型 + Cursor/Windsurf/Cline/Aider/Kiroのルールファイル型）。既存在庫に過剰実装抑制・YAGNI強制のスキルパックがなく重複なし。Yusukeのコア活動（SKILL開発/skill-verifier/combination-architect）とL0原理に直結: promptfoo定量ベンチはskill-verifier構想の先行事例（hermes-agentと同枠）、怠惰の梯子はL0-008完成度の段階や判断構造化の設計信念のスキル実装例、縦型スキルパックに過剰実装抑制の制御層を噛ませる手本、13エージェント移植の実装リファレンス。MIT・13.6k★でL3投入。ただしベンチ数値は自己申告のため注意タグ付き。
- **注記:** file_name: ponytail-l3_lightrag.txt（3108 bytes, upload成功・background処理中）。MIT、JS91%/Python8%、13.6k★/553 fork、62 commits、8 releases（最新v4.6.0 / 2026-06-15）。★ベンチ数値80-94%減等は作者自己申告（median of 10 runs、promptfoo再現手順は公開）＝注意タグ付き。重複チェック: naive 2クエリ実施、ponytail/caveman自体の既存なし。READMEが比較対象に挙げるJuliusBrussee/cavemanは同系統で別途評価キュー追加。
- **関連:** skill-design-patterns-l2, multi-tool-skills-sharing-l2c, codex-plugin-cc-l3, awesome-agent-skills-l3, hermes-agent-l3, openspec-spec-driven-dev-l3
- **再検討条件:**
  1. skill-verifierの客観スコアリング設計でpromptfooベンチ手法を参照する時
  2. オリジナルSKILL開発で過剰実装抑制・YAGNI強制の制御を組み込む時
  3. combination-architectで縦型スキルパックに「過剰実装抑制層」を設計する時
  4. マルチエージェント移植（プラグイン型/ルールファイル型2系統）の実装を参照する時
  5. ベンチマーク数値の第三者検証や自前再現を行う必要が生じた時（現状は作者自己申告）
  6. 比較対象cavemanの評価結果が出てponytailとの優劣・使い分けを整理する時

---

## 2026-06-15: caveman — L3投入

- **対象:** https://github.com/JuliusBrussee/caveman
- **判断:** L3投入(caveman)
- **根拠:** AIエージェント出力をトークン圧縮するClaude Code等30+対応スキル/プラグイン（原始人話法で出力トークン約65%削減・技術的正確性は保持）。ponytailと同じ「トークン削減」だが作用点が補完的: ponytailは書くコード量を減らす（YAGNI）、cavemanは話す出力トークンを減らす（電文体）。併用可能で削減レイヤーが異なる。特にYusuke文脈との接続が強い: (1)caveman-shrink（MCPミドルウェア）はLightRAG MCPに直接適用可能で、現在のブランチfeature/compression-middlewareの領域に直結する参照実装、(2)caveman-compressはRESUME.md/プロジェクトファイル圧縮に転用可能、(3)既存llm-token-reduction-proxy系パターンの実装リファレンス、(4)実APIトークン計測＋誠実な比較対象（"Answer concisely."と比較）＋再現スクリプト公開でskill-verifier構想の先行事例。69.4k★・MITでL3投入。出力トークンのみ削減（thinking不変）・電文体は顧客納品向けでない点を注意タグで明記。
- **注記:** file_name: caveman-l3_lightrag.txt（3564 bytes, upload成功・background処理中）。MIT、JS63%/Python28%、69.4k★/3.9k fork、185 commits、14 releases（最新v1.8.2 / 2026-05-12）。ponytail評価時のnaive 2クエリでcaveman自体の既存なし確認済み。ponytailと同時期に評価キュー追加→L3投入。エコシステム他4ツール（caveman-code/cavemem/cavekit/cavegemma）は別途評価候補。
- **関連:** ponytail-l3, llm-token-reduction-proxy-l2c, codex-plugin-cc-l3, multi-tool-skills-sharing-l2c, awesome-agent-skills-l3, hermes-agent-l3
- **再検討条件:**
  1. LightRAG MCPのトークンコスト削減でcaveman-shrink（MCP記述圧縮ミドルウェア）の適用を検討する時
  2. ブランチfeature/compression-middlewareの実装でMCP圧縮の参照実装が必要な時
  3. RESUME.md/KNOWLEDGE-INDEX等のメモリ・ドキュメント圧縮でcaveman-compress手法を参照する時
  4. skill-verifierの客観スコアリング設計で実APIトークン計測ベンチ手法を参照する時
  5. エコシステム他ツール（caveman-code/cavemem/cavekit/cavegemma）の評価可否を判断する時
  6. ponytailとの併用パターンをL2c化する判断をする時

---

## 2026-06-15: Claude for Small Business — L3投入

- **対象:** https://claude.com/plugins/small-business
- **判断:** L3投入(Claude for Small Business)
- **根拠:** Anthropic公式の小規模事業者向けプラグイン（Claude Cowork）。新プランではなくPro/Max/Team契約にトグル追加するスキル+コネクタの束。15ワークフロー+15スキル（/plan-payroll, /close-month, /run-campaign, /monday-brief等、下に cash-flow forecasting/invoice chasing/contract review/margin analysis等が自動発動）。コネクタはQuickBooks/PayPal/HubSpot推奨+Canva/DocuSign/Gmail/Outlook/Slack/Stripe/Square、未接続時はgraceful degradation。money/customerに触れる操作は人間承認。Yusukeのアップセルモデル「アプリ層商品」のAnthropic公式による基準点（リファレンス実装かつ競合）。「職種特化スキルパック+コネクタ+自然言語ルーター+人間承認」構造は構想中の縦型商品そのもので差別化検討材料。前回zubator系（sales/marketing/legal）保留・見送り判断の裏付け（公式が同領域カバー）。人間承認設計はL0-002/L0-009の商用実装例、graceful degradationは堅牢な商品設計の手本、常駐自動化が別レイヤー必要な点はn8n資産の差別化余地。公式・基準点としての参照価値が高くL3投入。
- **注記:** file_name: claude-for-small-business-l3_lightrag.txt（3507 bytes, upload成功・background処理中）。Anthropic公式（Anthropic Verified）、2026-05-13発表。Claude Coworkプラグイン（marketplace: anthropics/knowledge-work-plugins）。GitHubリポジトリではなく公式プロダクトのため出典は公式ページ（claude.com/plugins/small-business, anthropic.com/news, claude.com/solutions/small-business）。web_search+公式ページweb_fetchで一次確認。重複チェック: naive 2クエリ実施、自体の既存なし。
- **関連:** anthropic-claude-code-l3, skill-product-self-knowledge-l3, awesome-agent-skills-l3, multi-tool-skills-sharing-l2c, domain-skillpack-productized-service-l2c, ai-sales-team-claude, ai-marketing-claude
- **再検討条件:**
  1. アップセル「アプリ層」で職種/業種特化スキルパック商品を企画する時（公式構造を基準点に差別化を設計）
  2. 人間承認フロー（money/customer操作）の商用実装をL0-002/L0-009の参照として設計する時
  3. 日本市場・特定業種向けにClaude for Small Business相当を組む際の差別化（n8n常駐自動化との組み合わせ等）を検討する時
  4. 公式プラグインのスキル/コマンド構成・コネクタ・料金が更新された時（最終確認日2026-06-16の鮮度更新）
  5. 日本での提供状況・日本語対応・対応会計ソフトを確認する必要が生じた時

---

## 2026-06-15: AstrBot — L3投入

- **対象:** https://github.com/AstrBotDevs/AstrBot
- **判断:** L3投入(AstrBot)
- **根拠:** IMプラットフォーム統合型のオールインワン・エージェントチャットボット基盤（"openclaw alternative"公称）。QQ/WeChat/Feishu/DingTalk/Telegram/Slack/Discord/LINE等多数のIMに対応、マルチLLM（Anthropic含む）、MCP/Skills/ナレッジベース/ペルソナ/自動コンテキスト圧縮、Agent Sandbox（隔離実行）、1000+プラグインのマーケットプレイス、豊富なデプロイ手段。既存在庫にIM常駐型エージェント基盤がなく独自ポジション。Yusuke文脈との接続が複数: (1)OpenClaw代替公称でopenclawのIMフロントエンド比較対象、(2)LINE対応が日本の小規模事業者向けアップセルの差別化手段（米国SaaS中心のClaude for Small Businessに対する日本市場の具体策）、(3)Agent Sandboxはminiclaw-sandbox-pattern-l2cの実装事例、(4)1000+プラグイン+マーケットプレイスはスキルパック配布モデルの手本、(5)MCP対応でLightRAG MCPをIMボットに組み込み可能。33.7k★・221リリースで成熟しL3投入。ただしAGPL-3.0+EULAのライセンス影響は商品化時に要精査の注意タグ付き。
- **注記:** file_name: astrbot-l3_lightrag.txt（2899 bytes, upload成功・background処理中）。Python70%/Vue24%、33.7k★/2.3k fork、4753 commits、221 releases（最新v4.25.2 / 2026-05-30）、319 contributors。★AGPL-3.0 + EULA.md＝ライセンス注意タグ必須。重複チェック: naive 2クエリ実施、AstrBot自体の既存なし（IM常駐エージェント基盤は未在庫）。
- **関連:** agent-zero-l3, livekit-agents-l3, flowise-l3, miniclaw-sandbox-pattern-l2c, multi-tool-skills-sharing-l2c, claude-for-small-business-l3, caveman-l3
- **再検討条件:**
  1. 日本の小規模事業者向けにLINE常駐AIボット/カスタマーサービスを構築する案件が出た時（AstrBotを第一候補に）
  2. openclawのIMフロントエンド層を設計・比較する時
  3. AGPL-3.0+EULAのライセンス影響を商用・受託組み込みの観点で精査する必要が生じた時
  4. LightRAG MCPをIMボットのツールとして組み込む構成を設計する時
  5. スキルパック商品の配布モデル（マーケットプレイス型）をcombination-architectで検討する時
  6. Agent Sandboxの実装をminiclaw-sandbox-pattern-l2cの参照事例として見る時

---

## 2026-06-15: Hoppscotch — L3投入

- **対象:** https://github.com/hoppscotch/hoppscotch
- **判断:** L3投入(Hoppscotch)
- **根拠:** オープンソースのAPI開発エコシステム（Postman/Insomnia代替）。Web/Desktop/CLI、オフライン/オンプレ/クラウド対応。REST/WebSocket/SSE/Socket.IO/MQTT/GraphQL、OAuth2.0/OIDC/PKCE認証、Pre/Post-Requestスクリプト（JS）、コレクション/環境、チーム/RBAC、CLI（CI連携）、self-host。Yusukeの開発領域「Webアプリ（認証/DB/API）」の標準的な開発・テストツールで、商品の手本ではなく開発を支える実務ツールの部品在庫。LightRAG MCP（port9622）やn8n webhookのエンドポイント動作確認、Hostinger VPSへのself-host、Post-Request TestsでのAPI監視/E2E転用、CLIでn8n/GitHub Actions連携、OAuth/OIDC認証フロー検証（Clerk/Supabase開発のデバッグ）に有用。既存在庫にAPI開発クライアントがなくYusukeスタックの部品在庫として妥当、79.4k★・MIT・成熟のためL3投入。
- **注記:** file_name: hoppscotch-l3_lightrag.txt（2640 bytes, upload成功・background処理中）。TypeScript68%/Vue23%/Rust4%、MIT、79.4k★/5.9k fork、6134 commits、104 releases（最新2026.5.0 / 2026-05-28）。一部SSO等はEnterprise edition feature。重複チェック: naive 2クエリ実施、Hoppscotch自体の既存なし（API開発クライアント未在庫）。
- **関連:** composio-l3, mcp-servers-l3, supabase-l3, nextjs-l3, inspect-ai-l3
- **再検討条件:**
  1. Webアプリ/API開発案件でAPIクライアント・テスト環境が必要な時（Hoppscotchを標準ツールに）
  2. LightRAG MCP/n8n webhookのエンドポイントを叩いて動作確認する時
  3. Hostinger VPSにself-hostのAPI開発環境を構築する時
  4. CLI連携でn8n/GitHub ActionsからAPIテストを自動化する時
  5. OAuth2.0/OIDC/PKCEの認証フローを検証する時（認証付きWebアプリのデバッグ）
  6. チーム機能のフル活用・商用self-hostでEnterprise edition featureの機能境界を確認する時
