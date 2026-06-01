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
- **出典URL**: https://github.com/rtk-ai/rtk
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
- **出典URL**: https://github.com/LiuMengxuan04/MiniCode
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
- **出典URL**: https://github.com/jeecgboot/JeecgBoot
- **理由**: 45.4k stars巨大Java/SpringBoot低代码プラットフォーム。Yusukeさんの技術スタック（TypeScript/Python中心）と言語が合わず、ドメインも企業向け低代码と距離がある
- **再検討条件**: Javaエンタープライズ案件を受注したとき、または業界別Skill戦略の検討に着手したとき

#### Agent Lightning
- **判断**: 保留
- **出典URL**: https://github.com/microsoft/agent-lightning
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

## 2026-05-22 評価分

### dzlau/stripe-supabase-saas-template = 保留

- リポジトリ: https://github.com/dzlau/stripe-supabase-saas-template
- 評価日: 2026-05-22
- 判定: 保留(L2c/L3いずれにも未投入)

#### 保留理由
1. 課金SaaSは別プロジェクトとして起動予定(Vercel + Supabase + Stripe、VPS不要)
2. 現時点で本実装に着手していないため、ナレッジ化が早すぎる
3. テンプレート全体ではなく、本実装で実際に採用したパターンだけをL2c/L3化する方が品質が上がる

#### 再評価条件
- 課金SaaS本実装着手後にL2c/L3再評価
- 採用しなかった場合は見送りに変更

### refactoringhq/tolaria = 見送り

- リポジトリ: https://github.com/refactoringhq/tolaria
- 評価日: 2026-05-22
- 判定: 見送り

#### 見送り理由
1. Mac専用(macOSプラットフォーム依存)で運用環境と不一致
2. スター数3、フォーク少、1人開発で永続性に疑義
3. 既存ナレッジ(汎用リファクタリング系)で代替可能
4. 学べる独自パターンが少ない

#### 再評価条件
- macOSベースの開発環境に移行した場合
- 同等の機能を持つクロスプラットフォームOSSが見つからない場合のみ

### Obsidian = 投入推奨(条件付き)

- 参照: Obsidianアプリ全般、関連OSSエコシステム
- 評価日: 2026-05-22
- 判定: 投入推奨(実使用1-2週間後にL3投入)

#### 投入根拠
1. Yusukeの開発スタイル(マークダウン中心)と整合性が高い
2. ナレッジ管理・ノートテイキングのデファクト
3. AIエージェント(rowboat等)とのObsidian互換vault連携が成立する
4. SKILL/プラグインのエコシステムが豊富

#### 投入条件
- Yusuke自身が1-2週間Obsidianを実使用し、運用イメージが固まってから
- 投入時は使用実感に基づくL3記述(教科書的でなく実用本位)

### kestra-l3 = L3投入済み

- リポジトリ: https://github.com/kestra-io/kestra
- 投入ファイル: kestra-l3_lightrag.txt
- 評価日: 2026-05-22
- 判定: L3投入済み

#### 投入根拠
1. n8nの主要競合(イベント駆動ワークフロー、YAML定義)
2. Yusukeのn8n事業の競合分析用部品在庫として有用
3. エンタープライズ志向の機能差分を把握

#### 再評価条件
- 顧客がKestra採用を検討した場合に詳細精査
- n8n vs Kestra比較資料が必要になった場合

### polar-l3 = L3投入済み

- リポジトリ: https://github.com/polarsource/polar
- 投入ファイル: polar-l3_lightrag.txt
- 評価日: 2026-05-22
- 判定: L3投入済み

#### 投入根拠
1. Merchant of Record型決済プラットフォーム(Stripe代替候補)
2. 海外売上における税務処理を肩代わりするモデル
3. 課金SaaSプロジェクトでの将来的選択肢

#### 再評価条件
- 海外売上の現実化(税務負担が問題化する段階)で乗換検討
- 国内売上のみの段階ではStripeを継続採用

---

## 2026-05-25 評価分

### rowboatlabs/rowboat = L3投入済み

- リポジトリ: https://github.com/rowboatlabs/rowboat
- 公式: https://www.rowboatlabs.com/
- スター数: 9.3k、フォーク: 792、コミット: 1,380
- ライセンス: Apache-2.0
- 投入ファイル: rowboat-l3_lightrag.txt (3424 bytes)
- 評価日: 2026-05-25
- 投入方法: Claude.aiから LightRAG MCP upload_document 経由
- 判定: L3投入済み

#### 投入根拠
1. 戦略の中核と直結: 「ナレッジ活用エージェント構築」というLightRAG運用の根本動機の参考実装
2. Obsidian導入計画との接続: Obsidian互換のMarkdown vaultを採用、Obsidian L3予定との横断知識
3. LightRAGとの対比知識: retrieval cold start vs persistent memory の設計思想対比
4. MCP対応: ナレッジMCPサービス構想の競合・参照例
5. OSS品質: 9.3k stars、YC出身、Apache-2.0、活発開発

#### 再評価条件
- Obsidian L3投入時(隣接知識として連携検討)
- AIエージェント設計時(persistent memory パターンの参照)

### krusemediallc/arcads-claude-code = 見送り

- リポジトリ: https://github.com/krusemediallc/arcads-claude-code
- スター数: 563、フォーク: 153
- 内容: Arcads.ai(商用AI動画広告サービス)のClaude Code用スキルパック
- 評価日: 2026-05-25
- 判定: 見送り

#### 見送り理由
1. Arcads.ai(有料商用サービス)依存で汎用性なし
2. Yusukeの開発領域(Website/Webapp/AIエージェント/n8n)と無関係
3. note.com発信活動は低優先のため広告クリエイティブ領域は射程外
4. 学べるパターン(MASTER_CONTEXT、スキルパック構造)は既存ナレッジで充足

#### 再評価条件
- Yusukeが広告クリエイティブ事業に参入する場合
- 顧客がArcads採用検討した場合

---

## 2026-05-28 評価分

### zubair-trabzada/geo-seo-claude = L3投入済み

- リポジトリ: https://github.com/zubair-trabzada/geo-seo-claude
- スター数: 7.6k、フォーク: 1.2k
- ライセンス: MIT
- 投入ファイル: geo-seo-claude-l3_lightrag.txt (3699 bytes)
- 評価日: 2026-05-28
- 投入方法: Claude.aiから LightRAG MCP upload_document 経由
- 判定: L3投入済み

#### 投入根拠
1. GEO(Generative Engine Optimization)の完結パイプライン: 13サブスキル+5並列エージェントで /geo audit 一発で監査→0-100スコア→クライアント納品PDFまで自動化
2. Webサイト/LP制作サービスへの上乗せ価値: 既存制作に「GEO監査・最適化」を付加可能
3. アップセル階段の新商材候補: n8n→Claude Code→アプリ→エージェントの間に「GEO監査サービス」を挟める。海外では月$2K〜12Kのエージェンシー価格帯
4. マルチエージェント+SKILLオーケストレーション設計の生きた教材

#### 既存ナレッジとの関係(明記)
- skill-ai-seo-l3(coreyhaines31/marketingskills、AEO/GEO/LLMO単一スキル) = コンテンツ最適化の考え方
- 本エントリ(geo-seo-claude) = 監査・納品パイプラインの実装
- skill-page-cro-l3(CRO) = 補完関係
- 3者でスコープが異なるため別エントリで併存

#### 再評価条件
- 顧客向けGEO監査サービスを商材化する段階で、本スキルをベースにL2パターン(分散分析→統合オーケストレーション)を抽出するか判断

### tinyhumansai/openhuman = L3投入済み

- リポジトリ: https://github.com/tinyhumansai/openhuman
- スター数: 28.2k、フォーク: 2.6k
- ライセンス: GPL-3.0(商用利用時は要注意。組み込みではなく設計参照用途を推奨)
- ステータス: Early Beta(v0.54.0、2026-05-19リリース)
- 投入ファイル: openhuman-l3_lightrag.txt (4331 bytes)
- 評価日: 2026-05-28
- 投入方法: Claude.aiから LightRAG MCP upload_document 経由
- 判定: L3投入済み

#### 投入根拠
1. Phase 1A compression middleware開発の直接参照素材: 内蔵TokenJuiceの圧縮設計(HTML→MD、URL短縮、dedup、サマリー化、grapheme-by-grapheme保持)が現行のscripts/middleware/compression.pyの次セッション以降の拡張方針として参照価値高い。「コスト・レイテンシ最大80%削減」主張あり
2. LightRAGナレッジ管理の比較研究: Memory Tree(≤3kトークンチャンク+スコアリング+階層サマリー+SQLite+Obsidian.md出力)はLightRAGの3層構造(L0/L1/L2/L3)と異なるアプローチ。同テーマ多重投入の整理やKNOWLEDGE-INDEX再設計の参照素材
3. エージェント市場の競合分析素材: 比較表(Claude Cowork/OpenClaw/Hermes Agent/OpenHuman)はアップセル階段の提案書作成時に流用可能
4. マネージド/ローカル併用モデル: ナレッジ商品化(LightRAGをマネージド化する場合)のアーキ参照

#### 注意点
- GPL-3.0: 商用利用時にコピーレフトの制約。自社プロダクトには設計を学んで自分で書く形を推奨
- Early Beta: 本番依存は時期尚早
- マネージド前提機能の残存: 完全オンプレ運用は現状不可

#### 再評価条件
- Phase 1A compression middleware Session 4以降の実装着手時にTokenJuice実装詳細を深掘り
- ナレッジMCPサービス商品化時にMemory Tree設計を比較研究素材として参照
