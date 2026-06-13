# 再開手順書

## このドキュメントについて
LightRAGナレッジパイプラインの作業を再開する際の手順。セッション開始時にこのファイルを確認する。

## 即座に伝えること

LightRAGナレッジパイプラインの続きをやります。

- VPS: 76.13.187.66
- 作業ディレクトリ: /docker/lightrag/
- Git: https://github.com/7272yusuke-design/light-rag

計画書（全てVPS上 /docker/lightrag/docs/）:
- RESUME.md（本ファイル）
- GSD-PLAN.md（全体計画とフェーズ）
- ARCHITECTURE.md（システム設計）
- DATA-SCHEMA.md（データ構造ルール・L1 v3再定義/L2c/4判断カテゴリ含む）
- KNOWLEDGE-INDEX.md（ナレッジ一覧・移行ログ）
- KNOWLEDGE-DECISIONS.md（投入判断ログ）
- SYSTEM-SPEC.md（システム仕様）

## 現在のフェーズ
**Phase 12 完了（2026-05-01）**: 整理・再棚卸しセッション

## ナレッジベース現状（2026-05-01）
- **総数: 157件**（全processed、エラー0件）
- **doc_full = doc_status = 157**（整合性確保、ゴースト21件除去済み）

### レイヤー内訳
| レイヤー | 件数 | 割合 |
|---------|------|------|
| L3（実装） | 103 | 65.6% |
| L2（検証済みパターン） | 18 | 11.5% |
| L2c（候補パターン） | 19 | 12.1% |
| L1-Infra | 1 | 0.6% |
| L1-Ops | 2 | 1.3% |
| L1-old | 1 | 0.6% |
| other（旧形式） | 13 | 8.3% |

## 環境確認コマンド
    cd /docker/lightrag && docker compose ps
    systemctl status ollama --no-pager
    curl -s http://localhost:9621/health || echo "LightRAG is down"
    docker exec lightrag-postgres pg_isready -U lightrag
    systemctl status mcp-lightrag --no-pager
    systemctl status cloudflared-mcp --no-pager

## 環境復旧（止まっていた場合）
    sudo systemctl start ollama
    cd /docker/lightrag && docker compose up -d
    sudo systemctl start mcp-lightrag
    sudo systemctl start cloudflared-mcp

## 現在のインフラ構成
    VPS (76.13.187.66)
    +-- Ollama (systemd, port 11434)
    |   +-- nomic-embed-text (embedding, 768dim)
    +-- Docker
    |   +-- lightrag-postgres (pgvector:pg16, port 5433, user: lightrag, db: lightrag)
    |   +-- lightrag-server (port 9621, network_mode: host)
    |       +-- LLM: OpenRouter -> anthropic/claude-sonnet-4.6
    |       +-- Embedding: Ollama -> nomic-embed-text
    |       +-- Storage: PostgreSQL + NetworkX
    +-- MCP (port 9622, systemd)
    |   +-- mcp-lightrag.service
    |   +-- cloudflared-mcp.service
    |       +-- https://mcp.7272yusuke.cloud/mcp
    +-- Repomix (npm global)
    +-- graphify (pip global)

## 認証情報
- WebUI: http://76.13.187.66:9621 -> admin / LightRag@2026!
- .envはgit外。VPS上の /docker/lightrag/.env を参照
- **OpenRouter APIキーは要ローテーション**（チャットで公開済み・最優先タスク）

## ナレッジ4レイヤー構成（2026-04-18 v3 / 2026-05-01時点件数）

### L3（実装）: 103件
気になる技術スタックの部品在庫。リポジトリ/ツール/SKILLは最初からL3で投入。
詳細はKNOWLEDGE-INDEX.md参照。

### L2（検証済みパターン）: 18件
組み合わせ方を知る。検証済みのみ。category: pattern/combination のみ許可。
詳細はKNOWLEDGE-INDEX.md参照。

### L2c（候補パターン）: 19件
ブレスト/OSS読解ベースで投入可（status: unverified）。
ファイル名: *-l2c_lightrag.txt。検証後にL2へ昇格。

### L1（横断運用メタ知識のみ）: L1-Infra 1件 + L1-Ops 2件 = 計3件
v3再設計によりプロジェクト固有情報は全除外。
- dev-environment-workflow-v2-l1-infra（L1-Infra）
- lightrag-infra-ops-l1-ops（L1-Ops）
- lightrag-knowledge-ops-l1-ops（L1-Ops）

### その他（旧形式・リネーム対象）: 14件
- L1-old: 1件（awesome-agent-skills-l1）
- other（サフィックスなし）: 13件
詳細・リネーム計画はKNOWLEDGE-INDEX.md参照。

## ナレッジ投入ルール（2026-04-18 v3）

### 基本ルール
- 汎用スキル・パターンのみ投入。顧客固有情報はClaude Code側で完結
- ナレッジ本体の投入経路はClaude.ai（LightRAGプロジェクト）からのupload_document
- 管理ドキュメント（INDEX/DECISIONS/RESUME/SCHEMA）はVPS上で直接編集
- リポジトリ/ツールは最初からL3品質で投入（段階的アップグレード禁止）
- 削除はDELETE API禁止。psql直接操作 + pg_dump必須
- 案件完了後、汎用化できるパターンをL2として投入

### L1 v3ルール
- L1はL2/L3を使うための「横断運用のメタ知識」と「環境前提」のみ
- プロジェクト固有情報はLightRAGに入れない（Claude.aiプロジェクト/Notion側で管理）
- サブタイプ: L1-Infra（開発環境前提）、L1-Ops（LightRAG運用メタ知識）
- ファイル名: *-l1-infra_lightrag.txt / *-l1-ops_lightrag.txt

### L2c（候補パターン）ルール
- ブレスト/OSS読解ベースでも投入可（status: unverified）
- ファイル名: *-l2c_lightrag.txt
- 自環境で実装・動作確認後、L2に昇格（ファイル名リネーム）

### L2品質ゲート
- L2のカテゴリは pattern / combination のみ（context/persona/research禁止）
- L1→L2直接昇格禁止。必ず L1→L2c→検証→L2 の段階を経ること

### 判断ログ（必須）
- 新規リソース評価時は必ずKNOWLEDGE-DECISIONS.mdに記録
- 4カテゴリ: L3投入 / L2c投入 / 保留 / 見送り
- 再検討条件は具体ビジネスイベント形式で書く
- 再評価時は必ずDECISIONSを参照して重複判断を避ける

## 活用目的
1. **開発設計**: Claude.aiからMCP経由で参照、具体的な設計書を出力
2. **開発支援**: Hostingerターミナル開発時にナレッジ参照
3. **情報発信**: 主にL2ユースケースの記事を自動生成して発信

## 残タスク（優先順、2026-05-01更新）

1. [ ] **OpenRouter APIキーローテーション**（最優先・セキュリティ）
2. [ ] **旧形式13件のリネーム再投入**（other枠、INDEX.md記載の計画通り）
3. [ ] **L1-old 1件のリネーム**（awesome-agent-skills-l1 → l3化検討）
4. [ ] **entity_chunks/relation_chunks のゴースト要素クリーンアップ**（LightRAG公式手順調査が必要）
5. [ ] **L2c → L2 昇格候補の検証**（実装による検証実施）
6. [ ] **L2拡充**（現18件 → 目標25件）
7. [ ] **2段階クエリ戦略のスキル化**（理論はDATA-SCHEMA.md記載済、スキル化のみ未着手）

## 完了タスク履歴

### 2026-05-01: 整理・再棚卸し（Phase 12）
- [x] doc_fullゴースト21件削除（chunks 71件 + vdb_chunks 71件巻き込み）
- [x] doc_full = doc_status = 157 の整合性達成
- [x] 全157件のレイヤー別棚卸し（INDEX.md全面書き換え）
- [x] 新規L3投入2件（trellis-mindfold-l3 / voxcpm-openbmb-l3）
- [x] 見送り判断1件（docker-android budtmo）
- [x] DECISIONS.md / INDEX.md / RESUME.md 同期更新
- [x] 旧形式13件のリネーム計画明文化

### 2026-04-19: Phase 3 無サフィックス再投入
- [x] 用途別検索精度の実地検証（6テストクエリ）
- [x] エンティティ構造の解明（lightrag_full_entities と vdb_entity の役割分担）
- [x] Phase 1a 重複24件削除（skill系旧版18+プロジェクト進捗2+孤児4）
- [x] crewai 削除→L3再投入（エンティティ純度問題の検証）
- [x] バッチ1 マルチエージェント3件再投入（langgraph/mastra/n8n）
- [x] バッチ2 Web系3件再投入+llmfit削除（firecrawl/browser-use/ffmpeg）
- [x] バッチ3 SaaS/取引6件再投入+nemo-agent-toolkit削除（anthropic-cookbook/ccxt/freqtrade/n8n-as-code/supabase/vercel）

### 2026-04-18: L1 v3再設計 + L2c拡充
- [x] DATA-SCHEMA.md v2/v3更新（L2cレイヤー、4判断カテゴリ、L1再定義）
- [x] KNOWLEDGE-DECISIONS.md新設
- [x] L2c本体投入5パターン
- [x] mcp2cli L3投入 + Schema-driven Lazy CLI L2c投入
- [x] L1から汎用パターン3件をL2cへ昇格
- [x] L1削除10件 + L1維持3件をL1-Infra/L1-Opsにリネーム

## Claude.aiプロジェクト スキル
- combination-architect: ナレッジ組み合わせ→企画提案・設計・L2/L3投入
- knowledge-navigator: ナレッジ検索→実装提案・技術選定・問題解決
- skill-verifier: Claudeception方式でナレッジ/スキル品質検証

---

## 2026-05-24 フェーズ1A セッション1+2（圧縮ミドルウェア実装）

### セッション1（記録漏れ補修）
- 実施日: 2026-05-23(推定、コミットb54d116時点)
- 完了: ベースライン計測完了
  - tools/list: 272 tokens
  - query1(openspec/naive): 729 tokens
  - query2(mcp/hybrid): 1234 tokens
  - query3(agent/hybrid): 1171 tokens
- 成果物: /docker/lightrag/measurement/baseline/ 配下4ファイル + count_tokens.py
- ブランチ: feature/compression-middleware
- コミット: b54d116

### セッション2
- 実施日: 2026-05-24
- 完了: tool description簡潔化
  - 6箇所のdescription削減(search_knowledge / list_knowledge / list_projects / upload_document + 内部フィールド3)
  - file_nameの例示「skill-docx-l3.txt」のみ保持
- 効果: tools/list 272 -> 201 tokens (-26%)
- バックアップ: scripts/mcp_remote.py.bak-session2
- 重要発見: search_knowledgeの結果はLLM合成のため毎回変動(±20%)
  -> セッション3着手前に複数回実行→中央値方式の測定スクリプトを設計する必要あり
- 次回開始時: セッション3(圧縮ミドルウェア基盤=パススルー実装)の前に測定方法再設計


## 2026-05-24 フェーズ1A セッション3(圧縮ミドルウェア基盤=パススルー)

### 完了
- scripts/middleware/compression.py を新設(58行、パススルー実装)
- scripts/mcp_remote.py の do_search() 出口にミドルウェア組み込み
  - import: from middleware.compression import compress_response
  - 正常系 + エラー系 両方の return をミドルウェア経由に
- [compression] ログを stderr→journalctl に出力する設計
- 安全装置: 例外時は元テキストをそのまま返す try/except 構造

### 動作確認
3クエリすべてで input == output、delta=+0.0% を確認:
- openspec/naive: 2461 bytes
- mcp/hybrid:     3574 bytes
- agent/hybrid:   3147 bytes

セッション2時点のレスポンスバイト数と完全一致(2670/3806/3338)。

### 重要な発見・申し送り
1. do_search() に既に簡易圧縮(件数制限・文字数制限・重複除去)が
   組み込み済み。フェーズ1Aで追加するミドルウェアは
   「既存圧縮 + 追加圧縮」の二段構造になる。
2. ベースライン取得時の「±20%変動」記録は誤認だった可能性大。
   3クエリ全てで決定論的(5回連続同一バイト数)であることを実証。
   → 中央値方式は不要、1回計測で十分。
3. ナレッジ件数が動くと比較が崩れるため、セッション4以降は
   「同セッション内のbefore/after差分」で評価する方針に修正済み。
4. ベースラインとセッション2の比較で query1 が +17% 増加していた
   理由は不明(ナレッジ件数変動の可能性)。セッション4以降は気にしない。

### 成果物
- 新規ファイル: scripts/middleware/__init__.py
- 新規ファイル: scripts/middleware/compression.py (58行)
- 修正ファイル: scripts/mcp_remote.py (+5 / -2)
- 比較基準CSV: measurement/baseline_vs_s2.csv (未コミット保留)

### コミット
- da30dc5 feat(mcp): add compression middleware skeleton (pass-through)
- ブランチ: feature/compression-middleware (push済み)

### 棚上げ中(stash)
- stash@{0}: 20260510-cleanup-pending
  (config/project_profiles.json, docs/KNOWLEDGE-DECISIONS.md, docs/KNOWLEDGE-INDEX.md)
  → フェーズ1A完了後にmainブランチで処理

### 次回開始時: セッション4(Deduplication実装)

---

## 2026-06-01 検索品質チューニング（後段キャップ調整）

### 議題1の結論: 「10件上限」は誤認だった
- 記憶/旧ノートの「検索しきれない真因＝検索結果10件上限」は**実体と不一致**だった。
- 真因は do_search() の**後段カテゴリ別キャップ** `entities/relationships/chunks = 5/5/3`。
  - 「10」は references の `[:10]` を見た誤認と判断。
- 上流 /query/data は top_k 無指定でデフォルト依存だが潤沢に返している（実測 36/168/17）。
  recall を殺していたのは上流ではなく後段キャップ。
  - 破棄率: entities 86% / relationships 97% / chunks 82%。

### 実施: relationships キャップ 5→15
- relationships は「XがYと組み合わさる/Yに適用される」型の**組み合わせ設計知識**を運ぶ。
  これがL2が表現したい「組み立て発想」と同質。5キャップで97%が検索から締め出されていた。
- 3クエリ検証（RAG/マルチエージェント/n8n）: bytes 3535→5032(+42%)、4.6-5.1KBで安定。
  良質な組み合わせエッジが6件目以降に多数（例: RAG app + LangGraph = Dual-loop / n8n→Claude Code→app のアップセル連鎖）。
- コミット 5f45975（feature/compression-middleware上、compressionとは独立コミット）。
- 本番反映済み（mcp-lightrag restart）。本番経由で relationships:15/bytes:5032 確認。
- compression は level=off のままなので、これは純粋なキャップ単体の効果。

### 議題2（L2供給増）は保留・後日再評価
- L2は分母184件中19件=10.3%（目標20-25%の半分以下、L3が75.5%支配）。
- ただし「組み合わせ知識」は relationships に既に存在し、可視化で表面化できることが判明。
  → **L2を急いで増やす前に、relationships可視化の効果を1-2週間体感**してから供給増の要否を再評価。
- 検証定義の選択肢（A:自環境のみ / B:OSS読解も / C:他者実証も / D:タグで強度区別）は議題2着手時に決定。
  推し: D（verified:self/oss/thirdparty をタグ化、商品配信は self を主軸）。

### 次セッション候補
1. chunks キャップ 3→5 の本文増量検証（圧縮セッション4と掛け合わせて計測）
2. relationships=20 まで攻めるかの再検討（今回は15で確定、ノイズ比増の懸念で据え置き）
3. 議題2着手: L2c→L2昇格レビュー（21件）＋検証定義D決定
4. KNOWLEDGE-INDEX.md ハイブリッド化（自動生成＋手動エリア分離、今回deferred）

### 注: ナレッジ実数は184件（L3=139/L2c=21/L2=19/L1=3/other=2）
旧ヘッダの「157件」「166件」はいずれも古い/誤り。inventory.sh の 184/184/184 が正。

---

## 2026-06-06 リポジトリ評価＆L2c企画セッション

### ナレッジ実数更新
- 本日投入: L3=12件 + L2c=4件 = 計16件
- 投入前184件 → **投入後 約200件**（次回 inventory.sh で正確値を確定すること）
- ※RESUME冒頭ヘッダの「157件」は古い。正は inventory.sh（前回184、本日+16）。

### L3投入（12件）
ecc / quant-mind / vimax / viga / odysseus / syncthing / understand-anything / listmonk / postiz / ppt-master / composio / mattpocock-skills

### L2c投入（4件）
- domain-skillpack-productized-service（ai-recruiter発、ドメイン特化スキルパックのサービス化）
- self-hosted-multichannel-distribution（listmonk+Postiz+n8n配信基盤）
- company-profile-matching-engine（EDINET DB×エージェントのマッチング）
- document-to-sns-image-pipeline（ppt-master+Postiz文書→SNS画像）

### 見送り（4件）
ANUS / API-mega-list / build-your-own-x / ai-recruiter-claude(リポ単体L3)

### 調査のみ
エージェント×企業プロフィール・マッチングエンジン → company-profile-matching-engine-l2c として企画化

### 次セッション候補（本日分の発展）
1. L2c企画3件のうち1つを実装着手（推奨: self-hosted-multichannel = 既存n8n資産が活きる）
2. 参考OSS（b2b-sdr-agent-template/openfang/recsys-agent）のL3投入要否判断
3. inventory.sh で正確な件数確定＋KNOWLEDGE-INDEX.md更新
4. 既存の優先タスク（OpenRouter APIキーローテーション等）は継続


---

## 2026-06-13 record_decision実装セッション(C-2完了)

### 完了
- [x] record_decision ツール実装(scripts/record_decision.py、独立モジュール=C-1流用可能)
- [x] mcp_remote.py 3行パッチ(import / TOOLS / HANDLERS)+ サービス再起動
- [x] 試運転成功: paperclip-l3 投入 + record_decision実弾実行(commit 151a698)
- [x] git identity固定(7272yusuke-design / noreply)
- [x] セキュリティ修復: remote URL埋め込みPAT(ghp_)除去 → gh credential helper化
- [x] systemd drop-in: mcp-lightrag に HOME=/root 付与(gh認証がサービスから動かない問題の修正)

### ルール改訂(投入ルール v3への追記)
- 「管理ドキュメントはVPS上で直接編集」の例外: **KNOWLEDGE-DECISIONS.mdへの判断ログ追記は
  MCP record_decision ツール経由を標準とする**(追記専用・バックアップ付き・自動commit/push)。
  INDEX/RESUME/SCHEMAは引き続きVPS直接編集。
- 投入フロー更新: upload_document → record_decision の2連で1評価が完結(手動貼り付け廃止)

### 安全装置(record_decision)
- 追記前バックアップ(.bak-rd)/ appendモードのみ / 例外時復元 / git失敗でも追記保持
- commit対象は docs/KNOWLEDGE-DECISIONS.md のみ(他の未コミット変更を巻き込まない)
- push先は origin HEAD(ブランチ追従)

### 残タスク・申し送り
- [ ] **露出PAT(ghp_ItVf...)のRevoke確認**(GitHub Settings、未確認なら最優先)
- [ ] DATA-SCHEMA.md の投入フロー記述に record_decision を反映(次回編集時で可)
- [ ] Claude.ai側は次セッションから record_decision を直接呼べる(今セッションはツール一覧キャッシュのため不可だった)
- [ ] 将来: C-1(Claude Codeスキル化)時に record_decision.py を流用 / RESUME.md自動更新は別途検討
