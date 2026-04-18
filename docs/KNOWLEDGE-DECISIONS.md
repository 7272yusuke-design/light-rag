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

