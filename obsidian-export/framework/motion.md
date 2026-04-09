---
source: https://github.com/framer/motion
category: framework
sub_categories: [tool, webapp]
tags: [TypeScript, React, animation, WAAPI, layout-animation, motion, framer-motion, spring-physics]
language: 
ingested: 2026-04-09
source_updated: unknown
status: active
---

# motion

# motion

## 基本情報
- リポジトリ: https://github.com/framer/motion
- カテゴリ: framework
- サブカテゴリ: tool, webapp
- タグ: TypeScript, React, animation, WAAPI, layout-animation, motion, framer-motion, spring-physics
- 最終確認日: 2026-04-09

## 概要
Motion（旧Framer Motion）はReact向けのアニメーションライブラリで、宣言的APIによるレイアウトアニメーション、共有要素トランジション、ジェスチャー、スクロール連動アニメーションなどを提供する。Web Animations API（WAAPI）とJSベースのアニメーションエンジンを組み合わせ、高パフォーマンスなアニメーションを実現する。モノレポ構成でmotion-dom（コアエンジン）、framer-motion（Reactバインディング）、motion-utils（ユーティリティ）に分割されている。

## 設計思想
UIロジックとアニメーションロジックの分離を重視し、宣言的なprops（animate, initial, exit, whileHover等）でアニメーションを記述する設計。ProjectionNodeによるレイアウト投影システムで、CSSレイアウト変更をtransformに変換してGPUアクセラレーションを活用。LazyMotionによる機能の動的ロードでバンドルサイズを最小化。VisualElementという抽象レイヤーでHTML/SVG/Objectの差異を吸収し、モーション値（MotionValue）をリアクティブな状態管理単位として使用する。

## 主要コンポーネント
- VisualElement: HTML/SVG要素の抽象レイヤー。レンダリング、モーション値管理、アニメーション状態を統合管理する基底クラス
- ProjectionNode: レイアウトアニメーションのコアエンジン。要素の実際のレイアウトを測定し、transformで視覚的位置を補正するFlip技術を実装
- AnimatePresence: コンポーネントのマウント/アンマウント時にexitアニメーションを実行するReactコンポーネント
- MotionValue: アニメーション可能な値の基本単位。サブスクリプションベースでレンダリングをバイパスしてDOMを直接更新
- NativeAnimation/JSAnimation: WAAPIとJavaScriptベースのアニメーション実行エンジン。スプリング、キーフレーム、イージングを処理
- frameloop: requestAnimationFrameベースのバッチ処理システム。読み書きを分離してレイアウトスラッシングを防止
- animate(): 命令的APIでDOM要素・オブジェクト・モーション値をアニメートするスタンドアロン関数
- LazyMotion: アニメーション機能を動的インポートで分割ロードし、初期バンドルサイズを削減するコンポーネント

## 実装パターン
- FLIP（First Last Invert Play）: レイアウト変更前後の位置を測定し、transformで視覚的に補正することでCSSレイアウト変更をスムーズにアニメートするProjectionNodeの中核技術
- Variant propagation: 親コンポーネントのvariant変更を子コンポーネントに自動伝播するシステム。Contextを介してアニメーション状態を共有
- Optimized appear（SSR handoff）: サーバーサイドレンダリング時にCSSアニメーションを開始し、ハイドレーション後にJSアニメーションにシームレスに引き継ぐ最適化
- Shared element transition: layoutIdプロパティで異なるDOM要素間のアニメーションを連続させる共有要素トランジション
- Motion value composition: useTransform、useSpring、useMotionTemplate等でMotionValueを合成・変換するリアクティブパイプライン
- Feature bundle splitting: drag、gesture、layoutなどの機能をモジュールとして分割し、必要な機能のみをロードするツリーシェイキング対応設計

## 適用シーン
Reactアプリケーションでページトランジション、モーダル開閉、リスト並び替えなどのUIアニメーションを実装するプロジェクト。App StoreカードUI、ライトボックス、ドラッグ&ドロップ、スクロール連動アニメーション、共有要素トランジションを必要とするWebアプリ。Next.js等のSSR環境でのアニメーション最適化が必要なケースにも対応。

## 注意点・制約
Preactとの互換性なし。React 19はframer-motion 12.0.0-alpha以降が必要。height:autoのアニメーションはDOM測定が必要なため、同要素にpaddingがあると不正確になる場合がある。AnimatePresenceの子要素には安定したkeyが必須。RSC環境ではmotion/react-clientからインポートが必要。ProjectionNodeによるレイアウト測定はパフォーマンスコストが高く、大量要素への適用は注意が必要。


## 関連ナレッジ
- (なし)
