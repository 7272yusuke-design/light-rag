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

---

## 2026-06-15: 過剰実装抑制パイプライン (over-engineering-guard-pipeline) — L2c投入

- **対象:** https://github.com/DietrichGebert/ponytail
- **判断:** L2c投入(過剰実装抑制パイプライン (over-engineering-guard-pipeline))
- **根拠:** ponytail（L3）を実装ガードレールとして組み込んだ過剰実装抑制パイプライン（L2c候補パターン、status:unverified）。Yusukeの構想「設計時にナレッジ参照して過剰設計を防ぐ」のうち、ponytail単体で確実に届く範囲＝実装フェーズの過剰実装抑制に絞った最小構成版。3ゲート構造: ゲート1=ponytail full常駐でYAGNI梯子による最小実装、ゲート2=/ponytail-review・/ponytail-auditでdiff監査・削除リスト適用、ゲート3=/ponytail-debtでponytail:近道の負債台帳化。pattern/combinationとして成立（context/persona/research非該当）。重複チェック: naive 2クエリで同趣旨の既存L2/L2cなし確認（過剰実装抑制の在庫はponytail-l3のみ、パイプライン化は新規）。検証状態はdesigned（未実装）のためL2c。設計フェーズの過剰設計抑制（knowledge-navigator/GSD/OpenSpecを前段に置く構成）は射程外として「将来拡張」に明記し、別L2c切り出し候補とした。
- **関連:** ponytail-l3, skill-design-patterns-l2, caveman-l3, gsd-spec-driven-l3, openspec-spec-driven-dev-l3
- **再検討条件:**
  1. 実案件でAIエージェントにコードを書かせ、このパイプラインを通した時（ponytail導入前後のコード量・不要実装の減少、/ponytail-reviewの指摘妥当性、/ponytail-debt台帳の有効性を確認しverified:selfならL2昇格）
  2. 設計ゲート（knowledge-navigator/GSD/OpenSpecを前段に置く拡張）を実装して有効性を確認する時（別L2c「最小設計パイプライン」として切り出し判断）
  3. ponytailのコマンド・モード構成が更新されパイプライン手順の見直しが必要な時
  4. caveman（出力圧縮）との併用パターンを設計する時

---

## 2026-06-17: qmd (Query Markup Documents) — L3投入

- **対象:** https://github.com/tobi/qmd
- **判断:** L3投入(qmd (Query Markup Documents))
- **根拠:** 完全ローカルで動くCLIハイブリッド検索エンジン。BM25全文+ベクトル意味検索+LLMリランクをnode-llama-cpp+GGUFでローカル実行。3モード(search/vsearch/query)、クエリ拡張(fine-tuned 1.7B、元クエリ×2重み)、RRF融合(k=60)+トップランクボーナス+位置考慮ブレンド(rank1-3=75%retrieval/rank11+=60%reranker)、スマートチャンキング(markdown境界スコアリング)、context機能、MCPサーバー(stdio+HTTP transport)、SDK利用可。Yusukeの既存タスク「LightRAG検索品質改善」に最も直接効く実装リファレンス: (1)位置考慮ブレンド/RRF重み付け/トップランクボーナスはrag-retrieval-quality-l2c・rag-pipeline-patterns-l2の具体実装例で検索キャップ調整とは別軸のretrieval品質改善ヒント、(2)Qwen3-Embedding-0.6B推奨のCJK知見は日本語ナレッジ検索の埋め込みモデル選定に直接適用可能、(3)スマートチャンキングは*_lightrag.txtのチャンク設計参考、(4)ローカルGGUF完結はOpenRouter依存(コスト・キーローテーション宿題)削減の参考、(5)context機能はKNOWLEDGE-INDEX手動エリア設計に通じる。16.5k★・MIT・Shopify CEO作で信頼性高くL3投入。LightRAGの代替ではなく検索手法の参照元（グラフ構造は持たない点を注意明記）。
- **注記:** file_name: qmd-l3_lightrag.txt（4184 bytes, upload成功・background処理中）。作者tobi=Tobias Lütke（Shopify CEO）。MIT、TypeScript81%/Python17%、16.5k★/991 fork、364 commits、9 releases（最新v2.0.1 / 2026-03-11）。重複チェック: naive 2クエリ実施、qmd自体の既存なし。ハイブリッド検索手法はrag-retrieval-quality-l2c/rag-pipeline-patterns-l2と重なる領域で具体実装例として補完関係。
- **関連:** rag-retrieval-quality-l2c, rag-pipeline-patterns-l2, lightrag-framework-l3, rag-anything-l3, microsoft-graphrag-l3, qdrant-l3, surfsense-l3, caveman-l3
- **再検討条件:**
  1. LightRAGの検索品質改善（retrieval精度・L2比率とは別軸）で位置考慮ブレンド/RRF重み付け/トップランクボーナスの融合戦略を参照する時
  2. 日本語ナレッジ検索の埋め込みモデル選定（Qwen3-Embedding等への切替）を検討する時
  3. *_lightrag.txt投入ドキュメントのチャンク設計を見直す時（スマートチャンキング参考）
  4. OpenRouter依存を減らしリランク/埋め込み/クエリ拡張をローカルGGUF化する構成を検討する時
  5. KNOWLEDGE-INDEX手動エリアやcontext付与の設計をする時（qmd context機能の発想）
  6. qmdをVPSに実際に立ててLightRAGと検索品質を比較検証する時（リソース要件確認のうえ）

---

## 2026-06-19: Chroma — L3投入

- **対象:** https://github.com/chroma-core/chroma
- **判断:** L3投入(Chroma)
- **根拠:** AI向けオープンソース検索/データインフラ（ベクトルDB）。コアがRust移行済みで高速。最大の特徴はAPIのミニマルさ（実質4関数: create_collection/add/query/get）で、in-memory試作→永続化→client-serverを同一APIで地続きに移行できプロトタイピングが極めて簡単。メタデータ/全文フィルタ、Chroma Cloud（サーバーレスのベクトル/ハイブリッド/全文検索）、多言語クライアント、LangChain/LlamaIndexのデフォルト統合先。既存Qdrantとは用途が異なる軽量・プロトタイプ枠として差別化（Qdrant=高性能本番志向・詳細制御 / Chroma=開発者体験・学習コスト最小）。LightRAG本体はpgvector運用のためChromaが本番に入る余地は小さいが、アップセル「アプリ層」でのRAG試作・単発PoCを最速で立てる用途、ベクトルストア選定比較（Chroma/Qdrant/pgvector）の在庫として価値がある。28k★・Apache-2.0・デファクトの一つでL3投入。注: LightRAG検索品質改善にはqmd（融合手法・CJK・リランク）の方が直接効き、Chromaはストア選択肢であって検索手法の改善ソースではない点を明記。
- **注記:** file_name: chroma-l3_lightrag.txt（2528 bytes, upload成功・background処理中）。Apache-2.0、Rust68%/Python16%/TS7%/Go5%、28k★/2.3k fork、4378 commits、137 releases（最新1.5.9 / 2026-05-05）。重複チェック: naive 2クエリ実施、Chroma自体の既存なし。ベクトルストアはQdrant在庫済みだが用途が異なる（Qdrant=本番志向 / Chroma=軽量プロトタイプ枠）ため重複ではなく差別化して投入。
- **関連:** qdrant-l3, lightrag-framework-l3, supabase-l3, rag-pipeline-patterns-l2, rag-retrieval-quality-l2c, qmd-l3, rag-anything-l3
- **再検討条件:**
  1. 別案件・PoCで軽量にRAG/ベクトル検索を最速で試作する時（Chromaを4関数で即起動、本番化時にQdrant/pgvectorへ移行）
  2. ベクトルストアの選定比較（Chroma=試作 / Qdrant=本番 / pgvector=既存スタック統合）が必要な時
  3. アップセル「アプリ層」でRAG機能のプロトタイプを作る時
  4. Chroma CloudのマネージドサーバーレスRAGを検討する時
  5. APIや永続化フォーマットがメジャー更新された時（鮮度更新）

---

## 2026-06-21: PocketBase — L3投入

- **対象:** https://github.com/pocketbase/pocketbase
- **判断:** L3投入(PocketBase)
- **根拠:** Goで書かれた1ファイルのオープンソース・リアルタイムバックエンド。組み込みSQLite+リアルタイム購読、ファイル/ユーザー管理、管理ダッシュボードUI、REST的APIを単一実行ファイルに含む。プリビルド実行ファイルで即起動、またはGoライブラリとして業務ロジックを組み込み単一バイナリ化（JS VMプラグインでJS拡張も可）。既存Supabaseとは差別化される軽量BaaS枠（Supabase=PostgreSQL+pgvectorの本格基盤・RAG統合可 / PocketBase=SQLite組み込みの超軽量単一ファイル・小規模/PoC/エッジ向き）。Chroma↔Qdrantと同じ本格vs軽量の対構造。アップセル「アプリ層」で小さな顧客向けアプリを最速で1ファイル配布する用途、BaaS選定比較の在庫として価値あり。58.3k★・MIT・成熟でL3投入。ただし(1)v1.0前で後方互換非保証の注意タグ、(2)事務・経理・顧客統合の二層記憶テーマではベクトル検索の都合でSupabaseが主役でありPocketBaseはSQLiteゆえRAG統合が弱く主役にならない点を明記し棲み分け。
- **注記:** file_name: pocketbase-l3_lightrag.txt（2738 bytes, upload成功・background処理中）。Go69%/JS24%、58.3k★/3.4k fork、2317 commits、263 releases（最新v0.38.1 / 2026-05-15）。★v1.0.0前で完全な後方互換保証なし＝注意タグ必須。重複チェック: naive 2クエリ実施、PocketBase自体の既存なし（BaaSはSupabase在庫済みで対比対象）。
- **関連:** supabase-l3, drizzle-l3, better-auth-l3, reflex-l3, qdrant-l3, chroma-l3, twenty-crm-l3
- **再検討条件:**
  1. 小規模アプリ/PoCのバックエンドを単一ファイルで最速に立てたい時・エッジ/低リソース環境に置きたい時（PocketBaseを選択肢に）
  2. BaaS選定比較（PocketBase=超軽量 / Supabase=本格pgvector）が必要な時
  3. v1.0.0に到達し後方互換が安定した時（本番採用可否の再評価）
  4. アップセル「アプリ層」で軽量な顧客向けアプリを1ファイル配布する構成を設計する時
  5. （注: 事務・経理・顧客統合の二層記憶＝構造化+意味検索の用途はSupabase+pgvector/LightRAGが主役。PocketBaseはこの用途では選ばない）

---

## 2026-06-21: last30days-skill — L3投入

- **対象:** https://github.com/mvanhorn/last30days-skill
- **判断:** L3投入(last30days-skill)
- **根拠:** 直近30日のソーシャル世論を13プラットフォーム（Reddit/X/YouTube/TikTok/Instagram/HN/Polymarket/GitHub/Threads/Pinterest/Bluesky/Perplexity/Web）横断で並列検索しエンゲージメント重み付けで合成するAgent Skill。51以上のAgent Skillsホストに対応（Claude Code/Codex/Cursor/Copilot/Gemini CLI/Windsurf/Cline/Continue/Roo/Aider-Desk/OpenCode/goose等）。v3でpre-researchブレイン（"OpenClaw"→@steipete・r/openclaw等を事前resolve）、Best Takes（ユーモア判定第二judge）、cross-source cluster merging、single-pass比較、auto-discovered competitor、GitHub person-mode、ELI5モード、shareable HTML brief、trend monitoring（--store+watchlist+briefings）を備える成熟ツール。Yusuke文脈との接続が極めて強い: (1)アップセル「アプリ層」の受託メニュー（商談前/評判監視）に直接納品できる、(2)米国SaaS中心のClaude for Small Businessに対し日本顧客にも刺さるソーシャル横断リサーチ商品として差別化可能、(3)保留中ai-sales-team-claudeとの組み合わせで商談前リサーチ→Hermes要点抽出→Supabase記録のパイプライン、(4)--store+watchlist.pyはn8nスケジュールトリガーから回す常駐自動化素材、(5)1012テスト・実エンゲージメント計測でskill-verifier構想の先行事例（hermes-agent/ponytail/cavemanと同枠）、(6)51ホスト対応はmulti-tool-skills-sharing-l2cの上位事例（ponytail13ホスト超え）、(7)HTML brief出力はSurfSense Deliverable Studioと同方向。41.5k★・MIT・成熟でL3投入。外部API/トークン多数必要・日本語ソース限定の注意タグ付き。
- **注記:** file_name: last30days-skill-l3_lightrag.txt（4929 bytes, upload成功・background処理中）。MIT、Python98%、41.5k★/3.4k fork、623 commits、14 releases（最新v3.3.0 / 2026-05-17）、1012テスト。GitHub Trending #1取得実績。重複チェック: naive 2クエリ実施、last30days自体の既存なし。在庫deep-research-l3とソーシャル横断リサーチで部分重複あるが「直近30日特化・エンゲージメントスコアリング・13ソース・51ホスト対応・Polymarket等独自源」で明確に差別化、補完関係として投入。
- **関連:** deep-research-l3, hermes-agent-l3, ponytail-l3, caveman-l3, multi-tool-skills-sharing-l2c, claude-for-small-business-l3, ai-sales-team-claude, n8n-l3, surfsense-l3, awesome-agent-skills-l3
- **再検討条件:**
  1. アップセル「アプリ層」で商談前リサーチ/評判監視を顧客に納品する商品を設計する時（last30daysを基準点に）
  2. 保留中のai-sales-team-claudeとの組み合わせ（商談前→Hermes→Supabase）のパイプラインを実装する時
  3. n8nスケジュールトリガー+last30days watchlistで顧客向け常駐リサーチ自動化を組む時
  4. skill-verifierの客観スコアリング設計で1012テスト・エンゲージメント計測手法を参照する時
  5. HTML brief出力の成果物形式をSurfSense Deliverable Studio等と比較する時
  6. 日本向け受託でソーシャル横断リサーチを商品化する時の鍵管理・課金モデル設計時（外部API多数の運用論点）
  7. 日本語ソース対応（2ch/5ch/Yahoo知恵袋等）が拡張される時（最終確認日2026-06-16の鮮度更新）
  8. ponytail/caveman/hermes-agentとの「客観スコアリング先行事例」L2c化を検討する時

---

## 2026-06-29: GraphAnything — 保留

- **対象:** https://github.com/InternScience/GraphAnything
- **判断:** 保留(GraphAnything)
- **根拠:** 何でもナレッジグラフ化するツール（10 schema presets / 8 extractors / 9 render formats / 17 MCP tools / 19 CLI sub-commands / federation / provenance / 増分更新）。設計はLightRAG/GraphRAGの弱点（暗黙スキーマ・provenance弱い・federation不可・外部出力なし）に正面から答える。Yusukeの「GraphRAGの課題を解決する可能性」「Notion×Supabase×LightRAGアーキテクチャの前処理候補」という観点で補完価値あり。ただし(1)Star 15/1 commit/リリースなしで信頼性未確立・README機能と実装の乖離可能性、(2)LightRAGをすでに事業基盤として運用中で出来たてOSSを焦って併用する根拠が薄い、(3)単独で見るより相方（HelixDB等のgraph-vector DB）とのセットで評価すべき。HelixDB（github.com/HelixDB/helix-db、Rust製OLTP graph-vector DB、YC出身、2026-04 GA、約4k★、AGPL）が「GraphAnything=抽出/HelixDB=実行エンジン」という綺麗な補完を構成しうるが、HelixDB自体もクレジット都合で投入保留中。よってGraphAnythingも保留として記録し、HelixDB投入時に併せて再評価する。
- **注記:** 作者: InternScience。MIT、Python 100%、Star 15・Fork 1・1 commit・リリースなし（極めて新興・未検証）。中国語READMEあり。重複チェック: naive 2クエリ実施、自体の既存なし。在庫の関連グラフ系: Microsoft GraphRAG / RAG-Anything / LightRAG / graphify / Understand-Anything / CodeGraph。コード専用4件と文書グラフ系2件で、GraphAnythingは文書グラフ系の独自ポジション。
- **関連:** microsoft-graphrag-l3, rag-anything-l3, lightrag-framework-l3, graphify-l3, understand-anything-l3, codegraph-l3, claude-obsidian-l3
- **再検討条件:**
  1. HelixDB投入時に「GraphAnything=抽出 + HelixDB=実行エンジン」の補完構成を実装検証する時（最有力の再評価タイミング）
  2. GraphAnything側でcommitが増え本番運用事例が出てきた時（半年程度後の再評価）
  3. 契約書/OpenAPI/DBスキーマなど構造が明確な文書を、明示スキーマでグラフ化する必要が実案件で出た時
  4. Notion×Supabase×LightRAGアーキテクチャで議事録/契約のprovenance（evidence_span）が経理監査の観点で必要になった時
  5. 複数顧客のグラフを後でfederationしたい受託モデルに進展した時
  6. Neo4j連携・Obsidian Canvas出力が顧客成果物として求められる時

---

<!-- 以下、mainブランチから救出した記録(2026-07-07マージ時) -->

- **出典URL**: https://github.com/rtk-ai/rtk
- **出典URL**: https://github.com/LiuMengxuan04/MiniCode
- **出典URL**: https://github.com/jeecgboot/JeecgBoot
- **出典URL**: https://github.com/microsoft/agent-lightning

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

---

## 2026-07-09: understand-anything-l3（既存エントリ更新） — 保留

- **対象:** https://github.com/Egonex-AI/Understand-Anything
- **判断:** 保留(understand-anything-l3（既存エントリ更新）)
- **根拠:** org移管（Lum1104→Egonex-AI）とv2.5→v2.7.3の大幅差分（/understand-knowledge、/understand-domain、diff影響分析、--language ja、17プラットフォーム対応、72.1k★）により既存L3エントリの全面更新を決定。更新版ドキュメント作成済みだが、MCP overwrite実装が旧doc削除でHTTP 404となり投入未完。あわせてoverwrite実装がDELETE APIに依存していることが判明（運用ルール「削除はpsql直接操作のみ」に抵触する実装）。
- **注記:** 更新版ドラフト全文は2026-07-09のClaude.aiセッション内に保存済み（過去チャット検索「Understand-Anything Egonex 更新」で取得可能）。旧エントリは無傷、重複未発生（総数221維持）を確認済み。
- **再検討条件:**
  1. 次回VPSターミナルセッション時: pg_dumpバックアップ→psqlで旧understand-anything doc削除→Claude.aiから新版をupload_documentで再投入
  2. 同セッションでmcp_remote.pyのoverwrite実装修正（DELETE API依存の解消）とrescan_documentsツール追加を検討

---

## 2026-07-10: mcp-agent-lastmile-l3 — L3投入

- **対象:** https://github.com/lastmile-ai/mcp-agent
- **判断:** L3投入(mcp-agent-lastmile-l3)
- **根拠:** Anthropic公式Building Effective Agentsの全パターン（Router/Orchestrator/Evaluator-Optimizer/Swarm等）をMCPネイティブ・コンポーザブルに実装した8.3k★フレームワーク。Agent-as-MCP-server（server-of-servers）がナレッジMCPサービスの商品進化経路（検索→エージェント提供）に直結。Temporal耐久実行とhuman-in-the-loop承認ゲートを標準装備。在庫のLangGraph（graph-first）と対極のcode-first思想で補完関係、MCP前提設計は在庫初。
- **注記:** 直前セッションで議論した「状態駆動スキル・ファシリテーター」構想（gstack発）の実装土台候補。Router/Intent Classifier=遷移判断、human-inputシグナル=承認ゲートに対応。ファシリテーター層をL2c化する際の使用ナレッジ筆頭。
- **再検討条件:**
  1. ナレッジMCPサービスのエージェント層実装に着手した時（server-of-servers構成の検証）
  2. 状態駆動スキル・ファシリテーターのL2c化・実装検証に着手した時
  3. Temporal Cloudの費用対効果検討が必要になった時（KVM2同居は非推奨のため）

---

## 2026-07-10: os-taxonomy (Marble Skill Taxonomy) — 見送り

- **対象:** https://github.com/withmarbleapp/os-taxonomy
- **判断:** 見送り(os-taxonomy (Marble Skill Taxonomy))
- **根拠:** 初等教育カリキュラムの構造化データセット（1,590 micro-topics / 3,221前提エッジDAG / ODbL+CC BY-SA）。教育ドメインは事業領域外でデータ自体の利用価値なし。ただし設計知見が高価値: ①ドメインをmicro-topic分解し hard/soft強度+理由付き前提エッジで結線するスキーマ（ナレッジ商品の体系化テンプレート）②assessmentPrompt（各トピックに習得確認の自然言語プロンプト付与、習熟度測定に転用可）③ODbLの「派生DB公開義務/成果物は自由」二層ライセンス（自社ナレッジDB商品のライセンス設計参照、HelixDB AGPL論点の隣）。
- **注記:** 本評価から派生アイデアあり: 「単一入口でスキルの組み合わせを解決するMCP」（エージェントが1ツールを呼ぶと、スキルナレッジ＋組み合わせグラフから適切なスキル構成を返す）。os-taxonomyのスキーマ（前提エッジ+エビデンス）はこのスキルグラフのデータ設計図として転用可能。関連在庫: mcp2cli / Composio / Agentic OS / mcp-agent / Smithery。
- **再検討条件:**
  1. AIエージェント開発ナレッジ（約120件）の顧客向け体系化・前提グラフ化に着手した時（スキーマ参照として）
  2. スキルリゾルバMCP（単一入口スキル組み合わせ解決）の設計に着手した時（スキルグラフのデータ設計図として）

---

## 2026-07-10: openmanus-foundationagents-l3 — L3投入

- **対象:** https://github.com/FoundationAgents/OpenManus
- **判断:** L3投入(openmanus-foundationagents-l3)
- **根拠:** MetaGPTチーム製の汎用オープンエージェント（56.4k★/MIT）。評価の決め手は4つのエントリポイント分離設計、特にrun_mcp_server.py=エージェント自体をMCPサーバー化する実装（単一入口executor型の実物）とplanning flow（意図→計画→逐次実行のプラン生成構造）。mcp-agent（SDK/部品）との役割分担が明確で補完関係。a2aプロトコル実装とOpenManus-RL（RLチューニング路線）も将来参照価値あり。
- **注記:** Skill Resolver MCP構想（単一入口スキル組み合わせ解決）のexecutor型参照実装として評価・投入。自分用v0はresolver型（ホスト実行）で構築し、商品版でrun_mcp_server.pyパターンを参照する二段構え。VPS常駐は非推奨（依存が太くKVM2に重い）、読解対象としての投入。
- **再検討条件:**
  1. Skill Resolver MCPの商品版（executor型）設計に着手した時（run_mcp_server.py読解）
  2. マルチエージェント商品でa2aプロトコル対応が必要になった時
  3. skill-verifier発展としてRLベースのエージェント改善を検討する時（OpenManus-RL）

---

## 2026-07-13: meetily-l3 — L3投入

- **対象:** https://github.com/Zackriya-Solutions/meetily
- **判断:** L3投入(meetily-l3)
- **根拠:** 完全ローカルAI議事録アシスタント(Tauri/Rust、Whisper.cpp + Parakeet、Ollama要約、MIT、★23.8k、v0.4.0)。顧客案件アーキテクチャ(Supabase + LightRAG + n8n + Hermes)における「会議音声 → 構造化議事録」の入力コネクタとして即戦力。LLMプロバイダ差し替え設計(Ollama/Claude/Groq/OpenRouter/OpenAI互換)が既存のOpenRouter運用と直結。プライバシー訴求(議事録がクラウドに出ない)が日本企業向け営業材料として直接使える。Community(MIT無償)/PRO/Enterpriseの3層商用モデルは、ナレッジMCPサービスの価格・機能分割の実例参照としても価値あり。制約: Tauriデスクトップアプリのため顧客側マシン前提、KVM2への常駐は非現実的。話者分離はPRO側機能でCommunity版に無い。
- **関連:** ffmpeg-l3 / pocketbase-l3(顧客軸の二層記憶設計) / hermes-agent-l3 / Screenpipe(未投入・要調査)
- **再検討条件:**
  1. 顧客案件で「会議議事録の自動化」が要件として上がった時点でCommunity版のPoCを実施
  2. 話者分離(誰が発言したか)が要件になった時点でPRO契約 or pyannote等の別解を評価
  3. Screenpipe(音声・画面キャプチャの借用元)を独立して評価する必要が出た時点
  4. Linux/VPS側で動く議事録パイプラインが必要になった時点(meetilyはデスクトップ前提のため別解が必要)

---

## 2026-07-13: claude-real-video — 保留

- **対象:** https://github.com/HUANGCHIHHUNGLeo/claude-real-video
- **判断:** 保留(claude-real-video)
- **根拠:** 動画をLLMに「見せる」ためのローカルCLI(Python、MIT)。固定間隔サンプリングではなくシーン変化検出 + 密度フロア + スライディングウィンドウ重複排除でフレームを選別し、Whisper文字起こしとMANIFEST.txtを添えて出力する。設計思想(知覚ハッシュではなく実ピクセル差分を使う理由、A-B-Aカットの再送防止、--reportによるkeep/drop判定の可視化)には参照価値がある。ただし成熟度が極めて低く(★14、6 commits、fork 0、単独開発者)、実体はffmpeg + yt-dlp + Whisperの薄いラッパー。ffmpeg-l3が既に在庫にあり、部品としての追加価値が限定的。VPS常駐サービスではなくCLIツールであり、現時点の顧客案件・LightRAG開発のいずれとも直接接続しない。既存ナレッジの磨き込み優先方針に照らし、今回は投入せず記録のみとする。
- **注記:** 中核となる設計思想: (1)フレーム選択はシーン変化検出 + 密度フロア(最低N秒に1枚)の併用。固定間隔は静的スクリーンキャストを過剰サンプリングし、高速カットを取りこぼす。(2)重複排除は知覚ハッシュではなく縮小RGBの実ピクセル差分。ハッシュはフラットカラーや等輝度の色変化で失明する。(3)直前フレームだけでなく直近N枚の保持フレームとの比較(スライディングウィンドウ)により、A-B-Aカットで既出ショットを再送しない。(4)字幕(.srt/.vtt/埋め込みトラック)が既にあればWhisperを回さない。この4点は、動画をLLM入力に落とす際の一般原則として再利用可能。
- **関連:** ffmpeg-l3 / vimax-l3 / remotion-l3 / text-first-on-demand-visuals-l2c
- **再検討条件:**
  1. 顧客案件でマルチモーダル入力(動画マニュアル、会議録画、店舗内装動画等)をLLMに食わせる要件が発生した時点
  2. 「マルチモーダル入力のコンテキスト削減パターン」をL2cとして書き起こす判断をした時点(ffmpeg + フレーム選択思想 + Whisperの組み合わせ)
  3. リポジトリのスター数・コミット数が伸び、実運用に耐える成熟度に達した時点
  4. Gemini等のネイティブ動画入力のコスト・精度が問題になり、前処理でのフレーム削減が必要になった時点

---

## 2026-07-13: opencut-l3 — L3投入

- **対象:** https://github.com/OpenCut-app/OpenCut
- **判断:** L3投入(opencut-l3)
- **根拠:** CapCutのOSS代替動画エディタ(MIT、★50.2k、fork 5.4k、1565 commits、v0.3.0)。動画編集機能そのものより、アーキテクチャ参照価値で投入する。(1)TypeScript → Rust/WASM のビジネスロジック移行が「進行中」の状態で観察できる希少な教材、(2)apps/desktop に GPUI(Zedエディタのフレームワーク)を採用しており、Electron / Tauri / GPUI の選定判断材料になる(meetily-l3 の Tauri と対比可能)、(3)Bun + Turborepo + Biome の新世代モノレポを★50k規模の本番で採用している実例、(4)WGSL/WebGPU によるブラウザGPU合成の実装参照、(5)docker compose up -d でセルフホスト完結、(6)OSS運営設計として Focus areas / Avoid for now を README に明示する運用が、自身のOSS公開時の参考になる。
- **注記:** 在庫の主眼は「動画編集ツール」ではなく「アーキテクチャ参照実装」。特に(1)rust/ に GPUコンポジタ・エフェクト・マスク・WASMバインディングを置き、apps/web(Next.js)と apps/desktop(GPUI)の両方に供給する単一コア多面展開、(2)bun link によるローカルWASMパッケージ差し替え手順、(3)README で Focus areas / Avoid for now を明示するコントリビュート誘導設計 の3点。顧客案件(n8n / LightRAG / 顧客DB統合)とは直接接続しない。KVM2ではGPUコンポジタが本体のため本番ホスティング非現実的。プレビューパネルとエクスポートはリファクタ中(新バイナリレンダリング方式へ移行中)のため、当該領域のコード参照は近い将来変わる前提で読むこと。
- **関連:** remotion-l3(コードで動画生成、用途が異なる) / ffmpeg-l3(下層) / meetily-l3(Tauri vs GPUI のフレームワーク対比) / claude-real-video(保留、動画→LLM入力)
- **再検討条件:**
  1. Rust/WASM をフロントエンドに組み込む案件・自作ツールが発生した時点で rust/wasm の構成と bun link 手順を実装参照する
  2. デスクトップアプリのフレームワーク選定(Electron / Tauri / GPUI)が必要になった時点で apps/desktop を評価する
  3. 顧客に「セルフホスト動画編集環境」を提供する要件が出た時点で、GPU付きホスティングのコストを含めて評価する
  4. スポンサーの fal.ai 連携によるAI動画編集機能が実装された時点で、AI機能部分を再評価する
  5. 自身のOSS公開時に、コントリビュート誘導設計(Focus / Avoid の明示)を参照する

---

## 2026-07-13: intent-driven-skill-resolution-l2c — L2c投入

- **対象:** https://github.com/affaan-m/ECC
- **判断:** L2c投入(intent-driven-skill-resolution-l2c)
- **根拠:** ECC v2.0.0(affaan-m/ECC、MIT)から抽出した「意図駆動スキル解決 + 段階的インストール」のパターン。設計中の Skill Resolver MCP(resolve_skills / install_skill / backfill_skills)に対する直接的な先行事例であり、比較対象として最も価値が高い。特に(1)`npx ecc consult "<intent>"` が resolve_skills とほぼ同一UXでありながら「候補 + profile + 導入コマンド」をセットで返す点、(2)install-plan / install-apply の2相分離により dry-run / preview が成立する点(現行の install_skill 設計には無い)、(3)SQLite install-state による状態記録が「安全なアンインストール」の前提条件になっている点(backfill_skills 設計時に逆操作の可能性を最初から入れるべき)、(4)profile / module / capability の3層スコープが registry の status 1軸より豊かである点、の4つが設計に直接効く。上位原理は L0-007(Progressive Disclosure)であり、本パターンはそれをインストール層まで拡張したものとして位置づけられる。
- **注記:** status:unverified(OSS読解ベース、自環境での実装検証は未実施)。パターン構成4段: 段1=意図から候補を解決する単一エントリ(npx ecc consult "<intent>" → 候補 + profile + 導入コマンドをセットで返す。カタログ全体を利用者に見せない)。段2=profile / module / capability の3層スコープ(既定は最小、ランタイム介入するフックはオプトイン、--with/--without の両方向)。段3=install-plan.js(計画) → install-apply.js(適用)の2相分離 + SQLite install-state記録(これがあるから doctor / repair / uninstall --dry-run が成立する。状態記録なしのインストーラは原理的に安全に消せない)。段4=導入経路の単一化(「Do not stack install methods」+ クリーンアップ順序の規定)。併走: MCP既定コネクタを6→1に削減した2026-06監査、MCP<10 / tools<80 の運用上限。Skill Resolver MCP設計への最大の含意は「解決とインストールの間に dry-run / preview の相を挟めるか」が安全性の分かれ目になる点。
- **関連:** ecc-l3(本体、v2.0.0への更新は保留中) / instinct-based-continuous-learning-l2c(同じECC由来) / awesome-agent-skills-l3(スキルカタログの類例) / L0-007 Progressive Disclosure(上位原理)
- **再検討条件:**
  1. Skill Resolver MCP に「解決 → preview → 適用」の2相分離を実装し動作確認した時点でL2昇格を判定する
  2. install-state 相当の状態記録を実装し、逆操作(uninstall / rollback)の成立を確認した時点でL2昇格を判定する
  3. ECC の `npx ecc consult` 内部実装(埋め込み検索 / キーワードマッチ / LLM呼び出しのいずれか)を確認できた時点で、resolve_skills の実装方式選定に反映する
  4. 自環境のMCP数・ツール数がコンテキストを圧迫している兆候が出た時点で、ECC同様のコネクタ監査(既定6→1削減)を実施する

---

## 2026-07-15: crewai-skills — 保留

- **対象:** https://github.com/crewAIInc/skills
- **判断:** 保留(crewai-skills)
- **根拠:** 3つの理由で今回は投入せず記録のみとする。(1)CrewAIが現在のスタック(n8n / LightRAG中心)の主軸ではなく、CrewAI採用案件が無い限り中身(CrewAI固有のRole-Goal-Backstory、Flow設計等)の直接的な参照価値が低い。(2)スキル集/スキルマーケットプレイスのパターンは既に在庫5件(mattpocock-skills / daymade-skills / awesome-agent-skills / obsidian-skills / skill-creator)でカバー済みで観点が飽和気味。「公式ベンダー配布」という差分だけでは新規投入の必要性が弱い。(3)成熟度が低い(★29、fork 9、12 commits、リリースなし)。既存ナレッジの磨き込み優先方針に照らし、パターンの存在のみ記録してCrewAI採用時に再訪する。
- **注記:** CrewAI公式(crewAIInc org)が配布するAgent Skills形式のスキル集。中身は3スキルのみ: getting-started(抽象度選択 LLM.call/Agent.kickoff/Crew.kickoff/Flow、CLIスキャフォールド、YAML設定)、design-agent(Role-Goal-Backstory、LLM選択、ツール割当、max_iter/max_rpm等チューニング、memory/knowledge sources、guardrails)、design-task(タスク記述、context依存、構造化出力 output_pydantic/output_json/output_file、human-in-the-loop、async)。各スキルは SKILL.md + references/(tools catalog、MCP servers、structured output patterns)の構造。配布はClaude Codeプラグイン(/plugin marketplace add crewAIInc/skills → /plugin install crewai-skills@crewai-plugins)、.claude-plugin/marketplace.json 駆動。MIT。パターンとして新しいのは「フレームワーク公式ベンダーがAgent Skills形式でベストプラクティスを配布する」点。SKILL.md + references/ の分離構造は、Skill Resolver MCP設計時に公式配布スキルの実例として1つ参照する価値はある。
- **関連:** mattpocock-skills-l3 / daymade-skills-l3 / awesome-agent-skills-l3 / obsidian-skills-l3 / skill-creator-l3 / intent-driven-skill-resolution-l2c(Skill Resolver設計文脈)
- **再検討条件:**
  1. CrewAI を採用する案件・自作エージェントが発生した時点で、3スキルの内容(抽象度選択・エージェント設計・タスク設計)をL3投入対象として再評価する
  2. Skill Resolver MCP の設計で「公式ベンダーが配布するSKILL.md + references/ 構造」の実例を1つ手元に置く必要が出た時点
  3. CrewAI公式がスキル数を増やし、フレームワーク公式スキル集として在庫価値のある規模に育った時点
  4. 「フレームワーク公式がAgent Skillsを配布する」動きが他ベンダー(LangChain等)にも広がり、パターンとして独立したL2c化の価値が出た時点

---

## 2026-07-16: claude-code-templates-l3 — L3投入

- **対象:** https://github.com/davila7/claude-code-templates
- **判断:** L3投入(claude-code-templates-l3)
- **根拠:** ★28.2k/fork 2.9k/1264 commits/v1.28.3 と成熟・活発。既存のスキル集在庫(mattpocock-skills/daymade-skills/awesome-agent-skills/obsidian-skills/skill-creator)と観点が重ならない差分が3つ明確(合成インストール/運用監視レイヤー/アグリゲーター構造)。特にSkill Resolver MCP設計にとって、ECC(intent-driven-skill-resolution-l2c、意図駆動)に次ぐ第2の先行事例となり、「意図駆動 vs カタログ明示選択」「単一 vs 合成インストール」の設計判断を対比で明確化できる。加えて --chats --tunnel の Cloudflare Tunnel モバイル監視が既存インフラ(Named Tunnel + mobile運用)と接続し、外部OSSアグリゲーションのライセンス継承モデルがナレッジMCP商品化時の参考になる。単なるスキル集ではないため、在庫飽和の懸念(crewai-skills保留の理由)には該当しない。
- **注記:** aitmpl.com。Claude Codeの6コンポーネント種別(Agents/Commands/MCPs/Settings/Hooks/Skills)を単一CLIで合成インストールできるカタログ + 運用監視ツール群 + 外部OSSアグリゲーター。中核3点: (1)合成インストール(npx claude-code-templates@latest --agent X --command Y --mcp Z --yes で多種を一括投入)。ECCの意図駆動(npx ecc consult)とは対極の「カタログ明示選択 + 合成」UX。(2)運用監視レイヤー(--analytics リアルタイムセッション監視、--chats --tunnel で Cloudflare Tunnel経由モバイル遠隔監視、--health-check、--plugins)。これは他スキル集在庫に無い観点で、既存の Named Tunnel + mobile運用と発想が一致。(3)アグリゲーター構造(anthropics/skills、obra/superpowers、wshobson/agents、K-Dense scientific-skills 等をライセンス継承 + アトリビューション付きで束ねる。外部OSS商品化時のライセンスモデル参照)。Python主体 + cli-rust/ 併設 + Vercel/Neon/Cloudflare Workers。制約: Claude Code専用(クロスハーネスではない)、カタログが大きいが意図駆動の絞り込みは薄く選択問題自体は未解決、束ねた外部OSSの品質はまちまち。
- **関連:** intent-driven-skill-resolution-l2c(意図駆動 vs 明示選択の対比) / everything-claude-code-l3 / ecc-l3(doctor/consultとの対比) / mattpocock-skills-l3 / daymade-skills-l3 / awesome-agent-skills-l3(束ねられる側) / smithery-smithery-ai-l3(MCPカタログ類例) / crewai-skills(保留)
- **再検討条件:**
  1. Skill Resolver MCP の install_skill を設計する時点で、--agent X --command Y --mcp Z の合成インストール実装(cli-tool/)を参照する
  2. Claude Code セッションのモバイル遠隔監視を自環境に導入する時点で --chats --tunnel の実装を参照する
  3. ナレッジMCPで外部OSSを束ねて商品化する判断をした時点で、本リポジトリのアトリビューション/ライセンス継承実装を参照する
  4. Skills種別(Plugin Skills Support、v1.28.3)が成熟した時点で Skills配布部分を再評価する
  5. cli-rust/ が主軸化した時点で、Python→Rust移行事例として再確認する

---

## 2026-07-16: claude-mem-l3 — L3投入

- **対象:** https://github.com/thedotmack/claude-mem
- **判断:** L3投入(claude-mem-l3)
- **根拠:** LightRAGプロジェクトの中核テーマ(エージェント永続メモリ/3層記憶/Progressive Disclosure/トークン効率検索)と今回の一連で最も強く重なる参照実装。★86.9k/fork 7.5k/2136 commits/296リリース/Apache-2.0と巨大・超活発・組み込みやすいライセンス。特に3層検索ワークフロー(search→timeline→get_observations)がLightRAG /query/data と Skill Resolver の index先行設計の外部実装リファレンスになり、L0-007の実装例として直接効く。Hermes/OpenClawに明示対応し日本語モード内蔵で、自環境の主要プロジェクトと直接接続する。Chroma+SQLite FTS5ハイブリッドがLightRAGのpgvector+グラフに対する別アプローチの比較対象になる。CMEMトークンの存在は技術本体と切り離して中立記録し、投入判断には影響させない。
- **注記:** セッション横断の永続メモリ圧縮システム。ツール使用をライフサイクルフックで捕捉→AI要約→SQLite+Chromaに格納→次セッションで関連文脈注入。最重要の再利用ポイントは3層検索ワークフロー(MCP 4ツール): search(index約50-100tok/結果、ID付き、type/date/projectフィルタ)→timeline(前後の時系列文脈)→get_observations(フィルタ済みIDのみ詳細約500-1000tok/結果、バッチ)。「index先行→詳細オンデマンド」で約10xトークン節約。これは自環境のLightRAG /query/data(生データ返却→Claude側合成)とSkill Resolverのindex先行設計と同型で、L0-007 Progressive Disclosureの実装リファレンスとして最良。他の対応: SQLite+observations/summaries=L0-006 3層メモリの外部実装、Chroma+SQLite FTS5ハイブリッド=LightRAG pgvector+グラフの別アプローチ比較対象、<private>タグで機密除外=顧客情報境界ルールと同発想、5ライフサイクルフック自動捕捉=loop-architectの題材。Hermes/OpenClaw明示対応、日本語モードcode--ja内蔵。構成: Claude Agent SDK+TypeScript、Bunランタイム、Workerサービス(HTTP API+Webビューア)、uv。v3→v5アーキテクチャ進化がドキュメント化。ragtime/ディレクトリ(RAG別モジュール、要精査)。【重要な注意】READMEにCMEM暗号トークン記載(第三者発行・作者公認のコミュニティトークン、Official BASE CA: 0x76b1967...)。技術本体(Apache-2.0)とは別レイヤーだが、商用文脈で顧客紹介時はノイズ/懸念材料として認識すること。KVM2常駐コストは要実測(既にLightRAG+PG+Ollama+MCP常駐中)。npm -g は SDKのみで機能しない罠あり。v13系で296リリース、仕様変更頻繁の可能性。
- **関連:** L0-006 3層メモリアーキテクチャ / L0-007 Progressive Disclosure / intent-driven-skill-resolution-l2c(index先行で同型) / hermes-agent-l3 / everything-claude-code-l3 / ecc-l3 / rowboat-l3 / claude-code-templates-l3 / LightRAG本体(pgvector+グラフ、ハイブリッド検索比較対象)
- **再検討条件:**
  1. Skill Resolver MCP / LightRAG検索の「index先行→詳細オンデマンド」を実装・改良する時点で3層検索ワークフロー(search/timeline/get_observations)の実装を参照する
  2. Hermes に永続メモリを持たせる要件が出た時点でHermes対応部分を評価する
  3. OpenClaw に永続メモリを組み込む判断をした時点で openclaw.sh インストーラと openclaw/ を精査する
  4. LightRAG(pgvector+グラフ)の代替・補完として Chroma+SQLite FTS5 ハイブリッドを検討する時点で search-architecture を比較する
  5. ragtime/ モジュールの精査が必要になった時点
  6. メモリシステムのアーキテクチャ設計判断が必要になった時点で v3→v5 の architecture-evolution を教材として読む
  7. claude-mem を実際に自環境へ導入検討する時点で、KVM2の追加常駐コスト(Worker+Chroma+uv)を実測する

---

## 2026-07-16: stop-slop-l3 — L3投入

- **対象:** https://github.com/hardikpandya/stop-slop
- **判断:** L3投入(stop-slop-l3)
- **根拠:** ★13.9k/fork 981とスキル文書として高認知。実用と教材の両面で価値あり。(1)note.com収益化パイプラインの記事生成の最終工程にAI臭除去の推敲を挟むと品質が上がり、既存 sns-writing-rules-l3(書き方ルール)と補完関係(あちらは「どう書くか」、こちらは「AI臭をどう抜くか」)。(2)SKILL.md + references/ + 採点ルーブリックの構成がProgressive Disclosure(L0-007)準拠の純テキストスキル設計テンプレートとして参照でき、skill-creatorでスキルを作る際の構造見本になる。(3)5次元採点ルーブリックは言語非依存の文章品質自己評価フレームワークとして単独でも有用。日本語適用の限界(phrases.mdは英語前提)は明示済みで、日本語AI臭スキルを自作する際の下敷きにもなる。純テキストで軽量、在庫コストが低い。
- **注記:** 散文からAI臭(AI tells)を除去するスキル。コード無しの純テキストスキル(SKILL.md + references/phrases.md + structures.md + examples.md)。検出対象: 禁止フレーズ(喉払い開始・強調松葉杖・ビジネスジャーゴン・全副詞・曖昧断定・メタコメンタリー、※英語前提)、構造的クリシェ(二項対比・否定的列挙・劇的断片化・修辞的お膳立て・偽りの主体性・遠くの語り手・受動態、※言語をまたぎやすい)、文レベルルール(Wh-文頭禁止・em dash禁止・スタッカート断片化禁止・安易な極端禁止・能動態必須)。採点ルーブリック5次元各1-10(Directness/Rhythm/Trust/Authenticity/Density)、35/50未満で改稿。この採点軸は言語非依存で流用可能。価値2軸: (1)コンテンツ=文章生成の最終工程(推敲)に挟むAI臭除去ルール、(2)スキル構造=SKILL.md + references/ オンデマンド読込 + 採点ルーブリックの型がProgressive Disclosure準拠の純テキストスキル設計テンプレート。【重要注意】phrases.mdは英語のAI臭であり日本語出力にそのまま効かない(日本語版の作成が必要)。structures.mdと採点軸は日本語適用可。「AI検出回避」に転用されうるが顧客提供時は品質向上ツールとして位置づけ検出回避目的の訴求はしない。em dash禁止等一部は作者の文体的好み。
- **関連:** sns-writing-rules-l3(補完・書き方ルール側) / L0-007 Progressive Disclosure / skill-design-patterns-l2 / skill-creator(プロジェクトスキル) / ai-document-generation-pipeline-l2(組み込み先) / skill-verifier(採点による品質検証)
- **再検討条件:**
  1. note.com収益化パイプラインに推敲工程を追加する時点で、phrases.mdの日本語版を作成しつつ本スキルを組み込む
  2. 顧客向け文書生成の品質を上げる要件が出た時点で、structures.mdと採点ルーブリックを日本語文書に適用検証する
  3. skill-creatorで新規スキルを作る際に、純テキストスキル + references/ の構造テンプレートとして参照する
  4. 日本語のAI臭パターンを体系化する独自スキルを作る判断をした時点で、本スキルを下敷きにする

---

## 2026-07-18: wardrobe-tandpfun-l3 — L3投入

- **対象:** https://github.com/tandpfun/wardrobe
- **判断:** L3投入(wardrobe-tandpfun-l3)
- **根拠:** 規模は極小(★5)だが、既存プロジェクトスキル asset-sheet-extractor(素材シート→個別PNG切り出し・透過)および property-completion-prompt-builder(スケルトン物件→内装完成イメージ)と同系譜の「AIによる画像素材の抽出→整備→適用」パイプラインであり、在庫として位置づける価値がある。特に4点: (1)検出(Responses API)と生成(Images API)でモデルを使い分ける構成、(2)参照画像を固定して生成物の一貫性を保つ手法(model-reference.png)がproperty-completion-prompt-builderの強化に直接転用可能、(3)Web UI + エージェントスキルの二重提供という配布構造と README の "For agents" セクションが、自作ツール配布時の型として参照できる、(4)同梱スキルが生成→レビュー→保存のmaker/checker分離ループを内蔵しておりloop-architectの設計思想と一致。EC商品画像の整備(検出→カットアウト→モデル着用)は顧客案件で発生しうる要件であり、その実装参照として在庫化する。
- **注記:** 服の写真から衣類を検出→商品カットアウト生成→モデル着用画像生成→ローカル管理するアプリ。パイプライン4段: (1)衣類検出=OpenAI Responses API(gpt-5.4-mini)、(2)カットアウト抽出=OpenAI Images API(gpt-image-2)で背景除去済み商品画像、(3)モデル着用画像生成=gpt-image-2 + data/model-reference.png(本人参照写真で人物を固定)、(4)ローカル保存=data/library.json + data/imported/。検出と生成でモデルを使い分ける設計、参照画像固定で生成物の一貫性を保つ手法が要点。配布構造が最大の参照ポイント: Web UI(Vite、localhost:5173、ドラッグ&ドロップ/編集/レビュー/再生成/承認)と Codexスキル(.agents/skills/ に import-clothes と generate-outfits の2本)の二重提供。両スキルとも生成物を自分でレビュー/検証してから保存するループを内蔵しており、maker/checker分離の発想が入っている(loop-architectと一致)。READMEに "For agents" セクションがあり、AIエージェントがこのリポジトリをユーザー向けにセットアップする場合の分岐手順(Codex経路 / Web UI経路)が明記されている。設定は環境変数でビジョンモデル・画像モデルを差し替え可能。【制約】★5/fork 0/9 commits/リリースなし/単独ホビープロジェクトで成熟度は最低レベル。ドメイン(ファッション)は顧客案件と直結せず、価値はパイプライン設計と配布構造の側。OpenAI API完全依存でローカルモデル差し替え経路なし。モデル着用生成は本人の顔写真を扱うため顧客提供時は肖像・個人情報の論点。スキルはCodex向け(.agents/skills/)でClaude Codeの.claude/skills/とはパスが異なる。汎用部品として抽出できるコードは薄く、参照するのは設計と手順。
- **関連:** asset-sheet-extractor(プロジェクトスキル、素材シート→個別PNG) / property-completion-prompt-builder(プロジェクトスキル、参照画像固定の同型手法) / loop-architect(プロジェクトスキル、maker/checker分離) / ffmpeg-l3 / claude-code-templates-l3(スキル配布構造の類例) / intent-driven-skill-resolution-l2c
- **再検討条件:**
  1. EC商品画像の整備(検出→カットアウト→モデル着用)が顧客要件として出た時点で段1-3のパイプラインを実装参照する
  2. asset-sheet-extractor を実写真入力に拡張する判断をした時点で、カットアウト生成とレビュー工程を参照する
  3. property-completion-prompt-builder で参照画像固定(model-reference相当)の手法を強化する時点
  4. 自作ツールを「Web UI + エージェントスキル」の二重構成で配布する判断をした時点で、README の "For agents" セクションと .agents/skills/ 構成を参照する
  5. gpt-image-2 の商品カットアウト品質・コストを実測する必要が出た時点
  6. 本リポジトリが成熟(スター/コミット増加)し実運用に耐える水準になった時点

---

## 2026-07-19: council-of-high-intelligence-l3 — L3投入

- **対象:** https://github.com/0xNyk/council-of-high-intelligence
- **判断:** L3投入(council-of-high-intelligence-l3)
- **根拠:** ★978/fork 103/v1.1.0。自環境のL0討議フォーマットB(SKILL側 + RAG側 + Yusuke の3者構造)の直接的な先行事例であり、それを18人・3ラウンド・強制反対機構つきで体系化したもの。特に流用価値が高いのは集団思考防止の強制機構(dissent quota / novelty gate / 70%閾値での強制steelman / anti-recursion)で、「早すぎる合意は失敗」を機構として実装した具体例は他に少ない。Problem Restate Gate は「正しい問いに立っているか」を検証する工程としてL0-002/L0-010と同じ層の示唆を持つ。Polarity Pairs は L0-004「複数案提示と比較思考」(Phase 2候補)の実装例であり「単一案押し付けは判断機会を奪う」という設計信念を構造化している。--dry-route / --dry-run が Skill Resolver の dry-run 設計と同型。20ドメイン×トライアドのマッピング表は「問題領域→必要な視点の組み合わせ」の設計資産として単独で有用。combination-architect の複数案+トレードオフ可視化の強化にも直結する。
- **注記:** 18のAIペルソナが対極ペアを組んで多ラウンド討議し、集団思考を機構で防ぐスキル(/council)。中核設計5点: (1)Polarity Pairs=メンバーを意図的な反対勢力として配置(Socrates破壊 vs Feynman再構築、Torvalds今出荷 vs Musashi完璧な瞬間を待つ、Taleb隠れたテール vs Karpathy滑らかなスケーリング曲線 等13ペア)。多様性を祈らず構造で強制する。(2)Problem Restate Gate=分析前に全員が問いを言い直し代替フレーミングを提示。「3人が異なる形で言い直したなら質問自体が問題だった」。正しい答えの前に正しい問いに立っているかを検証するゲート。(3)集団思考防止の強制機構=dissent quota(反対意見の割当)、novelty gate(既出主張を弾く)、agreement check(70%超が早期同意したら2名に強制steelman)、anti-recursion、counterfactual pass、2/3多数決+ドメイン専門家重み付け。「早すぎる合意は失敗」を機構化。(4)評決がUnresolved QuestionsとRecommended Next Stepsから始まる出力設計。全評決にFollow-Upセクションで結果追跡。(5)マルチプロバイダ自動ルーティング=Claude/OpenAI(codex)/Gemini/Ollama/NVIDIA NIMを自動検出、Polarity Pairsは別プロバイダに分散(ハード制約)、失敗時Claudeへフォールバック。同一モデルにペルソナを演じさせるのは「衣装替え」に過ぎないという思想。--dry-route でルーティング表のプレビューのみ実行(Skill Resolverのdry-run設計と同型)。3モード(Full 7ステップ/Quick 2ラウンド/Duo 2名弁証法)、20ドメイン×トライアドのマッピング表、3プロファイル(classic 18名/exploration-orthogonal 12名/execution-lean 5名)。install.sh に --dry-run あり。【制約】Shell 100%/30 commitsで実装は薄く、価値の大半はプロンプト設計と討議プロトコル。18名フルモードはトークンコスト大。歴史上の実在人物ペルソナはキャラクター性に寄るリスクと実在人物への架空発言帰属の問題があり、自作時は役割名(前提破壊役/第一原理役)への抽象化が安全。ライセンス表記がCC0とMITで混在しており商用利用前に要確認。マルチプロバイダを活かすには複数CLI(codex/gemini/ollama)が必要。討議構造は「間違った合意」を防ぐが「正しい答え」は保証しない。
- **関連:** L0討議フォーマットB(3者構造の体系化版) / L0-002 判断委譲の構造化 / L0-010 合意の有効性判定 / L0-004 複数案提示と比較思考(Phase 2候補) / combination-architect / loop-architect(maker-checker分離・停止条件) / skill-verifier(採点検証) / agency-agents-msitarzewski-l3 / tradingagents-tauric-research-l3 / intent-driven-skill-resolution-l2c(dry-runパターン)
- **再検討条件:**
  1. L0討議フォーマットBを改訂・拡張する時点で、Enforcement機構(dissent quota / novelty gate / 70%閾値での強制steelman)を導入検討する
  2. combination-architect に「複数案のトレードオフ可視化」を強化する時点で、Duo/Triadモードの構造を参照する
  3. 非エンジニア顧客向けの意思決定支援機能を商品化する時点で、Problem Restate Gate と「未解決の問いを先頭に置く評決」を参照する
  4. Skill Resolver の dry-run 設計時に --dry-route の出力形式を参照する
  5. 自作の討議スキルを作る判断をした時点で、実在人物ペルソナを役割名に抽象化した版を設計する
  6. マルチプロバイダ構成(Claude + Ollama + OpenRouter)でエージェントを分散実行する要件が出た時点
  7. 商用利用を検討する時点でライセンス表記(CC0 vs MIT)を確認する

---

## 2026-07-19: waggle-l3 — L3投入

- **対象:** https://github.com/modiqo/waggle
- **判断:** L3投入(waggle-l3)
- **根拠:** 自環境の中核テーマ「index先行→詳細オンデマンド」を、記憶層(claude-mem)や検索層(LightRAG /query/data)ではなく「エージェント間ハンドオフ層」に適用した実装であり、同じ思想が別レイヤーでどう具体化されるかを見られる点で在庫価値が高い。特に4点が直接効く: (1)「参照層はハーネスの外に座らねばならない」という論証がSkill Resolver MCPのハーネス非依存設計の判断材料になる、(2)supersede/revoke+系譜による訂正伝播がL0-010(合意の有効性判定)の実装版として参照できる、(3)消費契約--require+coverageによる「読了の証明」がskill-verifier/loop-architectの発想の拡張として新しい、(4)「全ツール応答がnextステップを運ぶ/規約ファイルの指示は腐る」が自作MCPの設計にそのまま流用できる。加えて設計規律が異常に厚く(Sans-I/O、リプレイ等価性のCI検証、単一カタログの4射影+driftテスト、差分オラクルによる実インフラ検証)、Rustでの堅牢なMCPサーバー設計の教材として質が高い。Cloudflare Workers+Durable Object per tenantは既存のCloudflare Named Tunnel運用と地続きで、マルチテナント分離の実装参照にもなる。MCP1行設定+SQLite+単一バイナリで試用コストが低い。
- **注記:** エージェント間ハンドオフを「コンテキスト貼り付け」から「約30バイトのトークン参照」に置き換えるMCPネイティブな参照層。Rust 75.9%、SQLite(~/.waggle/waggle.db)、Cloudflare Workers edge、MIT OR Apache-2.0。問題設定: マルチエージェントはチャットの約15倍のトークンを消費し、その overhead はベンダー自身が「エージェント間のコンテキスト複製とハンドオフのための要約」に帰しており、マルチエージェント失敗の約37%がこの継ぎ目に起因する。競合は他プロトコルではなく生のパス(/tmp/analysis.md)であり、パスに欠けるのは帰属・適応・ライフサイクル・テレメトリ・到達性の5つ。ベンチでは生パス+ls/grep/open/pdftotext が90%、waggleが96%で、READMEは「ローカル・短時間・監査不要ならパスを使え、waggleはオーバーヘッド」と明示。核心メカニズム: トークンは移動しアーティファクトは自動展開されず、resolve/read/search がバイト予算下で射影・スライスのみ返す(自環境のclaude-mem 3層検索・LightRAG /query/data・Skill Resolver index先行と完全に同型)。帰属マニフェスト(Ed25519署名、チャネル、親からの系譜ツリー、消費者別variants)、封印された決定論的マッチャー、ペイロードフリーな追記専用ログ。mint時コンテンツアドレス・スナップショットで不変化し supersede/revoke で全保持者に訂正が伝播(L0-010合意の有効性判定の実装版)。消費契約 --require symbol:X + coverage で「読んだことを証明」(skill-verifier/loop-architectの検証発想を参照層に持ち込んだもの)。tree-sitterによるmint時シンボル抽出(Rust/Python/TS/JS/Go)、配信パスでパーサは走らない。「参照層はいかなる単一ハーネスの外側に座らねばならない、ハンドオフは分散システムの問題であり一つのベンダーのハーネスロジック内で解くのは解けない唯一の場所で解こうとすること」という論証はSkill Resolverのハーネス非依存設計判断に直接効く。「全ツール応答が最大3つの実行可能なnextステップを運ぶ、mapが現在地を状態からライブ計算、規約ファイルの指示は腐るがエンベロープは腐らない」は自作MCPに流用可能。設計規律: Sans-I/O core(ドメインcrateに時計/エントロピー/ストレージなし、同コードがネイティブとWorkers wasmで動く)、イベントソース+リプレイ等価性のCIプロパティ、MCPツール/CLI/map/COMMANDS.mdが1表の4射影でdrift時ビルド失敗、差分オラクルで実Cloudflare上のedgeをSQLiteとバイト同一に検証。実測: cache-hit resolve 39ns、永続追記39µs、100万イベントfunnel 334µs、edge resolve p50 1.2ms。tmuxスイッチボード(waggle-tmux)でハーネス切替UI。【制約】v0.5.3/185commitsと若く仕様が動く可能性。マルチエージェント運用が実在しないと純粋なオーバーヘッド。Rust製追加常駐デーモンでKVM2の追加コストは要実測(SQLite+単一バイナリで軽量ではある)。edge運用にCloudflareアカウントとwrangler必要。15倍/37%の主張はベンダー資料由来で自環境未検証。
- **関連:** claude-mem-l3(3層検索、同型の思想を記憶層に適用) / L0-010 合意の有効性判定(supersede-revokeが実装版) / L0-007 Progressive Disclosure / intent-driven-skill-resolution-l2c / claude-code-templates-l3 / ecc-l3(クロスハーネス設計) / loop-architect / skill-verifier / LightRAG /query/data(自環境の同型実装)
- **再検討条件:**
  1. Skill Resolver MCP をハーネス非依存に設計するか判断する時点で「参照層はハーネスの外に」の論証を参照する
  2. 自作MCPのツール応答設計を行う時点で「全応答がnextステップを運ぶ/mapで現在地を答える」パターンを参照する
  3. L0-010(合意の有効性判定)を実装レベルに落とす時点で supersede/revoke+系譜ツリーの実装を参照する
  4. マルチエージェント/サブエージェント運用を実際に回し始めた時点で、ハンドオフのトークンコストを実測しwaggle導入を評価する
  5. 顧客向けマルチテナント分離を実装する時点で Durable Object per tenant + capability-URL + Ed25519 の構成を参照する
  6. Rustで堅牢なMCPサーバーを書く判断をした時点で Sans-I/O core と単一オペレーションカタログの設計を教材として読む
  7. v1.0に到達した時点で仕様の安定性を再評価する

---

## 2026-07-19: scrapling-l3 — L3投入

- **対象:** https://github.com/D4Vinci/Scrapling
- **判断:** L3投入(scrapling-l3)
- **根拠:** ★69.1k/1516 commits/48リリース/テストカバレッジ92%と極めて成熟・活発で実運用に耐える。顧客案件への接続度が高く、n8n による情報収集自動化(競合価格監視・求人情報収集・業界ニュース収集)の収集エンジンとして即戦力になる(Dockerイメージ提供済みでVPS配置が現実的、n8nのHTTP Requestノードから利用可能)。特に適応型要素追跡はサイト改修のたびにセレクタが壊れるという保守コストに直接効き、継続課金型の運用サービスと相性が良い。MCPサーバー内蔵の「抽出してからAIに渡す」設計は claude-mem / waggle / LightRAG /query/data と同じ index先行パターンのスクレイピング版であり、今セッションで揃いつつある同型事例の一つとして位置づけられる。Development Mode(レスポンスキャッシュ再生)は対象サーバーに負荷をかけずにparseロジックを反復できるため顧客案件での配慮として重要。scrapling extract get <url> content.md によるMarkdown化は、LightRAGへの外部ドキュメント取り込み前処理として現在の web_fetch 工程の代替・補完にもなる。日本語READMEあり。
- **注記:** 適応型Webスクレイピングフレームワーク(Python 99.9%、BSD-3-Clause、★69.1k/fork 6.8k/1516commits/v0.4.10/48リリース/テストカバレッジ92%/PyRight+MyPy全型ヒント)。中核6機能: (1)適応型要素追跡=auto_save=True で保存し後日 adaptive=True で類似性アルゴリズムにより構造変化後も要素を再配置。スクレイパ保守の最大コスト(サイト改修によるセレクタ破壊)に直接効く。AutoScraper比5.2倍高速。(2)anti-bot回避4系統=Fetcher(TLSフィンガープリント/ヘッダ偽装、HTTP/3)、AsyncFetcher、StealthyFetcher(Cloudflare Turnstile/Interstitial自動突破)、DynamicFetcher(Playwright Chromium/Chrome)。ProxyRotator、広告ブロック(約3500ドメイン)、DNS-over-HTTPSによるDNSリーク防止。(3)Spiders=Scrapy風API、並行クロール、チェックポイントによるPause&Resume(Ctrl+Cで停止、同じcrawldirで再開)、Streaming Mode、Multi-Session(1spider内でHTTPとステルスブラウザをセッションIDでルーティング)、Blocked Request Detection、robots_txt_obey、Development Mode(初回レスポンスをディスクキャッシュし再生。対象サーバーを叩かずparseロジックを反復開発できる)、JSON/JSONLエクスポート。(4)MCPサーバー内蔵(scrapling[ai])=Scraplingで対象コンテンツを先に抽出してからAIに渡しトークン使用を最小化。claude-mem/waggle/LightRAG /query/data と同じindex先行パターンのスクレイピング版。(5)agent-skill/ディレクトリ同梱(Claude Skill + OpenClaw Skillバッジ)。(6)CLI/IPythonシェル(scrapling shell、curl→Scrapling変換)、scrapling extract get <url> content.md で出力拡張子により .txt=テキスト / .md=Markdown / .html=HTML を切替。性能: 5000ネスト要素のテキスト抽出でBS4+Lxml比約784倍、Parsel/Scrapyとほぼ同等の2.02ms。Dockerイメージ提供(pyd4vinci/scrapling、全ブラウザ同梱、リリース毎自動ビルド)。日本語READMEあり。【重要な制約】READMEが免責を明記(教育・研究目的、データスクレイピング/プライバシー法の遵守、利用規約とrobots.txtの尊重)。anti-bot回避は諸刃で、Cloudflare Turnstile突破は技術的に可能でも対象サイト規約に反する場合がある。顧客提供時は「公開データの取得」「規約が許す範囲」に限定する運用ルールの明文化が必要。スポンサーがプロキシ業者中心。ブラウザ依存が重くKVM2でStealthyFetcher/DynamicFetcherを常用するとメモリ・CPU負荷が高いためHTTPのみのFetcherで足りるケースの見極めが必要。素のpip installはパーサーのみでfetchers/spidersはModuleNotFoundErrorになる罠あり(extras + scrapling install 必須)。Python 3.10+。
- **関連:** claude-mem-l3 / waggle-l3 / LightRAG /query/data(index先行パターンの同型事例) / n8n関連ナレッジ(収集エンジンの接続先) / crewai-skills(保留、公式Agent Skill配布の潮流) / gstack-garrytan-l3(anti-bot stealthブラウザの言及) / ffmpeg-l3
- **再検討条件:**
  1. 顧客案件で情報収集自動化(価格監視・求人収集・ニュース収集等)の要件が出た時点で n8n + Scrapling(Docker)の構成を設計する
  2. 既存スクレイパがサイト改修で壊れる問題が発生した時点で適応型セレクタ(auto_save/adaptive)への移行を評価する
  3. LightRAGへの外部ドキュメント取り込みを自動化する時点で scrapling extract によるMarkdown化を web_fetch の代替として評価する
  4. Claude Code から直接スクレイピングする要件が出た時点で scrapling[ai] のMCPサーバーを導入評価する
  5. KVM2上でブラウザ系Fetcherを常用する判断をする時点でメモリ・CPU負荷を実測する
  6. 顧客にスクレイピングを提供する契約を結ぶ時点で、利用規約・robots.txt・個人情報保護の観点から運用ルールを明文化する

---

## 2026-07-23: astrbot-l3-update-v4.25.2 — 保留

- **対象:** https://github.com/AstrBotDevs/AstrBot
- **判断:** 保留(astrbot-l3-update-v4.25.2)
- **根拠:** AstrBot は既にL3投入済みだが、既存エントリの内容が v4.25.2 時点の現況を反映していない可能性が高い。特に Yusuke案件との接続で新しく効くのは2点: (1) LINE公式サポートにより、日本の中小企業向けn8n案件で「LINEから社内ナレッジに問い合わせる」構成が現実的になり、Hermes の代替・補完候補として位置づけが変わる。(2) Agent Sandbox(コード実行の隔離、セッション単位リソース再利用)が、既存在庫 MiniClaw の4層防御パターンと対比できる具体例として加わる。加えて openspec/ + AGENTS.md の採用は、在庫の OpenSpec の実適用例として参照価値がある。ただし DELETE API 禁止(全消しバグ)かつ psql直接操作が現環境で実行できないため、既存レコードの削除→再投入ができない。重複投入は運用ルール違反になるため、更新待ちキューとして差分を記録するに留める。ECC v2.0.0更新と同じ扱いで、psql操作が可能になった時点で一括処理する。
- **注記:** 既存L3エントリ「AstrBot — IMプラットフォーム統合型オールインワン・エージェントチャットボット基盤」の更新待ち差分を記録する。現況(2026-07-13時点): ★33.7k / fork 2.3k / 4,753 commits / v4.25.2(2026-05-30) / 221リリース / contributors 319 / Python 70.4% + Vue 23.9%。ライセンスは AGPL-3.0(商用提供時に要注意、EULA.md も同梱)。

【既存エントリ作成時になかった可能性のある主な差分】
(1) Agent Sandbox — コード実行・shell呼び出しの隔離実行と、セッション単位のリソース再利用。docs.astrbot.app/use/astrbot-agent-sandbox.html に専用ドキュメント。既存在庫 MiniClaw(サンドボックスAIエージェントランタイムの4層防御パターン)と直接対比できる。
(2) Auto Context Compression — 文脈の自動圧縮が公式機能として明記。claude-mem のセッション圧縮と同系統。
(3) LINE 公式サポート — Official maintainer 扱い。日本の中小企業向け案件で「LINEから社内ナレッジに問い合わせる」構成が組める。Hermes の代替・補完候補。
(4) uv による1コマンド導入 — `uv tool install astrbot --python 3.12` → `astrbot init` → `astrbot run`。Python 3.12+必須。ただし uv 経由デプロイは WebUI からのアップグレード非対応(コマンドラインで `uv tool upgrade` が必要)。
(5) openspec/ ディレクトリ + AGENTS.md をリポジトリに同梱 — スペック駆動開発とエージェント前提の開発体制を採用。在庫の OpenSpec(スペック駆動開発フレームワーク)の実適用例として参照できる。
(6) k8s/ ディレクトリ — Kubernetesデプロイ対応。
(7) 1000+ コミュニティプラグインのワンクリック導入(マーケットプレイス、api.soulter.top でプラグイン数を動的表示)。
(8) LLMOpsプラットフォーム連携 — Dify / Alibaba Cloud Bailian / Coze と統合可能。
(9) Web ChatUI(agent sandbox + web search 内蔵)、WebUI、i18n対応。
(10) 対応IMプラットフォームの拡大 — QQ / OneBot v11 / Telegram / Wecom / WeChat公式アカウント / Feishu / DingTalk / Slack / Discord / LINE / Satori / KOOK / Misskey / Mattermost が Official、WhatsApp は Coming Soon。Matrix / Rocket.Chat / VoceChat はコミュニティ製アダプタ。
(11) STT/TTS の選択肢が豊富 — Whisper / SenseVoice / Xiaomi MiMo Omni、TTS は OpenAI / Gemini / GPT-Sovits / FishAudio / Edge / Azure / Minimax / Volcano Engine 等。VoxCPM(在庫)との比較対象。
(12) 多様なデプロイ経路 — Docker / RainYun / デスクトップアプリ(AstrBot-desktop) / Launcher / Replit / AUR / BT-Panel / 1Panel / CasaOS。
(13) 日本語README あり(README_ja.md)。

【更新できない理由】DELETE APIが使用できず(全消しバグのため禁止)、psql直接操作による既存レコード削除も現在の環境では実行できないため、既存エントリの内容更新が不可能。ECC v2.0.0更新と同じ制約。psql操作が可能になった時点で、ECC更新と合わせて処理する。
- **関連:** astrbot-l3(既存エントリ、更新対象) / ecc-l3(同じくpsql制約で更新保留中) / miniclaw(サンドボックス4層防御パターン、Agent Sandboxの対比対象) / hermes-agent-l3(LINE経路の代替・補完候補) / openspec-l3(openspec/採用の実例) / claude-mem-l3(Auto Context Compressionの同系統) / voxcpm-l3(TTS比較対象) / n8n関連ナレッジ
- **再検討条件:**
  1. psql直接操作が実行可能な環境になった時点で、ECC v2.0.0更新と合わせて既存 astrbot-l3 レコードを削除→v4.25.2内容で再投入する
  2. 日本の中小企業向け案件で「LINEから社内ナレッジに問い合わせる」要件が出た時点で、AstrBot(LINE公式対応)を Hermes の代替・補完として評価する
  3. エージェントのコード実行を隔離する要件が出た時点で、AstrBot Agent Sandbox と MiniClaw の4層防御パターンを比較する
  4. OpenSpec(スペック駆動開発)の実適用例が必要になった時点で、AstrBot の openspec/ ディレクトリ構成を参照する
  5. 商用サービスに組み込む判断をする時点で AGPL-3.0 の影響を精査する(ソース開示義務、EULA.md の内容確認)
  6. 自環境の TTS 選定時に AstrBot がサポートする TTS 群と VoxCPM を比較する

---

## 2026-07-24: claude-video-l3 — L3投入

- **対象:** https://github.com/bradautomates/claude-video
- **判断:** L3投入(claude-video-l3)
- **根拠:** 動画→LLM入力のトークン効率設計として、実測値つきで最も完成度が高い実装。特に3点が自環境に効く: (1)フレーム重複排除の実装が具体的で移植可能(16×16グレースケールの平均絶対差分、「最後に保持したフレーム」との比較によるスローフェード捕捉、予算キャップをdedupの後に適用する順序)。これは先に保留にしたclaude-real-videoの中核思想の上位互換にあたる。(2)--timestampsによる「文字起こしを先に読んで狙った瞬間だけフレーム取得」がindex先行パターンそのものであり、claude-mem/waggle/Scrapling/LightRAG /query/dataに続く5つ目の同型事例として動画入力層を埋める。(3)マルチサーフェス配布(3マニフェスト併存、SKILL.mdの相対解決による自己完結、タグpushでの.skill自動ビルドCI、サブ100msのプリフライト)がSkill Resolver/自作スキル配布の実装参照になる。加えて、YouTubeチャンネル→構造化MD→エージェント学習素材パイプラインの「抽出エンジン」として、watch-video-skillと組み合わせて使う下層部品として必要。★9k/fork 963でテスト・CI・CHANGELOGが整備されており、11 commitsという数字の割に成熟度は高い。
- **注記:** 動画をClaudeに「見せる」抽出エンジン(/watch)。MIT、★9k/fork 963/11 commits/v0.2.0。Python 94.9%。中核4点: (1)トークン予算を設計の中心に置く=動画長別フレーム予算(≤30秒→約30枚 / 1-3分→約60枚 / >10分→100枚キャップ+"sparse scan"警告)、画像トークンは(width×height)/750で512px幅の720pフレームが512×288の約197トークン/枚、--start/--endの焦点モードでは秒あたり予算が密になり最大2fps。長尺では文字起こしの方がコスト大の場合あり(49分で約26.6kテキストトークン)。(2)フレーム重複排除=1回のffmpeg呼び出しで16×16グレースケール化→以降は純標準ライブラリPython、「最後に保持したフレーム」との平均絶対差分(0-255スケール)が閾値2.0以下なら破棄、予算キャップはdedupの後に適用。直前ではなく最後に保持したフレームと比較することでスローフェードを捕捉。閾値は意図的に低く構造ではなく絶対輝度を測るため1行のコード差分やターミナルの1行スクロールは生き残る。出力に「14候補から6枚選択、8枚が近重複として破棄」と報告。(3)detail 4モードの実測値(49分08秒/1280×720/英語自動字幕): transcript=0フレーム約4.5秒ダウンロードなし、efficient=キーフレーム50枚約0.5秒約9.8kトークン、balanced=シーン変化100枚約20.9秒約19.7kトークン、token-burner=シーン変化116枚無制限約21.0秒約22.8kトークン。サンプリング規則は全モード共通で全候補検出後に均等サンプリング(最初と最後は常に保持)するため最後のフレームが必ず末尾に着地する。efficientは速度階層でシーンモードの約40倍速く、低モーション映像ではbalancedより多くフレームを返すこともある。(4)マルチサーフェス配布=Claude Codeプラグイン/npx skills add(50+ホスト)/claude.aiの.skillバンドル/手動symlink。.claude-plugin + .codex-plugin + .agents/plugins の3マニフェスト併存、SKILL.mdが自身のスクリプトを相対解決するためどのホストでも同じに動く、タグpushで.skillを自動ビルドするCI、プリフライト(setup.py --checkが初回のみ依存解決しmacOSはbrew自動実行、以降サブ100ms)。文字起こしは字幕優先→フォールバックでGroq whisper-large-v3(推奨)/OpenAI whisper-1。--timestampsで文字起こしを先に読んでから狙った瞬間だけフレーム取得できる(index先行そのもの)。【制約】成果物はチャット応答で永続ファイルを残さないため、学習素材用途には出力層を別途被せる必要がある(watch-video-skillが該当)。長尺はキャップモードで約10分超からカバレッジが薄まる。Whisperフォールバックには外部APIキーが必要。claude.ai利用時はCapabilitiesの「コード実行とファイル作成」を先に有効化する必要がある。
- **関連:** watch-video-skill-l3(本スキルのラッパー、出力層) / video-to-knowledge-pipeline-l2c(両者を組み合わせたパターン) / claude-real-video(保留、上位互換にあたる) / claude-mem-l3 / waggle-l3 / scrapling-l3 / LightRAG /query/data(index先行の同型事例) / L0-007 Progressive Disclosure / ffmpeg-l3 / meetily-l3 / claude-code-templates-l3(スキル配布の類例)
- **再検討条件:**
  1. YouTubeチャンネル→構造化MDのパイプラインを構築する時点で、本スキルを抽出エンジンとしてwatch-video-skillと組み合わせる
  2. 自作の動画処理パイプラインでフレーム選択・重複排除を実装する時点で、dedupの4ステップ(16×16グレースケール/最後に保持したフレームとの比較/閾値2.0/キャップは後適用)を移植する
  3. 自作スキルをマルチサーフェス配布する判断をした時点で、3マニフェスト併存構成とbuild-skill.sh/release.ymlを参照する
  4. 顧客案件で動画マニュアル・会議録画・不具合の画面録画をLLMに食わせる要件が出た時点
  5. 画像トークンのコスト試算が必要になった時点で(width×height)/750と49分動画の実測表を参照する
  6. Groq whisper-large-v3のコスト・精度を評価する必要が出た時点
  7. ネイティブ動画入力が安価になり前処理が不要になった時点で、本エンジンの必要性を再評価する

---

## 2026-07-24: watch-video-skill-l3 — L3投入

- **対象:** https://github.com/Newuxtreme/watch-video-skill
- **判断:** L3投入(watch-video-skill-l3)
- **根拠:** 計画中の「YouTubeチャンネル→エージェント学習用MDファイル出力パイプライン」において、出力層として必須の役割を担う。下層の抽出エンジン(claude-video)はチャット応答で終わるため成果物が残らないが、学習用途で決定的なのは「成果物が残るか」である。本スキルが書き出す構造化MDは、後で読み返せる/他ノートからリンクできる/別エージェントに食わせられる/既存のupload_document投入経路にそのまま流せる、という4点で資産になる。出力の5点構造(一行要約/TL;DR/タイムスタンプ付きタイムライン/キー引用/ビジュアルノート)はそのまま知識単位として機能し、特にビジュアルノートはテキスト字幕だけでは失われる画面情報を保存する。動画長に応じたサンプリング指示(短=全フレーム/中=5秒/長=10秒)がコンテキストウィンドウへの力任せな詰め込みを防ぎ、ノート書き出し時のtempフォルダ自動消去がバッチ処理・無人運用を前提とした設計になっている。manifest.jsonが中間フォーマットとして後段の変換に使える。★1という数字で判断すべきエントリではなく、評価軸はパイプライン適合性である。作者自身が下層との役割分担を明記しており、組み合わせ前提の設計であることが明確。
- **注記:** 動画を構造化Markdownノートに変換するClaudeスキル。MIT、★1/fork 0/7 commits/リリースなし、Python 100%。構成はSKILL.md + scripts/extract_video.py。Claude Code / Claude Desktop / Claude Agent SDK 対応。【重要】bradautomates/claude-video のラッパーであり、作者自身が「ラッパーなしの純粋なBradパイプラインが欲しければ bradautomates/claude-video を入れるべき、あれは優秀」と明記している。両者は競合ではなく役割分担(Brad版=抽出エンジン / 本スキル=出力層)。核心的な差分は出力形態: Brad版はチャットで答えて終わりセッションと共に消えるが、本スキルは実体のあるMarkdownファイルを書き出す。出力MDの5点構造=一行要約 / TL;DR / タイムスタンプ付きタイムライン / キー引用 / ビジュアルノート。特にビジュアルノートは字幕だけでは失われる画面情報(コード・UI・図表)を保存する。処理は4段: 文字起こし取得(YouTube字幕優先→ローカルWhisperフォールバック)→ffmpegで設定可能間隔のフレーム抽出→各フレームをその時刻に話されている文と整列→Claudeがフレーム+文字起こしを読みMDノート書き出し。動画長に応じたフレームサンプリング指示(短い=全フレーム / 中程度=5秒ごと / 長い=10秒ごと)により、Claudeが全フレームをコンテキストウィンドウに力任せに詰め込むことを防ぐ。ノートファイル書き出し時にtempフォルダを自動消去するため、バッチで繰り返し回しても中間生成物が溜まらない。CLI単独利用も可能で python scripts/extract_video.py "<url-or-path>" --output-dir ./out --interval 1.0、フラグは --interval N / --whisper-model tiny|base|small|medium|large / --no-whisper。manifest.json(フレームパス+タイムスタンプ+整列済み文字起こしセグメント)を出力し、これがパイプラインの中間フォーマットとして使える。作者が挙げる用途4つ: オンボーディング、チュートリアル学習、show-don't-tellによるコンテンツ生成、編集スタイルのクローン(Remotion/Hyperframesと組み合わせてClaude Codeから動画編集)。【制約】★1/7 commits/単独作者で成熟度指標は最低レベルだが、本エントリの評価軸は人気度ではなくパイプライン適合性である。ラッパーゆえ下層(Brad版)の進化に追随できないリスクがあり、Brad版がv0.2.0でdetailモードとdedupを導入した一方で本スキルは--intervalの固定間隔サンプリングが基本。将来的にはBrad版の出力に自前のMD書き出しを被せる自作構成の方が保守しやすい可能性がある。Windows+Python 3.12/3.13でpipがyt-dlp/whisperのインストールに失敗する既知問題(Python 3.9を入れてpy -3.9 -m pip install --user yt-dlpで回避)。yt-dlpがYouTube Shorts/年齢制限で失敗することがありandroidプレイヤークライアントへフォールバックするがメンバー限定・地域制限は失敗しうる。ローカルWhisper使用時はKVM2でのバッチ処理が現実的でない可能性が高く字幕優先経路の確保が必要。
- **関連:** claude-video-l3(下層の抽出エンジン、本スキルはそのラッパー) / video-to-knowledge-pipeline-l2c(両者を組み合わせたパターン) / meetily-l3(音声→構造化議事録、本スキルの動画版という対の関係) / claude-real-video(保留) / remotion-l3(編集スタイルのクローン用途) / stop-slop-l3(生成MDの推敲工程) / ffmpeg-l3 / L0-007 Progressive Disclosure
- **再検討条件:**
  1. YouTubeチャンネル→構造化MDのパイプラインを実装する時点で、Brad版と組み合わせた構成を設計・検証する(検証後 video-to-knowledge-pipeline-l2c のL2昇格判定を行う)
  2. 出力MDをupload_documentでLightRAGへ自動投入する経路を組む時点で、MD構造とL3テンプレートの対応を設計する
  3. Brad版が進化してラッパーが追随できなくなった時点で、Brad版の出力に自前のMD書き出しを被せる自作構成への移行を検討する
  4. 動画編集スタイルのクローン(用途4)を試す時点でremotion-l3と組み合わせる
  5. バッチ処理でチャンネル全体を回す時点で、KVM2上のWhisper負荷を実測し字幕優先経路を確保する
  6. 生成されたMDノートの品質向上が必要になった時点でstop-slop-l3を後段の推敲工程として接続する

---

## 2026-07-24: video-to-knowledge-pipeline-l2c — L2c投入

- **対象:** https://github.com/bradautomates/claude-video + https://github.com/Newuxtreme/watch-video-skill
- **判断:** L2c投入(video-to-knowledge-pipeline-l2c)
- **根拠:** 計画中の「YouTubeチャンネル→エージェント学習用MDファイル出力パイプライン」を、2つのL3(claude-video / watch-video-skill)の組み合わせとして構造化したパターン。単独のL3では捉えられない設計判断—特に「抽出エンジンと出力層を別部品として分離する」という中核判断—を独立したパターンとして記録する必要がある。この分離は、エンジン側が速く進化し出力構造が安定しているという性質の違いに基づいており、将来ネイティブ動画入力が安価になった際にエンジンだけを置換できるという可搬性を生む。加えて本パターンは、自環境で既に4つ揃っているindex先行パターン(LightRAG /query/data=検索層、claude-mem=記憶層、waggle=ハンドオフ層、Scrapling=収集層)の5つ目として動画入力層を埋めるものであり、L0-007 Progressive Disclosureが複数レイヤーを貫いていることの追加証拠になる。パイプライン未構築のためstatus:unverifiedのL2cとして投入し、実装・実測後にL2昇格を判定する。
- **注記:** status:unverified(OSS読解+設計構想ベース、自環境でのパイプライン構築・実測は未実施)。解決する3つの問題: (1)成果物が残らない(動画を見せて質問する形式は答えがセッションと共に消え、次回また処理し直す)、(2)コンテキスト破裂(30分動画を1fpsで取れば1800枚、512px幅で約35万トークン)、(3)重複フレームへの課金(90秒間1枚のスライドから十数枚のほぼ同一画像)。パターン構成4段: 段1=抽出エンジン(字幕最優先で字幕付きURLなら動画本体をダウンロードせず文字起こしのみ取得、Whisperは字幕が本当に無い場合のフォールバックに限定、動画長別フレーム予算、時刻指定時は焦点モードへ切替、画像トークンは(width×height)/750で見積もり、解像度を上げるのは画面上のテキストを読ませる必要がある時だけ、長尺では文字起こしの方がコスト大の場合があるためフレームだけ見て最適化しない)。段2=フレーム重複排除(16×16グレースケール化して標準ライブラリのみで比較、平均絶対差分が閾値以下なら破棄、比較対象は直前ではなく「最後に保持したフレーム」にしてスローフェードを捕捉、予算キャップはdedupの後に適用、閾値は意図的に低く絶対輝度を測ることで1行のコード差分やターミナルの1行スクロールを生き残らせる、何枚畳み込まれたかを出力に含めて挙動を観測可能にする)。段3=出力層(構造化MDとして永続化。5点構造=一行要約/TL;DR/タイムスタンプ付きタイムライン/キー引用/ビジュアルノート。ビジュアルノートは字幕だけでは失われる画面情報を保存。加えて書き出し後にtempフォルダ・抽出フレーム・音声クリップを自動消去。バッチ前提なら掃除を設計に含めないとディスクが埋まる)。段4=投入層(ナレッジベース/他ノートからのリンク/別エージェントの学習素材。中間フォーマットとしてmanifestを持たせると後段で別形式に変換できる)。中核設計判断=エンジンと出力層の分離: エンジンは「コストと忠実度のトレードオフ」を最適化し進化が速い、出力層は「後工程での再利用性」を最適化し出力構造は安定している。分離することでエンジンが進化しても出力構造は変わらず、出力形式の変更時にエンジンを触らずに済み、将来ネイティブ動画入力が安価になったらエンジンだけ置換して出力層を残せる。分離しない場合の失敗は「動画を見て答える」ツールをそのまま学習素材生成に使い資産が蓄積しないこと。参照実装はbradautomates/claude-video(抽出エンジン、★9k)+ Newuxtreme/watch-video-skill(出力層、★1)だが、★の数で判断してはならず評価軸はパイプライン適合性である。ラッパー構成には追随リスクがあり、将来はエンジンの出力に自前MD書き出しを被せる自作構成の方が保守しやすい可能性がある。上位原理はL0-007 Progressive Disclosureで、本パターンは「必要な分だけ渡す」を動画入力層に適用したもの。特に強力な運用は「先に文字起こし(テキスト、安い)を読ませ、発表者が『ここを見てください』と言っている箇所を特定してからその時刻だけフレームを取る」というindex先行の適用。
- **関連:** claude-video-l3(抽出エンジンの参照実装) / watch-video-skill-l3(出力層の参照実装) / meetily-l3(音声→構造化議事録、本パターンの音声版という対の関係) / claude-mem-l3 / waggle-l3 / scrapling-l3 / LightRAG /query/data(index先行の同型事例) / L0-007 Progressive Disclosure(上位原理) / stop-slop-l3(生成MDの推敲工程) / claude-real-video(保留) / ffmpeg-l3 / remotion-l3
- **再検討条件:**
  1. YouTubeチャンネル(または複数動画)に対してパイプラインを実際に構築し構造化MDを生成した時点でL2昇格を判定する
  2. 生成MDをupload_documentでナレッジベースに投入し検索で引けることを確認した時点
  3. トークンコストと所要時間を実測した時点(素朴な全フレーム投入との比較があるとなお良い)
  4. 段2(dedup)と段3(構造化出力)が実際に効いていることを削減率などの数値で確認した時点
  5. 出力MDの5点構造とL3テンプレートの対応を設計する時点(そのまま投入できるか変換が必要かの判断)
  6. KVM2でチャンネル全体をバッチ処理した際の所要時間・ディスク・CPU負荷を実測する時点
  7. ラッパー構成から自作構成への移行を判断する時点
  8. 重複判定の閾値が日本語スライドや低コントラスト映像で妥当か検証する時点
  9. 投入粒度(動画1本=1エントリか、チャプター単位で分割するか)を決定する時点

---

## 2026-07-24: mcpsnoop-l3 — L3投入

- **対象:** https://github.com/kerlenton/mcpsnoop
- **判断:** L3投入(mcpsnoop-l3)
- **根拠:** 自環境で繰り返し発生してきた「MCPが実際に何を返しているか見えない」問題に直接効く。具体的にはlist_knowledgeの表示バグ(MCP表示上はタグが空に見えるが実際はcontent内に存在し、現状は毎回 SELECT content FROM lightrag_doc_full でpsql直接確認する運用)と、do_searchのdownstream cap誤診(「10件制限」だと誤診していたが真因はentities/relationships/chunks=5/5/3の内部キャップだった)の両方が、実トラフィックの不可視性に起因している。mcpsnoopを挟めばレスポンスJSONを直接見て、タグがサーバー側の生成で失われているのかクライアント側の表示で失われているのかを切り分けられ、psqlでの間接確認を実観測に置き換えられる。加えてstreamable-HTTPのリバースプロキシモードがLightRAG MCP(port 9622)にそのまま適用でき、Replay機能が自作Skill Resolver MCPの反復開発ループを短縮する。ツールレベルのresult.isErrorまで捕捉するためJSON-RPCレベルでは成功に見える失敗を見逃さない。ECCが行った既定MCPコネクタ6→1削減のような監査を、推測ではなく実測で行える点も実益。単一バイナリ・ランタイム依存なしで顧客環境への持ち込みも容易。★6と極めて小規模だが、評価軸は人気度ではなく自環境の既知問題への適合性である。
- **注記:** MCP版Wireshark。AIクライアントとMCPサーバーの間に透過プロキシとして座り、実際にやり取りされる全JSON-RPCフレームをターミナルUIでライブ表示する。Go 99.3%、MIT、★6/fork 0/15 commits/v0.1.1。問題設定: 公式MCP Inspectorはそれ自身が別クライアントとして接続するため、実クライアント(Claude Desktop/Cursor/Claude Code)とサーバー間のトラフィックを見ない。実クライアントが呼ばなかった呼び出しや予期しない引数での呼び出しを見せられず、ツールが黙って呼ばれない・capabilityが噛み合わない・呼び出しがハングする時に/tmpのログをtailして推測する羽目になる。mcpsnoopは実データ経路に座るためサーバーの実装言語を問わず実トラフィックを覗ける。機能: ライブJSON-RPCストリーム(リクエスト/レスポンス/通知/stderr色分け、遅い呼び出しにフラグ、JSON-RPCエラーだけでなくツールレベルのresult.isErrorも捕捉)、Replay(捕捉したツール呼び出しを新鮮で隔離されたサーバーコピーに再実行)、Capability inspector(ハンドシェイクの合意内容確認)、Frame inspector(整形JSON+フレーム内検索)、ハング検出(進行中リクエストをPENDING+ライブタイマー表示)、フィルタクエリ(tool:/method:/id:/kind:/dir:/status:をAND結合、例 tool:search status:slow、dir:s2c kind:req でサーバー起点リクエスト)。アーキテクチャは1バイナリ2役割で、mcpsnoop -- <server> が透過shim(バイトをそのまま転送しつつ各フレームのコピーを送る)、引数なしのmcpsnoopがhub兼TUI。よく知られたソケットとディスク上ログでペアリングするため起動順序不問、UIがディスクから過去セッションをバックフィルする。streamable-HTTPは mcpsnoop http --target http://localhost:3000/mcp --listen :7000 のリバースプロキシモードで対応(自環境のLightRAG MCP port 9622 stateless HTTPにそのまま適用可能)。mcpsnoop demo で設定なしの試用可能。【制約】pre-1.0でSemVerに従うが0.xの間はマイナーリリースでユーザー向け挙動が変わりうるとREADMEが明記。ラップしたサーバーコマンドを実行するため信頼するサーバーのみラップし信頼できないものはコンテナで動かすこと。Homebrew coreには未収載(notability bar未達)でtap経由では brew trust が必要になることがある。デバッグ時のみ挟む使い方が基本で常時プロキシを噛ませる設計ではない。作者1名でメンテナンス継続性は未知数。
- **関連:** LightRAG MCP(自環境、デバッグ対象そのもの) / intent-driven-skill-resolution-l2c(Skill Resolver開発時に効く) / ecc-l3(MCPコネクタ6→1削減監査を実測できる) / claude-code-templates-l3(--analyticsによるセッション監視、観測レイヤーの類例) / waggle-l3(どのサブエージェントが実際に読んだかのテレメトリ、同じ問題意識) / smithery-smithery-ai-l3
- **再検討条件:**
  1. list_knowledge の表示バグを本格的に切り分ける時点で、mcpsnoop を挟んで実際のレスポンスJSONを確認する
  2. Skill Resolver MCP の開発に着手する時点で、Replay と Capability inspector を開発ループに組み込む
  3. 自環境のMCPコネクタ棚卸し(ECC同様の6→1削減監査)を行う時点で、実際に呼ばれているツールを実測する
  4. 顧客環境でMCPのトラブルシュートが必要になった時点(単一バイナリで持ち込みが容易)
  5. MCPサーバーがハングする・黙って呼ばれない問題が発生した時点(PENDING表示とハング検出)
  6. v1.0 に到達した時点で挙動の安定性を再評価する
  7. LightRAG MCP に新しいツールを追加する時点で、実クライアントがどう呼ぶかを観測する

---

## 2026-07-24: opencodex — 保留

- **対象:** https://github.com/lidge-jun/opencodex
- **判断:** 保留(opencodex)
- **根拠:** 完成度は高い(214 commits、v2.0.0、40+プロバイダ、5アダプタ、OAuth、GUI、3OS対応のサービス化、多言語README)が、現時点で自環境との接続点が薄いため保留とする。理由3点: (1)本ツールはCodexを使う前提であり、主軸はClaude Code + Claude.aiで、Codexは在庫の他リポジトリ(ECC、council-of-high-intelligence、claude-video等)でクロスハーネス対応として言及される程度にとどまる。(2)複数プロバイダを使い分けるという目的は、既存のOpenRouter運用で既に達成できている。本ツールを入れても解決する問題が現状存在しない。(3)接続点が「将来Codexを主要ハーネスとして使うなら」という条件付きであり、その予定が現時点でない。設計面で参照価値があるのは ocx stop の "Clean exit, zero residue"(プロキシ停止+サービス停止+Codex設定の原状復帰、残骸ゼロ)だが、この安全設計パターンは既に ECC の install-state による逆操作、claude-code-templates の --dry-run、council の --dry-route として在庫に複数存在しており、それだけで新規投入する理由としては弱い。既存ナレッジの磨き込み優先方針に照らし、パターンの存在のみ記録してCodex採用時に再訪する。
- **注記:** OpenAI Codex に任意のLLMを使わせるユニバーサル・プロバイダプロキシ。TypeScript 91%、MIT、★20/fork 3/214 commits/v2.0.0(2026-06-20)/11リリース。Bun 1.1+ 必須。Codex の Responses API を各プロバイダのプロトコルに翻訳するローカルプロキシで、ストリーミング・ツール呼び出し・推論トークン・画像が双方向で動作する。5つのプロトコルアダプタ(anthropic Messages / google Gemini / azure-openai / openai-responses パススルー / openai-chat=全OpenAI互換Chat Completions)で40+プロバイダをカバー。Anthropic・xAI・Kimi はOAuthログイン対応でトークン自動更新。モデルルーティングは provider/model 構文(codex -m "anthropic/claude-opus-4-8")、prefix省略時はデフォルトプロバイダまたはモデル名パターンで自動マッチ(claude-* → Anthropic)。Codex CLI/TUI/App/SDK に自動注入され、ルーティング済みモデルがCodexのモデルピッカーにネイティブ同様に表示される。subagentピッカーに最大5モデルをフィーチャー可能(複雑なタスクは推論モデル、高速タスクは安価なモデルへ委譲)。非OpenAIモデルにも gpt-5.4-mini サイドカー経由でWeb検索と画像理解を付与できる。Webダッシュボード(ocx gui、localhost:10100)でプロバイダ・OAuth状態・モデル選択・ライブリクエストログを表示。launchd/systemd/Task Scheduler でバックグラウンドサービス化。設計面で注目すべきは ocx stop の "Clean exit, zero residue" — プロキシ停止・バックグラウンドサービス停止・Codex設定の原状復帰を一括で行い、素の codex が以前と全く同じに動く。設定ファイルの残骸も孤児プロセスも残さない。これは今セッションで観察した dry-run / uninstall 系の安全設計(ECC の install-state による逆操作、claude-code-templates の --dry-run、council の --dry-route)と同系の思想。README は英語/韓国語/簡体中国語の3言語。
- **関連:** ecc-l3(クロスハーネス、install-stateによる逆操作) / claude-code-templates-l3(--dry-run) / council-of-high-intelligence-l3(マルチプロバイダ自動ルーティング、--dry-route) / claude-video-l3(マルチサーフェス配布) / OpenRouter運用(自環境、同目的の既存手段)
- **再検討条件:**
  1. Codex を主要ハーネスとして採用する判断をした時点で、プロバイダプロキシとしてL3投入を再評価する
  2. 顧客案件で「Codexに自社契約のLLM(Anthropic/Gemini/ローカルOllama)を使わせたい」という要件が出た時点
  3. OpenRouter運用の限界(プロバイダ固有機能が使えない、OAuth認証を使いたい等)に突き当たった時点で、5アダプタ方式との比較を行う
  4. 自作ツールに「クリーンなアンインストール・原状復帰」を実装する時点で、ocx stop の zero residue 設計を参照する
  5. ローカルLLM(Ollama/vLLM/LM Studio)をコーディングエージェントから使う構成を組む時点で、openai-chat アダプタの設定例を参照する
  6. サブエージェントへのモデル振り分け(複雑なタスクは推論モデル、高速タスクは安価なモデル)を設計する時点で、subagentピッカーの実装を参照する

---

## 2026-07-25: moshi-kyutai — 保留

- **対象:** https://github.com/kyutai-labs/moshi
- **判断:** 保留(moshi-kyutai)
- **根拠:** 技術的には極めて質が高いが、4つの理由で現時点では投入せず記録のみとする。(1)自環境で動かせない。PyTorch版は量子化未対応でGPU 24GB必須とREADMEが明記しており、KVM2(2vCPU/8GB/GPU無し)では議論の余地なく不可。MLX版はMac上で動くが顧客提供の形にならない。(2)音声領域は既存在庫でカバー済み。特に livekit-agents-l3(リアルタイム音声AIエージェント、WebRTC + 電話統合、Apache 2.0)が実用面での第一候補であり、STT→LLM→TTSを外部APIで組み立てる方式のため自前GPUを必要としない。Moshiはend-to-endのspeech-to-speech基盤モデルで層が異なるが、顧客案件で音声対話要件が出た場合の現実的な選択肢はLiveKit側になる。他に meetily-l3(ローカル議事録)、vapi-hermes-mcp-report.md も在庫にある。(3)リリースが2024年9月(rustymimi-0.2.2)で止まっており、731コミットに対してリリースタグは2つのみ。README自身がKyutaiのTTS/STT実用系として delayed-streams-modeling リポジトリを案内しており、Moshi本体は論文成果としての位置づけに移っていると読める。(4)日本語対応の記載がなく、日本企業向け案件への適合が不明。ただしMimi単体の設計思想(音声を12.5Hzトークンに落とし、テキストトークンの3-4Hzに近づけることで自己回帰ステップを削減する)は、今セッションで追跡してきたトークン予算・index先行のテーマと発想が通じるため、その観点での参照価値は記録しておく。
- **注記:** Kyutai Labs の speech-text 基盤モデル + full-duplex 音声対話フレームワーク。★10.2k / fork 952 / 731 commits。コードは MIT(Python) / Apache-2.0(Rust)、重みは CC-BY 4.0。論文 arXiv:2410.00037。

【アーキテクチャ】2つの音声ストリーム(Moshi自身の発話とユーザーの発話)を同時にモデル化する full-duplex 設計。加えて自分の発話に対応するテキストトークン(inner monologue)を予測することで生成品質を大きく向上させている。小さな Depth Transformer が同一タイムステップ内のコードブック間依存を、7Bパラメータの Temporal Transformer が時間方向の依存をモデル化する。理論レイテンシ160ms(Mimiのフレームサイズ80ms + 音響遅延80ms)、L4 GPU での実用レイテンシは約200ms。

【Mimi(音声コーデック)】24kHz音声を12.5Hz表現・1.1kbps帯域に、完全ストリーミング(レイテンシ80ms = フレームサイズ)で落とす。非ストリーミングの SpeechTokenizer(50Hz, 4kbps)や SemantiCodec(50Hz, 1.3kbps)を上回る。SoundStream / EnCodec の系譜にエンコーダ・デコーダ両方へ Transformer を追加し、ストライドを調整して 12.5Hz を実現。**テキストトークンの平均フレームレート(約3-4Hz)に近づけることで Moshi の自己回帰ステップ数を削減する**という設計思想が中核。SpeechTokenizer 同様に蒸留損失で第1コードブックを WavLM の自己教師表現に一致させ、意味情報と音響情報を単一モデルで扱う。EBEN 同様に敵対的損失のみ(+特徴マッチング)で学習し、低ビットレートながら主観品質を大きく改善。`rustymimi` として Python バインディングあり。

【3実装】PyTorch(研究・実験用、moshi/)、MLX(iPhone/Mac のオンデバイス推論、moshi_mlx/)、Rust(本番用、rust/。Mimi の Rust 実装を含む)。Web UI クライアントは client/。ファインチューンは kyutai-labs/moshi-finetune。

【モデル】Moshiko(男性合成音声)、Moshika(女性合成音声)、Mimi。PyTorch(bf16/int8)、MLX(int4/int8/bf16)、Rust-Candle(int8/bf16)で配布。

【同一コードベースで動く関連モデル】Hibiki(同時音声翻訳、kyutai-labs/hibiki)、Kyutai TTS/STT(kyutai-labs/delayed-streams-modeling)。READMEが後継として明示的に案内している。
- **関連:** livekit-agents-l3(音声エージェントの実用第一候補、STT→LLM→TTS組み立て型) / meetily-l3(ローカル議事録、Whisper系) / vapi-hermes-mcp-report.md(音声AI + Hermes) / kyutai-labs/delayed-streams-modeling(後継のTTS/STT、未評価) / kyutai-labs/hibiki(同時音声翻訳、未評価) / kyutai-labs/moshi-finetune(ファインチューン、未評価)
- **再検討条件:**
  1. Kyutai の後継リポジトリ delayed-streams-modeling(TTS/STT)を評価する時点で、本記録を前提知識として参照する。実用性はこちらの方が高い可能性がある
  2. 顧客案件でリアルタイム音声対話の要件が出た時点で、まず livekit-agents-l3 を第一候補として評価し、end-to-endモデルが必要な場合にのみMoshiを再検討する
  3. GPU付きホスティング(24GB以上)を確保する判断をした時点で、Rust実装(rust/、本番用)のセルフホストを評価する
  4. 音声をトークン化してLLMに食わせる要件が出た時点で、Mimi(rustymimi、Python バインディング)を音声表現の圧縮手段として単独評価する
  5. 同時音声翻訳の要件が出た時点で kyutai-labs/hibiki を評価する
  6. Moshiが日本語対応した、または日本語版が公開された時点
  7. Mac上でのローカル音声対話デモが営業材料として必要になった時点でMLX版(int4量子化)を評価する

---

## 2026-07-25: i-have-adhd-l3 — L3投入

- **対象:** https://github.com/ayghri/i-have-adhd
- **判断:** L3投入(i-have-adhd-l3)
- **根拠:** ★7.3k/fork 308と出力スタイル制御スキルの代表例だが、投入理由は内容(10ルール)ではなく作り方にある。最大の価値は evals/ + tests/ + CI という構成で、出力スタイルという主観的なものを機械的に検証する外部実装として、プロジェクトスキル skill-verifier の設計参照に直接効く。既存の stop-slop-l3 が採点ルーブリック(5次元、35/50未満で改稿)を持つものの手動運用であるのに対し、本エントリはCIまで自動化しており、両者を並べると「採点基準の設計」と「その自動化」の2段が見える。加えて5マニフェストの多サーフェス配布(Claude Code/Codex/Cursor/Gemini/汎用)は、これまで収集した配布構造(claude-video-l3の3マニフェスト、claude-code-templates-l3)の系列で最も広い実例であり、touch ~/.claude/.i-have-adhd-always によるファイル有無での状態表現、フォーク時の名前空間衝突とその回避手順も実務的な参照になる。10ルール自体も、非エンジニア顧客向けエージェントの出力設計指針(特にルール1・2・3・9・10)として流用でき、ナレッジMCP商品の応答設計に接続する。stop-slop-l3とは対象が異なり(散文 vs エージェント応答、英語前提 vs 構造ルール中心で言語をまたぐ)補完関係にあるため、在庫の重複にはならない。
- **注記:** コーディングエージェントが答えを埋もれさせるのを止める出力スタイル制御スキル。MIT、★7.3k/fork 308/84 commits/リリースなし。Python 95.7%だがスキル本体はSKILL.mdで、Pythonはevals/tests/hooks/scriptsが占める。出典は『The Adult ADHD Tool Kit』(Ramsay/Rostain)を緩やかに下敷きにし、人間の1日の整理法ではなくLLMの応答のあり方として翻案したもの。診断不要とREADMEが明記しており医療的文脈のものではない。

【10ルール】(1)次に取る行動から始める (2)複数手順には番号を振る (3)1つの具体的な次の一歩で終える (4)脱線を抑制 (5)毎ターン現在の状態を再掲 (6)時間見積もりは具体的に(「少し」ではなく分単位) (7)成果を可視化 (8)エラーは淡々と (9)リストは5項目まで (10)前置きなし・要約なし・締めの挨拶なし。Before/After対比の要点は「情報量は変わらず順序と密度だけが変わる」こと。

【参照価値1: evals + tests + CI】出力スタイルという主観的なものに対し evals/ tests/ .github/workflows/ を持ち、機械的に検証している。Python 95.7%という言語構成は評価・テスト基盤が中心を占めることを意味し、84コミットの大半はここに費やされていると読める。stop-slop-l3も採点ルーブリック(5次元、35/50未満で改稿)を持つがCIでは回していない。本エントリはそこまで踏み込んでおり、skill-verifier(テストケース実行→スコアリング→改善→再評価)の設計参照として直接効く。

【参照価値2: 5マニフェストの多サーフェス配布】.claude-plugin/ + plugin.json(Claude Code)、.codex-plugin/(Codex、暗黙発動もあり)、.cursor/skills/(Cursor)、gemini-extension.json + GEMINI.md(Gemini)、.agents/plugins/(汎用)。claude-video-l3の3マニフェストより広い。ローカルcloneは不要でClaude Codeがリポジトリを取得し更新も維持する。常時適用は touch ~/.claude/.i-have-adhd-always で、設定ファイルを持たずファイルの有無だけで状態を表す軽量設計。

【参照価値3: フォーク時の名前空間衝突】READMEがフォークして自分用に書き換える手順を明示し、「フォークと上流が同名を共有するため先に上流を外す必要がある」という衝突を手順として記載している(uninstall → marketplace remove → 自分のフォークをadd → install)。スキル配布の実務的な落とし穴の実例。

【制約】内容そのもの(10ルール)に目新しさはなく「結論を先に」「番号を振る」「前置きを省く」は文書作法として既知。価値はevals付きで配布されているという作り方の側にある。リリースなし(タグなし)で追跡しづらい。自環境には既に「説明よりコマンドを優先して出す」作業ルールがあり二重管理になる可能性がある。ルール5(毎ターン状態を再掲)とルール10(要約なし)は緊張関係にあり、実運用での両立方法はSKILL.md本文の確認が必要。ルール9(リスト5項目まで)は網羅性が必要な場面(技術評価、選択肢提示)と衝突する。SKILL.md本文とevalsの中身は未読で実装詳細は要確認。
- **関連:** stop-slop-l3(散文のAI臭除去、補完関係) / skill-verifier(プロジェクトスキル、evals-tests-CIの設計参照先) / skill-design-patterns-l2 / skill-optimization-methods-l3 / claude-video-l3(3マニフェスト配布、本エントリは5で上位) / claude-code-templates-l3 / intent-driven-skill-resolution-l2c / L0-007 Progressive Disclosure(ルール9が認知負荷の観点で接続)
- **再検討条件:**
  1. skill-verifier を改良する時点で evals/ と tests/ の構成・CIワークフローを実際に読んで設計参照する(本エントリで最も価値が高い行動)
  2. 自作スキルを多サーフェス配布する判断をした時点で、5マニフェスト構成と INSTALL.md を参照する
  3. 顧客向けエージェントの応答設計を行う時点で、10ルールを設計指針として流用する
  4. 自環境の作業ルール(「説明よりコマンドを優先して出す」)を見直す時点で、10ルールとの重複・補完を整理する
  5. SKILL.md本文を読む必要が出た時点で、ルール5(状態再掲)とルール10(要約なし)の両立方法を確認する
  6. スキルのフォーク運用を始める時点で、名前空間衝突の回避手順を参照する
  7. note.com等の文章生成でstop-slopと併用する判断をした時点で、両者の適用範囲を切り分ける

---

## 2026-07-26: three-role-agent-development-loop-l2c — L2c投入

- **対象:** N/A(リポジトリ由来ではない。loop-architectスキル + L0原理群からの設計抽出)
- **判断:** L2c投入(three-role-agent-development-loop-l2c)
- **根拠:** 「エージェントAで設計、Bでコーディング、戻ってきたコードをAが検証して次タスクへ」という開発効率化の構想を、loop-architectスキルの前提原則に照らして検討した結果として抽出したパターン。素朴な2者構成が原理的に壊れる理由(特にR2 fresh context違反により設計誤りが構造的に検出不能になる点)と、その修正としての3者分離は、今後エージェント間ループを組むあらゆる場面で再利用される設計知であり、特定のLoop Spec実装に埋もれさせるべきではない。加えて「検証基盤がない領域で無人ループを回さない」という前提条件は、着手順序を誤ると成果がマイナスになる判断であり、パターンとして明示的に記録する価値が高い。既存のL0原理(L0-009 自律実行の責任境界、L0-002 判断委譲の構造化、L0-008 完成度の段階)を実装レベルの設計判断へ落とす具体例にもなっており、L0とL2の接続点として機能する。今セッションで投入したcouncil-of-high-intelligence(集団思考を機構で防ぐ)、waggle(ハンドオフ継ぎ目の失敗)、i-have-adhd(evals+CIによる主観的品質の機械検証)、mcpsnoop(トラフィック観測という外部証拠)とも接続する。実装・実測が未実施のためstatus:unverifiedのL2cとして投入し、実際に回した時点でL2昇格を判定する。
- **注記:** status:unverified(設計のみ。実装・実測は未実施)。リポジトリ由来ではなく、loop-architectスキルとL0原理群からの設計抽出。

【2者構成の欠陥】「A(設計)→B(実装)→A(検証)」をmaker/checker 6原則(R1-R6)に照らすと、R1は形式的に満たすがR2-R5を破る。最も危険なのはR2(fresh context)違反で、Aは自分の設計に忠実な実装ほど「正しい」と判定するため、設計自体が誤っていた場合に忠実な実装ほど通過してしまい、誤りが検出されないまま次タスクへ積み上がる。学術的根拠はHuang et al. ICLR 2024(LLMは外部信号なしに自己の推論を修正できず、むしろ劣化する)。加えてwaggleが指摘するマルチエージェント失敗のハンドオフ継ぎ目問題があり、2者構成はその継ぎ目に検証を置いていない。

【3者分離】A(設計・委譲・統合、全体文脈あり、書込み権限あり)/ B(実装、当該タスク+制約のみ、成果物のみ書込み)/ C(独立検証、成果物と受入条件のみで設計経緯を見ない、書込み権限なし、外部証拠に接地、Default-FAIL)。Cは合否を出すが何をすべきかは決めず、Aは進行を決めるが合否は出さない。Aを完全に外さない理由は、設計と進行管理が人間の代理として必要で、そこにAを置くことで人間の介入点が1箇所に集約されるため。

【最重要の前提条件】検証基盤がない領域で無人ループを回さない。「無人で回したい × 検証基盤がない」は最も危険な組み合わせで、朝には壊れた成果物が積み上がる。対象領域ごとに外部証拠の有無を確認し、揃っている領域から型を確立してから他領域へ広げる。自環境の場合、n8n領域は validate_workflow / test_workflow / pin data が既にあり心拍(Schedule)も同一基盤で持てるため即座に成立する一方、自作MCP・スキル領域は部品(mcpsnoop / skill-verifier / evals)はあるが未接続、一般アプリケーションコードは基盤整備が先。

【その他の設計要素】停止条件は外部検証可能な形にし予算上限(反復回数/時間/コスト)と無変化サイクル検出を必ず設ける。自律実行の境界はL0-009の3軸AND判定(リスクレベル別が最優先→フェーズ別→影響範囲別)を適用し、取り消しが困難な操作(本番反映・公開・破壊的変更)は自律実行の対象外として人間承認に残す。作業対象は必ず複製上で行い原本に触れない(git worktree / ワークフロー複製)。記憶はコンテキストでなくディスク/DBに置き、構造化stateはData Table、意味記憶はナレッジベースへ割り当てる。kill-switch / steer / 人間レビュー点を定義する。3負債のうち理解負債の対策が最も抜けやすく、「変更差分 + Cの判定理由」のダイジェストを出して読まずに承認させない仕組みが必要。
- **関連:** loop-architect(プロジェクトスキル、本パターンの設計元) / L0-009 自律実行の責任境界 / L0-002 判断委譲の構造化 / L0-008 完成度の段階 / council-of-high-intelligence-l3(集団思考防止の強制機構) / waggle-l3(ハンドオフ継ぎ目の失敗、消費契約+coverage) / skill-verifier(in-sessionループの採点検証) / i-have-adhd-l3(evals+tests+CI) / mcpsnoop-l3(外部証拠としてのトラフィック観測) / miniclaw-sandbox-pattern-l2c(隔離の実装) / n8n-workflow-sync / n8n-workflow-builder(実体化経路)
- **再検討条件:**
  1. 検証基盤が揃った領域(まずn8n)で実際に3者ループを構築して回した時点でL2昇格を判定する
  2. CがNEEDS_WORKを正しく出した事例と、設計誤りを検出できた事例を確認した時点
  3. 予算上限・無変化サイクル検出が実際に発火することを確認した時点
  4. 1サイクルのコストと所要時間を実測し、2者構成および手動作業と比較した時点(3者構成は確実に高コストなため割に合うかの検証が必要)
  5. Cのfresh contextを別プロセス・別モデルで徹底する必要が出た時点(同一セッション内の役割分けでは文脈が漏れる可能性)
  6. Cの判定をPASS/NEEDS_WORKの二値からL0-008に従った段階評価へ変更を検討する時点
  7. 自作MCP・スキル領域へ展開する時点で、mcpsnoop + skill-verifier + evals を外部証拠として接続する設計を行う
  8. 理解負債ダイジェストを人間が実際に読んでいるか(形骸化していないか)を点検する時点

---

## 2026-07-26: pi-agent-harness-l3 — L3投入

- **対象:** https://github.com/earendil-works/pi
- **判断:** L3投入(pi-agent-harness-l3)
- **根拠:** ★77.5k/fork 9.5k/5,109 commits と今回評価した中で最大規模だが、投入理由はエージェント部品としてではなくセキュリティ・運営の参照実装としての価値にある。最大の理由はサプライチェーン強化の実装が具体的でそのまま転用できる点で、min-release-age=2(同日リリースの依存を避ける)、--ignore-scriptsの徹底、依存ライフサイクルスクリプトの明示的許可リスト、リポジトリ外に隔離した環境でのリリーススモークテストは、顧客案件でnpm依存を扱う際および自作MCP・スキルをnpm配布する際の防御策として即座に有用。第二に「パーミッションシステムを内蔵しない」という明示的な設計判断と外部化3パターンが、既存在庫のminiclaw-sandbox-pattern-l2c(4層防御を内蔵)と真逆の判断であり対比材料として価値が高い。特にGondolinパターン(認証はホストに残し実行をマイクロVMへ)は認証情報を隔離環境に持ち込まないという点で他2パターンより洗練されている。第三に★77.5k規模のOSS運営設計(新規コントリビュータのissue/PR自動クローズ、AGENTS.md、外部RFC、SHA256SUMS付き再現可能ビルド)が自作OSS公開時の参照になる。加えてpi-agent-coreがライブラリとして公開されているため、three-role-agent-development-loop-l2cをn8n以外で実体化する際のオーケストレーション基盤候補になる。
- **注記:** エージェントハーネスを4npmパッケージに切り出したツールキット。MIT、★77.5k/fork 9.5k/5,109 commits、TypeScriptモノレポ(Biome + vitest + Bun executable)。badlogicgames(Mario Zechner、libgdx作者)が関与。パッケージ: pi-ai(統一マルチプロバイダLLM API)、pi-agent-core(ツール呼び出しと状態管理を持つエージェントランタイム)、pi-coding-agent(対話型CLI)、pi-tui(差分レンダリングTUI)。別リポジトリ pi-chat でSlack/チャット自動化。自身を "self extensible coding agent" と表現。

【参照価値1: サプライチェーン強化 — 最重要】方針は「npm依存の変更をレビュー済みのコード変更として扱う」。実装: 直接の外部依存は厳密バージョンにピン(内部ワークスペースのみ範囲許容)、.npmrc に save-exact=true と **min-release-age=2**(同日リリースの依存を避ける)、package-lock.json が唯一の真実でpre-commitが誤コミットをブロック(PI_ALLOW_LOCKFILE_CHANGE=1 で明示解除)、npm run check がピン留め・ネイティブTSインポート互換性・生成shrinkwrapを検証、公開CLIに npm-shrinkwrap.json を同梱して推移的依存をピン、リリーススモークテストは npm run release:local でビルド・packし**リポジトリ外に隔離されたnpm/Bunインストールを作ってから**タグを打つ、ローカルリリースインストール/文書化されたnpmインストール/pi update --self は可能な限り --ignore-scripts、CIは npm ci --ignore-scripts でスケジュールワークフローが npm audit --omit=dev と npm audit signatures --omit=dev を実行、**shrinkwrap生成に依存ライフサイクルスクリプトの明示的許可リストがあり新規のものはレビューまでチェックを落とす**。

【参照価値2: パーミッションを内蔵しない設計判断】READMEが「ファイルシステム・プロセス・ネットワーク・認証情報のアクセス制限のための組み込みパーミッションシステムを持たず、既定では起動したユーザーとプロセスの権限で動く」と明示。代わりに外部化3パターンを提示(packages/coding-agent/docs/containerization.md): Gondolin extension(piとプロバイダ認証をホストに残し、組み込みツールと!コマンドをローカルLinuxマイクロVMにルーティング)、Plain Docker(プロセス全体をコンテナに)、OpenShell(ポリシー制御サンドボックス)。miniclaw-sandbox-pattern-l2c(4層防御を内蔵)と真逆の判断で、MiniClawが「安全な既定値」を取るのに対しPiは「明示的な選択」を取る。特にGondolinは認証情報を隔離環境に持ち込まない点で設計として洗練されている。

【参照価値3: 大規模OSS運営】新規コントリビュータのissue/PRを既定で自動クローズし、メンテナが毎日レビューする。opencut-l3の"Focus areas / Avoid for now"明示より過激。AGENTS.mdに人間とエージェント両方向けのプロジェクトルール、RFCを外部サイト(rfc.earendil.com)で運用、リリースにSHA256SUMSでカバーされたバージョン付きソースアーカイブを含め公式標準バイナリと同じビルドスクリプトで再現可能(--offline-model-dataでライブカタログを更新せずスナップショットでビルド、パッケージメンテナ向けに --skip-install --skip-deps)。

【参照価値4: OSSセッションのデータセット公開】badlogic/pi-share-hf でHugging Faceにセッションを公開。「おもちゃのベンチマークではなく実世界のタスク・ツール使用・失敗・修正」という方向性。作者自身も badlogicgames/pi-mono として継続公開。

【制約】部品としては使わない可能性が高い(コーディングエージェントはClaude Code、統一LLM APIはOpenRouter、TUIは不要)。価値は設計・運営・防御の参照に集中する。パーミッションを持たないため使う場合は必ずコンテナ化前提。新規コントリビュータのissue/PRは自動クローズされる。規模が大きく全体を読むのは非現実的で、目的の箇所(.npmrc、package.jsonのcheck、containerization.md)を狙って読むのが妥当。pi-agent-coreでループを組む場合マルチエージェント・オーケストレーションは自分で書くことになりTypeScriptを書く前提のため、現在の対話型開発スタイル(Claude.ai + ウェブターミナル)からは距離がある。
- **関連:** miniclaw-sandbox-pattern-l2c(サンドボックス内蔵、真逆の設計判断として対比) / three-role-agent-development-loop-l2c(pi-agent-coreが実体化候補) / opencut-l3(TSモノレポ Bun+Biome、OSS運営のFocus-Avoid明示) / council-of-high-intelligence-l3(マルチプロバイダ、プロファイルによる規模切替) / ecc-l3 / claude-code-templates-l3(エージェントハーネス・配布の類例) / i-have-adhd-l3(evals+CI、データセットの方向性) / waggle-l3(設計規律の厚さで同系)
- **再検討条件:**
  1. 顧客案件でnpm依存を扱う、または自作MCP・スキルをnpm配布する時点で .npmrc の設定と npm run check の検証項目を実装参照する(本エントリで最も価値が高い行動)
  2. エージェントのサンドボックス化を設計する時点で containerization.md の3パターン(特にGondolin)を miniclaw-sandbox-pattern-l2c と並べて比較する
  3. 自作OSSを公開する判断をした時点で、コントリビュート運営(自動クローズ)・AGENTS.md・SHA256SUMS付き再現可能ビルドを参照する
  4. three-role-agent-development-loop-l2c を n8n以外のランタイムで実体化する判断をした時点で pi-agent-core をオーケストレーション基盤の候補として評価する
  5. evals を設計する時点で「おもちゃのベンチマークではなく実世界の失敗と修正」というデータセットの方向性を参照する
  6. Slack/チャット経由のワークフロー自動化が必要になった時点で earendil-works/pi-chat を評価する
  7. npmサプライチェーン攻撃のインシデントが発生した時点で、本エントリの防御実装を自環境に適用する
