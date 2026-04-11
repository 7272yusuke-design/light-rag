# GSD計画: LightRAG 自己進化ループ
**作成日:** 2026-04-11
**目的:** ナレッジの品質を自動的に計測・分析・改善するセルフループの構築

---

## 設計根拠（使用ナレッジ）

| パターン | ソース | レベル | 採用箇所 |
|---------|--------|--------|---------|
| EvolutionLoop（keep/discard） | autoresearch | 3 | 進化ステップ |
| SelfEvolvingSystem（execute_and_learn） | OpenSpace | 3 | 学習ステップ |
| run_loop.py反復最適化（60/40 split） | skill-creator | 1 | 評価ステップ |
| check_freshness.py（180日鮮度） | LightRAG既存 | - | 分析ステップ |
| Ingestion Pipeline | ARCHITECTURE.md | - | 進化ステップ |

---

## ループ全体図

    [1] 計測（常時）
       search_knowledge.sh → search_log.jsonl
            ↓
    [2] 分析（cron週次 or 手動）
       analyze_usage.py → evolution_candidates.json
            ↓
    [3] 進化（autoresearch EvolutionLoopパターン）
       evolve_knowledge.py: backup → repomix → LLM再要約 → 仮投入
            ↓
    [4] 評価（skill-creator 60/40パターン）
       eval_quality.py: テストクエリ10件 → 期待Doc上位3件判定
            ↓
       score向上 → Keep（git commit）
       score低下 → Discard（旧版に戻す）
            ↓
    [5] 学習（OpenSpace SelfEvolvingSystemパターン）
       evolution_history.jsonlに履歴蓄積 → 次回の進化に活用
            ↓
    [6] 記録
       update_knowledge_index.py + RESUME.md更新 + git push
            ↓
       [1]に戻る

---

## Phase 1: 計測基盤

| # | タスク | 実装量 | 完了条件 |
|---|--------|--------|----------|
| 1-1 | search_knowledge.shにログ追記 | 3行追加 | search_log.jsonlに記録される |
| 1-2 | MCP mcp_lightrag.pyにもログ追記 | 5行追加 | MCPからの検索もログに記録 |

ログフォーマット（search_log.jsonl）:

    {"timestamp":"2026-04-11T12:00:00Z","query":"ccxt WebSocket","mode":"hybrid","project":"openclaw","hit_docs":["ccxt_level3.txt"],"source":"cli"}

---

## Phase 2: 分析エンジン

| # | タスク | 実装量 | 完了条件 |
|---|--------|--------|----------|
| 2-1 | analyze_usage.py 新規作成 | 1時間 | evolution_candidates.jsonが生成される |

ロジック:
1. search_log.jsonlを読み込み、ドキュメントごとのヒット頻度を集計
2. KNOWLEDGE-INDEX.mdからレベル情報を取得
3. 候補判定:
   - 高頻度（週3回以上） x レベル0-1 → レベルアップ候補
   - ヒット0件のクエリパターン → ナレッジ不足領域
   - 180日以上未更新 → 鮮度チェック候補（check_freshness.py流用）
4. evolution_candidates.jsonに出力

出力フォーマット:

    {
      "level_up": [
        {"doc": "langgraph_lightrag.txt", "current_level": 0, "hit_count": 12, "priority": "high"}
      ],
      "missing": [
        {"query_pattern": "websocket reconnection", "frequency": 5}
      ],
      "stale": [
        {"doc": "crewai_lightrag.txt", "last_updated": "2026-04-09", "days_old": 180}
      ]
    }

---

## Phase 3: 進化エンジン（autoresearch EvolutionLoopパターン）

| # | タスク | 実装量 | 完了条件 |
|---|--------|--------|----------|
| 3-1 | evolve_knowledge.py 新規作成 | 2時間 | 候補ドキュメントの自動レベルアップが動作 |
| 3-2 | テストクエリ定義 test_queries.json | 30分 | 10件のクエリx期待Docペアが定義済み |

核心ロジック（autoresearchパターン適用）:

    class KnowledgeEvolver:
        # autoresearch EvolutionLoop のナレッジ版
        def __init__(self, lightrag_api, eval_func):
            self.api = lightrag_api
            self.eval_func = eval_func
            self.history = load_history("evolution_history.jsonl")

        def evolve(self, candidate):
            # 1. backup: 旧ドキュメントを保存
            old_doc = self.api.get_document(candidate["doc_id"])

            # 2. modify: repomix → LLM再要約（Level3プロンプト）
            new_doc = self.regenerate(candidate)

            # 3. evaluate: テストクエリで検索品質計測
            old_score = self.eval_func(candidate["test_queries"])
            self.api.delete_and_upload(candidate["doc_id"], new_doc)
            new_score = self.eval_func(candidate["test_queries"])

            # 4. keep or discard
            if new_score >= old_score:
                self.keep(candidate, new_score)
            else:
                self.discard(candidate, old_doc)

            # 5. 履歴蓄積（OpenSpace SelfEvolvingSystemパターン）
            self.record_history(candidate, old_score, new_score)

---

## Phase 4: 評価エンジン（skill-creator反復評価パターン）

| # | タスク | 実装量 | 完了条件 |
|---|--------|--------|----------|
| 4-1 | eval_quality.py 新規作成 | 1時間 | テストクエリ10件でスコア算出が動作 |

test_queries.json:

    [
      {"query": "ccxt WebSocket接続", "expected_docs": ["ccxt_level3.txt"]},
      {"query": "freqtrade IStrategy 戦略定義", "expected_docs": ["freqtrade_level3.txt"]},
      {"query": "n8n Webhookトリガー", "expected_docs": ["n8n_level3.txt"]},
      {"query": "openclaw プラグイン作成", "expected_docs": ["openclaw_level3.txt"]},
      {"query": "autoresearch keep discard ループ", "expected_docs": ["autoresearch_level3.txt"]},
      {"query": "OpenSpace スキル自己進化", "expected_docs": ["openspace_level3.txt"]},
      {"query": "CrewAI Agent Task Crew定義", "expected_docs": ["crewai_lightrag.txt"]},
      {"query": "LangGraph StateGraph チェックポイント", "expected_docs": ["langgraph_lightrag.txt"]},
      {"query": "Supabase 認証 RLS", "expected_docs": ["supabase_lightrag.txt"]},
      {"query": "browser-use Playwright LLM操作", "expected_docs": ["browser-use_lightrag.txt"]}
    ]

評価ロジック:

    def evaluate(test_queries, api):
        score = 0
        for tq in test_queries:
            results = api.search(tq["query"])
            hit_docs = extract_doc_names(results)
            if any(exp in hit_docs[:3] for exp in tq["expected_docs"]):
                score += 1
        return score / len(test_queries)  # 0.0 ~ 1.0

合格基準: 0.8 (80%) 以上

---

## Phase 5: 学習・記録（OpenSpace SelfEvolvingSystemパターン）

| # | タスク | 実装量 | 完了条件 |
|---|--------|--------|----------|
| 5-1 | evolution_history.jsonl蓄積 | evolve_knowledge.pyに含む | 履歴が蓄積される |
| 5-2 | 進化レポート生成 | 30分 | 進化結果サマリーが出力される |

evolution_history.jsonl:

    {"timestamp":"2026-04-11","doc":"langgraph","old_score":0.3,"new_score":0.8,"action":"keep","iteration":1}
    {"timestamp":"2026-04-11","doc":"browser-use","old_score":0.5,"new_score":0.4,"action":"discard","iteration":1}

---

## オーケストレーション

### Option A: cron（シンプル）

    # 週1で実行
    0 3 * * 0 /docker/lightrag/scripts/evolve.sh >> /var/log/evolve.log 2>&1

### Option B: n8n（可視化・通知付き）
- Schedule Trigger（週1）→ evolve.sh実行 → 結果をSlack通知
- ダッシュボードで進化履歴・スコア推移を表示

---

## 実装順序

| Phase | 内容 | 依存 | 推定時間 |
|-------|------|------|---------|
| Phase 1 | 計測基盤（ログ追記） | なし | 15分 |
| Phase 2 | 分析エンジン | Phase 1 | 1時間 |
| Phase 3 | 進化エンジン | Phase 2 + Phase 4 | 2時間 |
| Phase 4 | 評価エンジン | なし | 1.5時間 |
| Phase 5 | 学習・記録 | Phase 3 | 30分 |
| 統合 | evolve.sh + cron設定 | 全Phase | 30分 |
| **合計** | | | **約6時間** |

---

## 進捗トラッキング
各タスク完了時にこのファイルを更新する。
