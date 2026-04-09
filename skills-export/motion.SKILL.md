改善版SKILL.md全文:

```markdown
---
name: motion
description: Reactでアニメーション実装するときに必ずこのスキルを使え。motion.div、AnimatePresence、layoutId、useScroll、useMotionValue、drag、variants、LazyMotionなどMotion（旧Framer Motion）のAPIが関係する場合は即座に参照せよ。モーダル開閉、ページトランジション、共有要素トランジション、スクロール連動、ドラッグ&ドロップ、リスト並び替えアニメーションの指示があれば適用する。
---

# motion

## 概要
Motion（旧Framer Motion）はReact向けアニメーションライブラリ。`motion.div` による宣言的アニメーション、`AnimatePresence` によるマウント/アンマウント制御、`layoutId` による共有要素トランジション、`useScroll`/`useMotionValue` によるリアクティブパイプラインを提供する。新規プロジェクトでは `motion/react` からインポートする（`framer-motion` は非推奨）。

## いつ使うか
- モーダル・ドロワー・ダイアログの開閉アニメーション
- ページ遷移・ルートトランジション
- リストの追加・削除・並び替えアニメーション
- App Storeカード風の共有要素トランジション（`layoutId`）
- スクロール連動アニメーション（視差効果、プログレスバー）
- ドラッグ&ドロップのインタラクション
- ホバー・タップのマイクロインタラクション
- CSSでは難しいスプリング物理ベースのアニメーション

## 主要コマンド・API

### インストール
```bash
npm install motion
```

### 基本アニメーション
```tsx
import { motion } from "motion/react"

<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  exit={{ opacity: 0, y: -20 }}
  transition={{ duration: 0.3, ease: "easeOut" }}
/>

// スプリング物理
<motion.div
  animate={{ x: 100 }}
  transition={{ type: "spring", stiffness: 300, damping: 20 }}
/>

// ホバー・タップ
<motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} />
```

### Variants（子要素のスタガーアニメーション）
```tsx
const container = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { staggerChildren: 0.1 } },
}
const item = { hidden: { opacity: 0, y: 20 }, visible: { opacity: 1, y: 0 } }

<motion.ul variants={container} initial="hidden" animate="visible">
  {items.map((i) => (
    <motion.li key={i.id} variants={item}>{i.label}</motion.li>
  ))}
</motion.ul>
```

### AnimatePresence（マウント/アンマウント）
```tsx
import { AnimatePresence, motion } from "motion/react"

<AnimatePresence>
  {isOpen && (
    <motion.div
      key="modal"
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.9 }}
    />
  )}
</AnimatePresence>

// リストアイテムの追加・削除
<AnimatePresence mode="popLayout">
  {items.map((item) => (
    <motion.div key={item.id} layout
      initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
    />
  ))}
</AnimatePresence>
```

### layoutId（共有要素トランジション）
```tsx
// リスト側
<motion.div layoutId={`card-${card.id}`}>
  <motion.h2 layoutId={`title-${card.id}`}>{card.title}</motion.h2>
</motion.div>

// 詳細側（同じlayoutIdで自動的にアニメーション接続）
<AnimatePresence>
  {selected && (
    <motion.div layoutId={`card-${selected}`} className="detail">
      <motion.h2 layoutId={`title-${selected}`}>{title}</motion.h2>
    </motion.div>
  )}
</AnimatePresence>
```

### useScroll + useTransform（スクロール連動）
```tsx
import { useScroll, useTransform, useSpring, motion } from "motion/react"

// プログレスバー
const { scrollYProgress } = useScroll()
const scaleX = useSpring(scrollYProgress, { stiffness: 100, damping: 30 })
<motion.div style={{ scaleX, transformOrigin: "left" }} />

// 要素ごとの視差効果
const ref = useRef(null)
const { scrollYProgress } = useScroll({ target: ref, offset: ["start end", "end start"] })
const y = useTransform(scrollYProgress, [0, 1], ["-20%", "20%"])
<motion.img ref={ref} style={{ y }} src={image} />
```

### useMotionValue + useTransform（値の変換パイプライン）
```tsx
import { useMotionValue, useTransform, motion } from "motion/react"

const x = useMotionValue(0)
const opacity = useTransform(x, [-100, 0, 100], [0, 1, 0])
const rotate = useTransform(x, [-100, 100], [-45, 45])

<motion.div style={{ x, opacity, rotate }} drag="x" />
```

### ドラッグ
```tsx
<motion.div
  drag
  dragConstraints={{ left: -100, right: 100, top: -50, bottom: 50 }}
  dragElastic={0.1}
  onDragEnd={(event, info) => {
    if (info.offset.x > 100) handleSwipeRight()
  }}
/>
```

### useAnimate（命令的アニメーション）
```tsx
import { useAnimate, stagger } from "motion/react"

const [scope, animate] = useAnimate()

async function handleClick() {
  await animate("li", { opacity: 1, y: 0 }, { delay: stagger(0.1) })
  await animate(scope.current, { scale: 1.05 }, { type: "spring" })
}

<ul ref={scope}>{/* ... */}</ul>
```

### animate関数（React外・DOM直接操作）
```tsx
import { animate, stagger } from "motion"

animate("#box", { x: 100, opacity: 1 }, { duration: 0.5 })
animate(".card", { y: [20, 0], opacity: [0, 1] }, { delay: stagger(0.1) })
```

### LazyMotion（バンドルサイズ最適化）
```tsx
import { LazyMotion, domAnimation, m } from "motion/react"

// domAnimation: ~18KB(gzip)。layout不要ならこれで十分
<LazyMotion features={domAnimation}>
  <m.div animate={{ opacity: 1 }} />
</LazyMotion>

// domMax: layout/layoutId含む全機能。動的インポートで分割可能
const loadFeatures = () => import("./features").then(res => res.default)
<LazyMotion features={loadFeatures}>
  <m.div layout />
</LazyMotion>
```

## ワークフロー例

### モーダルアニメーションの実装
1. `AnimatePresence` で条件付きレンダリングをラップ
2. オーバーレイとモーダル本体それぞれに `motion.div` + `initial`/`animate`/`exit` を定義
3. `transition` でスプリングの質感を調整（`type: "spring"`, `duration: 0.4`）

```tsx
function Modal({ isOpen, onClose }) {
  return (
    <AnimatePresence>
      {isOpen && (
        <>
          <motion.div className="overlay"
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            onClick={onClose}
          />
          <motion.div className="modal"
            initial={{ opacity: 0, scale: 0.95, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 20 }}
            transition={{ type: "spring", duration: 0.4 }}
          >
            <ModalContent />
          </motion.div>
        </>
      )}
    </AnimatePresence>
  )
}
```

### スクロール連動パララックスセクション
1. `useRef` で対象セクションを参照
2. `useScroll({ target, offset })` でセクション内の進捗を取得
3. `useTransform` で進捗を位置やスケールに変換
4. `motion.div` の `style` に渡す（React再レンダリング不要で高パフォーマンス）

```tsx
function ParallaxHero() {
  const ref = useRef(null)
  const { scrollYProgress } = useScroll({
    target: ref,
    offset: ["start start", "end start"],
  })
  const y = useTransform(scrollYProgress, [0, 1], ["0%", "50%"])
  const opacity = useTransform(scrollYProgress, [0, 0.8], [1, 0])

  return (
    <section ref={ref} style={{ position: "relative", overflow: "hidden" }}>
      <motion.div style={{ y, opacity }}>
        <h1>Hero Content</h1>
      </motion.div>
    </section>
  )
}
```

### ページトランジション（Next.js App Router）
1. ルートレイアウトで `AnimatePresence` をラップ
2. 各ページコンポーネントに `motion.div` + `initial`/`animate`/`exit` を定義
3. `"use client"` ディレクティブを忘れずに付与

```tsx
"use client"
import { AnimatePresence, motion } from "motion/react"
import { usePathname } from "next/navigation"

export default function Template({ children }: { children: React.ReactNode }) {
  const pathname = usePathname()
  return (
    <AnimatePresence mode="wait">
      <motion.div key={pathname}
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -10 }}
        transition={{ duration: 0.2 }}
      >
        {children}
      </motion.div>
    </AnimatePresence>
  )
}
```

## 注意点

### AnimatePresence の落とし穴
- `exit` が動作しない最大の原因: アニメート要素が `AnimatePresence` の**直接の子でない**、または `key` が未設定。条件付きレンダリング時は必ず `key` を付与する
- `mode="wait"` は前の要素が完全に退場してから次が入場する。リストでは `mode="popLayout"` の方が自然
- ページトランジションでは `AnimatePresence` をルーターの外側に配置し、`key` にパス名を渡す

### layoutId のハマりポイント
- `layoutId` はアプリ全体でユニークが必須。ID衝突すると無関係な要素間でアニメーションが発生する
- トランジション中は新旧要素が同時にDOMに存在するため `z-index` 管理が必要
- `layoutId` 要素が同時に2つ以上存在しないよう `AnimatePresence` で片方を必ずアンマウントする

### パフォーマンス
- `layout` プロパティは全子孫の位置を再測定するため、大量要素には `layoutRoot` か `layoutScroll` で測定スコープを限定する
- `width`/`height`/`top` のアニメーションはブラウザのレイアウト再計算を発生させる。`scaleX`/`scaleY` + `layout` で代替する
- `useMotionValue` + `style` はReact再レンダリングをバイパスする。60fps必須の箇所（スクロール連動等）では `useState` ではなくこちらを使う
- `animate` に毎レンダリング新オブジェクトを渡すと無限再アニメーションする。`variants` か定数化で防ぐ

### SSR / Next.js
- `useScroll`・`useMotionValue`・`useAnimate` はクライアントサイドのみ。Next.js App Routerでは `"use client"` ディレクティブが必須
- `LazyMotion` + 動的インポートでSSR時のバンドルサイズを削減できる

### バンドルサイズ
- `motion` フルバンドル: ~50KB(gzip)。`LazyMotion` + `domAnimation` で~18KBに削減可能
- `layout`/`layoutId` 機能は `domMax` に含まれる。レイアウトアニメーション不要なら `domAnimation` で十分
- `m.div`（`LazyMotion` 用の軽量コンポーネント）と `motion.div` を混在させない

### 移行の注意
- `framer-motion` → `motion` パッケージへの移行が進行中。新規は `import { motion } from "motion/react"` を使う
- `useAnimation()` は非推奨。`useAnimate()` に置き換える（戻り値が `[scope, animate]` タプルに変わる）
- `AnimateSharedLayout` は削除済み。`layoutId` + `AnimatePresence` で代替する

## 関連スキル
- **react**: コンポーネント設計・状態管理と組み合わせたアニメーション実装の基盤
- **ui（shadcn/ui）**: shadcnコンポーネントにMotionアニメーションを追加する際のスタイリング統合
- **next.js**: App Router環境でのページトランジション、`"use client"` 境界、`LazyMotion` によるバンドル最適化
- **tailwindcss**: `className` によるレイアウト定義 + Motionによるアニメーション値制御の分担
- **browser-use**: E2Eテストでアニメーション完了を待機する際のセレクタ・タイミング設計
```

**改善サマリ:**

| 基準 | 元 | 改善後 |
|---|---|---|
| 1. description精度 | 抽象的（「UIアニメーション」） | API名をトリガーキーワードに明記（`motion.div`, `AnimatePresence`, `layoutId`, `useScroll`等） |
| 2. 行数 | 333行 | ~290行（重複コード例を統合） |
| 3. コマンド例 | ワークフローと主要APIで重複多い | 主要APIはリファレンス、ワークフローは実践シナリオに役割分担 |
| 4. ワークフロー | 3つ（モーダル/共有要素/スクロール） | 3つ（モーダル/パララックス/**Next.jsページトランジション追加**）。共有要素は主要API節に統合 |
| 5. 注意点 | 最終行が途切れ、`AnimateSharedLayout` 移行情報なし | 文を完成、`AnimateSharedLayout` 削除済み・`useAnimation` 非推奨の具体的移行先を明記 |
| 6. 関連スキル | **欠落** | 5スキル追加（react, ui, next.js, tailwindcss, browser-use） |
