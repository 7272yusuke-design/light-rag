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

- L3投入: 2件（openclaude, rtk）
- L2c候補（本体未投入）: 2件（video-use、rtkのL2c部分）
- 保留: 2件（MiniCode, Agent Lightning）
- 見送り: 2件（Documenso, JeecgBoot）

**合計**: 7件の評価実績

---

## 次のアクション

1. rtk・video-useのL2c本体投入（LightRAGへupload_document）
2. 未確認のURL（rtk, MiniCode, JeecgBoot, Agent Lightning）を次セッションで補完
3. 新規リソース評価時は本ドキュメント末尾に追記
