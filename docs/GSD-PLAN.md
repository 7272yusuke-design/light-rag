# LightRAGナレッジパイプライン プロジェクト計画

## プロジェクト概要
LightRAGを「外部脳」として構築し、GitHub OSS・Claude Code SKILL・技術ドキュメントから知識を構造化・蓄積する。複数プロジェクト（OpenClaw / Virtual Protocol / n8nコンサル / note.com発信）の開発を横断的に支援するナレッジパイプライン。

## 全体方針
- **3レイヤー + L2c構成**: L3（実装） / L2（検証済みパターン） / L2c（候補パターン） / L1（横断運用メタ知識のみ）
- **投入経路の明確化**: 本体ナレッジはClaude.aiから upload_document、管理ファイルはVPSで直接編集
- **判断ログの永続化**: 全ての投入評価を KNOWLEDGE-DECISIONS.md に記録（4カテゴリ: L3投入/L2c投入/保留/見送り）
- **クリーンアップ原則**: DELETE API禁止、psql直接操作 + pg_dump必須

---

## Phase 履歴サマリー

### Phase 1-11（2026-04-15）✅
**目的**: 初期構築 → 3レイヤー体系の確立
- インフラ構築（Docker / PostgreSQL / Ollama / MCP / Cloudflare Tunnel）
- 初期ナレッジ69件投入
- L0-L1から3レイヤー（L1/L2/L3）へリファクタリング
- combination-architect / knowledge-navigator スキル作成
- VPS正運用へ移行（管理ファイルをVPS側に集約）

### Phase 1-11補完（2026-04-17）✅
- openclaude-l3 新規投入
- L2抽出候補3パターン記録（Agent Routing / Tool-loop+MCP / OpenAI互換抽象化）

### Phase L1 v3再設計 + L2c拡充（2026-04-18）✅
**目的**: L1の意味再定義 + 候補パターンレイヤー新設
- DATA-SCHEMA.md v2/v3更新
  - L1再定義: 「横断運用のメタ知識」と「環境前提」のみ
  - サブタイプ追加: L1-Infra / L1-Ops
  - L2c（候補パターン）レイヤー新設
  - L2品質ゲート強化（pattern/combinationのみ、L1→L2直接昇格禁止）
  - 4判断カテゴリ明文化（L3投入/L2c投入/保留/見送り）
- KNOWLEDGE-DECISIONS.md 新設（初期7件の判断記録）
- L2c本体投入 5パターン
- mcp2cli L3投入 + Schema-driven Lazy CLI L2c投入
- L1から汎用パターン3件をL2cへ昇格（TrinityCouncil / n8n自己改善 / CLAUDE.md駆動）
- L1削除10件（プロジェクト固有情報を全除外）
- L1維持3件をL1-Infra/L1-Opsにリネーム

### Phase 3 無サフィックス再投入（2026-04-19）✅
**目的**: 旧形式ファイルを正規L3形式へ移行 + エンティティ純度向上
- 用途別検索精度の実地検証（6テストクエリ）
- エンティティ構造の解明（lightrag_full_entities と vdb_entity の役割分担）
- Phase 1a: 重複24件削除（skill系旧版18+プロジェクト進捗2+孤児4）
- バッチ1: マルチエージェント3件再投入（langgraph/mastra/n8n）
- バッチ2: Web系3件再投入+llmfit削除（firecrawl/browser-use/ffmpeg）
- バッチ3: SaaS/取引6件再投入+nemo-agent-toolkit削除（anthropic-cookbook/ccxt/freqtrade/n8n-as-code/supabase/vercel）
- 検証テストで品質改善を確認（CCXT+Freqtrade+TrinityCouncilが揃う等）
- 結果: 計39件削除・13件再投入・26件純減、vdb_entities 約800件のノイズ除去

### Phase 12: 整理・再棚卸し（2026-05-01）✅
**目的**: ナレッジベース実態と管理ファイル記録の同期
- ナレッジ実数を確認: **157件**（メモリ/INDEX記録の104〜123件から大幅増加が判明）
- 新規L3投入2件（trellis-mindfold-l3 / voxcpm-openbmb-l3）
- 見送り判断1件（docker-android budtmo）
- doc_fullゴースト21件削除
  - lightrag_vdb_chunks_nomic_embed_text_768d: 71件
  - lightrag_doc_chunks: 71件
  - lightrag_doc_full: 21件
  - 結果: doc_full = doc_status = 157（整合性達成）
- 全157件のレイヤー別棚卸し実施
- 旧形式13件のリネーム計画明文化
- INDEX.md / RESUME.md / DECISIONS.md / GSD-PLAN.md を157件状態に同期更新

---

## 現在の状態（2026-05-01）

### ナレッジベース統計
- **総数: 157件**（全processed、エラー0件）
- **整合性: doc_full = doc_status = 157**（ゴースト除去済み）

### レイヤー内訳
| レイヤー | 件数 | 目標 | 達成率 |
|---------|------|------|--------|
| L3（実装） | 103 | 50-60% | 超過（65.6%） |
| L2（検証済みパターン） | 18 | 20-25% | 50%（11.5%） |
| L2c（候補パターン） | 19 | - | 順調 |
| L1-Infra | 1 | 最小限 | ✅ |
| L1-Ops | 2 | 最小限 | ✅ |
| L1-old | 1 | 0 | リネーム必要 |
| other（旧形式） | 13 | 0 | リネーム必要 |

### バックアップ状態
- 最新: `/docker/lightrag/backups/pre-reinventory-20260501-011545.sql` (251MB)

---

## 残タスク（優先順、2026-05-01更新）

### 最優先（セキュリティ）
1. [ ] **OpenRouter APIキーローテーション**（チャットで公開済み）

### Phase 13候補: リネーム再投入
2. [ ] 旧形式13件のリネーム再投入（other枠、INDEX.md記載の計画通り）
   - L3にリネーム: 11件（agency-agents / ai / awesome-design-md / codex-plugin-cc / gh-cli / gws-cli / lightrag / motion / obsidian-skills / stripe-cli / ui）
   - L2にリネーム: 2件（awesome-compose / building-llm）
3. [ ] L1-old 1件のリネーム（awesome-agent-skills-l1 → l3化検討）

### Phase 14候補: 検索品質向上
4. [ ] entity_chunks/relation_chunks のゴースト要素クリーンアップ（LightRAG公式手順調査が必要）
5. [ ] 2段階クエリ戦略のスキル化（理論はDATA-SCHEMA.md記載済、スキル化のみ未着手、article-architect類似）

### Phase 15候補: パターン拡充
6. [ ] L2c → L2 昇格候補の検証（実装による検証実施）
7. [ ] L2拡充（現18件 → 目標25件）

---

## 活用目的（2026-04-18 明文化）
1. **開発設計**: Claude.aiからMCP経由で参照、具体的な設計書を出力
2. **開発支援**: Hostingerターミナル開発時にナレッジ参照
3. **情報発信**: 主にL2ユースケースの記事を自動生成して発信

## 主要プロジェクト（ナレッジ活用先）
- OpenClaw: 仮想通貨自動取引エージェント（TrinityCouncil 3エージェント議論型）
- Virtual Protocol関連開発（VirtuStore: ACP Marketplace SaaS構想）
- n8nコンサル業務（クライアント案件・上流提案材料）
- note.com（きよびん）コンテンツ発信
- その他単発開発案件（Website / Webアプリ / AIエージェント / n8nワークフロー）

---

## 関連ドキュメント参照
- [RESUME.md](RESUME.md): セッション開始時の確認事項
- [KNOWLEDGE-INDEX.md](KNOWLEDGE-INDEX.md): 全157件のレイヤー別一覧
- [KNOWLEDGE-DECISIONS.md](KNOWLEDGE-DECISIONS.md): 投入判断履歴
- [DATA-SCHEMA.md](DATA-SCHEMA.md): データ構造ルール・L2cテンプレート・4判断カテゴリ
- [ARCHITECTURE.md](ARCHITECTURE.md): システム設計詳細
- [SYSTEM-SPEC.md](SYSTEM-SPEC.md): システム仕様
