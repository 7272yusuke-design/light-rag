ファイルの書き込み権限が必要です。許可をお願いします。

以下がSKILL.md全文です:

```markdown
---
name: awesome-design-md
description: UIを生成・実装するときに特定ブランドのデザインを再現したい場合は必ずこのスキルを使え。「Vercelっぽく」「Stripe風に」「GitHub風のUI」「Notion風デザイン」のようにブランド名を含むUI生成指示があれば即座に参照せよ。DESIGN.mdをプロジェクトルートに配置してAIエージェントにデザイントークン（カラーパレット・タイポグラフィ・コンポーネントスタイル・レイアウト原則）を読み込ませるとき、Google Stitch DESIGN.mdフォーマットに準拠したデザインシステムを構築・適用するとき、getdesign.mdからブランドデザインを取得するときに適用する。
---

# awesome-design-md

## 概要
著名なWebサイト・プロダクトのビジュアルデザインシステムをMarkdown形式（DESIGN.md）で収集したキュレーションリポジトリ。Google Stitchが提唱するDESIGN.mdフォーマットに準拠し、60近くの有名サービス（Vercel, Stripe, GitHub, Notion, Linear, Supabase, Tailwind, Figma等）のデザイン言語を提供する。LLMが最も読みやすいMarkdown形式を採用し、Figmaエクスポートやカスタムトークンファイル不要で、プロジェクトルートに置くだけで即座に利用可能な「プレーンテキストデザインシステム」を実現する。

- リポジトリ: https://github.com/VoltAgent/awesome-design-md
- デザインホスティング: https://getdesign.md

## いつ使うか
- 「〇〇っぽいUIを作って」というブランド指定のUI生成指示があるとき
- AIコーディングエージェントにデザインシステムを読み込ませたいとき
- プロジェクトにDESIGN.mdを導入してデザイン一貫性を担保したいとき
- 既存ブランドのカラーパレット・タイポグラフィ・コンポーネントスタイルを参照したいとき
- Google Stitch DESIGN.mdフォーマットに準拠したデザインドキュメントを作成したいとき
- デザイントークンをコードに落とし込む際の具体的な値（HEX, フォントサイズ, スペーシング等）が必要なとき

## 収録ブランド（主要例）
Airbnb, Apple, AWS, Cloudflare, Discord, Dribbble, Figma, GitHub, GitLab, Google, Hacker News, Heroku, IKEA, Instagram, Linear, Medium, Netflix, Notion, npm, OpenAI, Pinterest, Product Hunt, Reddit, Shopify, Slack, Spotify, Stripe, Supabase, Tailwind CSS, Tesla, TikTok, Twitch, Twitter/X, Uber, Vercel, YouTube, Zoom 等

## リポジトリ構造
```
awesome-design-md/
├── design-md/
│   ├── vercel/
│   │   ├── README.md          # getdesign.mdへのリダイレクト
│   │   └── DESIGN.md          # デザイントークン本体（移行済みの場合はREADMEのみ）
│   ├── stripe/
│   │   └── README.md
│   ├── github/
│   │   └── README.md
│   └── ...（60近くのブランド）
├── preview.html               # ライトモード視覚カタログ
└── preview-dark.html          # ダークモード視覚カタログ
```

## DESIGN.mdフォーマット（Stitch準拠 9セクション構成）

```markdown
# Brand Name — DESIGN.md

## Visual Theme
全体のトーン・ムード・印象を記述

## Color Palette
### Primary
- Brand Blue: #0070F3
- Brand Blue Hover: #0060DF
### Neutral
- Background: #FFFFFF
- Foreground: #171717
- Muted: #666666
### Semantic
- Success: #0070F3
- Error: #EE0000
- Warning: #F5A623

## Typography
- Font Family: "Inter", -apple-system, sans-serif
- Heading 1: 48px / 700 / -0.02em
- Heading 2: 36px / 600 / -0.01em
- Body: 16px / 400 / 1.6 line-height
- Small: 14px / 400
- Mono: "Geist Mono", monospace

## Components
### Button
- Primary: bg #0070F3, text #FFFFFF, radius 8px, padding 8px 16px
- Secondary: bg transparent, border 1px #333, text #FFFFFF
- Hover: brightness(1.1), transition 150ms ease
### Card
- Background: #1A1A1A
- Border: 1px solid #333
- Radius: 12px
- Padding: 24px
### Input
- Background: #111
- Border: 1px solid #333
- Focus border: #0070F3
- Radius: 8px

## Layout
- Max width: 1200px
- Grid: 12 columns, 24px gap
- Section spacing: 64px
- Content padding: 0 24px

## Elevation
- Level 0: none
- Level 1: 0 2px 8px rgba(0,0,0,0.08)
- Level 2: 0 8px 24px rgba(0,0,0,0.12)

## Do's and Don'ts
- Do: ミニマリスティックなスペーシングを保つ
- Do: モノスペースフォントをコード表示に使用
- Don't: 3色以上のアクセントカラーを同時使用
- Don't: 丸すぎるborder-radius（max 12px）

## Responsive
- Mobile: < 768px, single column, 16px padding
- Tablet: 768-1024px, content max 720px
- Desktop: > 1024px, content max 1200px

## Agent Prompt Guide
このデザインを再現する際のAIエージェント向け要約指示
```

## 主要コマンド・使い方

### DESIGN.mdの取得と配置
```bash
# リポジトリをクローンして特定ブランドのDESIGN.mdを取得
git clone https://github.com/VoltAgent/awesome-design-md.git
cp awesome-design-md/design-md/vercel/DESIGN.md ./DESIGN.md

# または curl で直接取得（getdesign.mdホスティングから）
curl -o DESIGN.md https://getdesign.md/vercel/DESIGN.md

# プロジェクトルートに配置するだけでAIエージェントが自動認識
ls ./DESIGN.md
```

### 複数ブランドの参照
```bash
# 複数ブランドを比較参照したい場合
mkdir -p .design-references/
cp awesome-design-md/design-md/stripe/DESIGN.md .design-references/stripe.md
cp awesome-design-md/design-md/linear/DESIGN.md .design-references/linear.md
cp awesome-design-md/design-md/vercel/DESIGN.md .design-references/vercel.md
```

### プレビューの確認
```bash
# ブラウザでデザイントークンの視覚カタログを確認
open awesome-design-md/preview.html        # ライトモード
open awesome-design-md/preview-dark.html   # ダークモード
```

### カスタムDESIGN.mdの作成（Stitchフォーマット準拠）
```bash
# 既存ブランドをベースに自社デザインシステムを作成
cp awesome-design-md/design-md/vercel/DESIGN.md ./DESIGN.md
# エディタで値を自社ブランドに書き換える
```

## ワークフロー例

### 典型例1: 「Vercelっぽいランディングページ」を生成
```bash
# 1. DESIGN.mdを取得してプロジェクトルートに配置
curl -o DESIGN.md https://getdesign.md/vercel/DESIGN.md

# 2. Claude Codeに指示（DESIGN.mdが自動的にコンテキストに入る）
# プロンプト例:
# 「DESIGN.mdに従って、ダークテーマのランディングページを作成して。
#   ヒーローセクション、特徴3カラム、CTAボタン、フッターを含めて。」

# 3. 生成されたコードはDESIGN.mdのカラーパレット・タイポグラフィ・
#    コンポーネントスタイルに自動的に準拠する
```

### 典型例2: 既存プロジェクトにデザイン一貫性を導入
```bash
# 1. 現在のUIに最も近いブランドのDESIGN.mdを選択
#    （例: SaaSダッシュボードならLinear、ECサイトならShopify）

# 2. DESIGN.mdを取得
curl -o DESIGN.md https://getdesign.md/linear/DESIGN.md

# 3. プロジェクト固有のカスタマイズを追加
cat >> DESIGN.md << 'EOF'

## Project-Specific Overrides
- Primary Brand Color: #6C5CE7 (上書き)
- Logo Font: "Poppins", sans-serif
- Card max-width: 400px
EOF

# 4. 以降のUI生成・修正はすべてDESIGN.mdを基準に行われる
```

### 典型例3: デザインシステムの比較検討
```bash
# 1. 候補ブランドのDESIGN.mdを収集
mkdir -p .design-candidates/
for brand in vercel stripe linear notion supabase; do
  curl -o ".design-candidates/${brand}.md" "https://getdesign.md/${brand}/DESIGN.md"
done

# 2. 各ブランドのカラーパレットやタイポグラフィを比較
# プロンプト例:
# 「.design-candidates/ 内の5つのDESIGN.mdを比較して、
#   カラーパレット・タイポグラフィ・ボタンスタイルの違いを表にまとめて。」

# 3. 最適なブランドをベースに選定し、DESIGN.mdとしてプロジェクトルートに配置
cp .design-candidates/linear.md ./DESIGN.md
```

### 典型例4: 自社DESIGN.mdをStitchフォーマットで新規作成
```bash
# 1. テンプレートとして既存ブランドのDESIGN.mdをコピー
curl -o DESIGN.md https://getdesign.md/vercel/DESIGN.md

# 2. Claude Codeに指示して自社ブランドに書き換え
# プロンプト例:
# 「このDESIGN.mdを以下の自社ブランドガイドラインに書き換えて:
#   - プライマリカラー: #2D5BFF
#   - フォント: Noto Sans JP
#   - テーマ: クリーンでプロフェッショナル
#   - 角丸: 6px統一
#   9セクション構成は維持すること。」

# 3. preview.htmlでトークンの視覚確認
# preview.htmlをコピーして自社DESIGN.mdを読み込むように修正
```

## 注意点

### コンテンツの所在
- 実際のDESIGN.mdファイルの多くはgetdesign.mdホスティングサービスに移行済み。リポジトリ内のディレクトリにはREADME.md（リダイレクト）のみ存在する場合がある
- `curl`でgetdesign.mdから取得する場合、URLの正確なパスはリポジトリ内のREADME.mdに記載されている正規URLを確認すること

### ブランドデザインの著作権
- 抽出されたデザイントークンは公開CSSから取得したもの。各ブランドのビジュアルアイデンティティの所有権を主張するものではない
- 商用プロダクトでブランドデザインをそのまま使う場合は、そのブランドのガイドラインとライセンスを確認すること
- あくまで「参考」「インスピレーション」としての利用が前提。完全なコピーは避ける

### DESIGN.mdの鮮度
- ブランドはデザインシステムを頻繁に更新する。リポジトリのDESIGN.mdが最新のブランドデザインと一致しない場合がある
- 重要なプロジェクトでは、対象ブランドの公式サイトのCSSと照合して値を確認すること

### コントリビューション制限
- PR受付は既存ファイルの修正のみ。新規DESIGN.md追加は受け付けていない
- 新規ブランドの追加はgetdesign.mdサービス側で管理されている

### DESIGN.mdの配置と認識
- Claude Code等のAIエージェントがDESIGN.mdを自動認識するかはエージェントの実装に依存する。明示的に「DESIGN.mdを読んで」と指示した方が確実
- 複数のDESIGN.mdを同時に読み込ませると指示が競合する可能性がある。1プロジェクト1 DESIGN.mdが原則
- DESIGN.mdが長大な場合（1000行超）、AIエージェントのコンテキストを圧迫する。必要なセクションのみ抜粋して配置する方法も検討すること

### Stitchフォーマットとの互換性
- Google Stitchが提唱する9セクション構成に準拠しているが、ブランドによってはセクションが省略されている場合がある
- カスタムDESIGN.mdを作成する場合も9セクション構成を維持することで、ツール間の互換性が保たれる

## 関連スキル
- **ui（shadcn/ui）**: DESIGN.mdのデザイントークンをshadcn/uiのテーマ変数（CSS custom properties）にマッピングし、コンポーネントライブラリと統合する
- **motion**: DESIGN.mdで定義されたブランドのトーンに合わせたアニメーション（トランジション速度・イージング）の実装
- **frontend-design**: DESIGN.mdのレスポンシブセクションに基づくブレークポイント設計やレイアウトグリッドの実装
- **cli**: `curl`や`jq`でDESIGN.mdからデザイントークンを抽出し、CSS変数やTailwind設定に変換するパイプライン構築
- **graphify**: プロジェクトのコンポーネント構造をナレッジグラフ化し、DESIGN.mdのどのトークンがどのコンポーネントで使われているかを可視化
```
