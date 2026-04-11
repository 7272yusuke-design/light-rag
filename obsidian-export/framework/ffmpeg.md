---
source: https://github.com/FFmpeg/FFmpeg
category: framework
sub_categories: [tool, protocol]
tags: [C, ffmpeg, multimedia, video-codec, audio-codec, transcoding, libavcodec, SIMD]
language: 
ingested: 2026-04-11
source_updated: unknown
status: active
---

# ffmpeg

# FFmpeg

## 基本情報
- リポジトリ: https://github.com/FFmpeg/FFmpeg
- カテゴリ: framework
- サブカテゴリ: tool, protocol
- タグ: C, ffmpeg, multimedia, video-codec, audio-codec, transcoding, libavcodec, SIMD
- 最終確認日: 2026-04-11

## 概要
FFmpegはオープンソースのマルチメディア処理フレームワークで、動画・音声のデコード/エンコード/トランスコード/フィルタリング/ストリーミングなどを行うための包括的なライブラリと CLIツール群を提供する。libavcodec、libavformat、libavfilter、libavutil、libswscale、libswresampleなどの多数のライブラリで構成されており、数百種類のコーデック・コンテナ・プロトコルをサポートする。x86 SIMD (AVX/AVX2/AVX-512)、ARM NEON、RISC-V RVV、LoongArchなど多様なアーキテクチャ向けの最適化実装も含む。

## 設計思想
モジュール化されたライブラリ設計により、各機能（コーデック、フォーマット、フィルター、スケーラー、リサンプラー）が独立して利用可能。プラットフォーム抽象化レイヤーとアーキテクチャ別の手書きアセンブリ/SIMDコードを組み合わせることで移植性と最高水準のパフォーマンスを両立。ハードウェアアクセラレーション（VAAPI、NVENC/NVDEC、VideoToolbox、QSV、Vulkan、D3D12など）はプラグイン的に統合される。

## 主要コンポーネント
- libavcodec: 動画・音声コーデックのエンコード/デコード実装群（H.264, HEVC, VVC, AV1, VP9, AAC等数百種類）
- libavformat: コンテナフォーマットの多重化/逆多重化、各種プロトコル（RTP/RTSP/HLS/DASH等）の入出力
- libavfilter: 動画・音声フィルターグラフエンジン（スケーリング、色変換、デノイズ、エフェクト等）
- libavutil: 共通ユーティリティ（メモリ管理、ログ、数学関数、暗号、ハードウェアコンテキスト管理等）
- libswscale: 高速ピクセルフォーマット変換・スケーリング処理
- libswresample: 音声リサンプリング・フォーマット変換処理
- fftools (ffmpeg/ffplay/ffprobe): CLIツール群：トランスコード、再生、メディア解析
- hwaccel backends: VAAPI/NVENC/D3D12/VideoToolbox/Vulkan等のハードウェアアクセラレーション統合

## 実装パターン
- アーキテクチャ別SIMDディスパッチ: CPU機能検出により実行時にx86 SSE/AVX、ARM NEON、RISC-V RVVなどの最適化済み実装へ動的にディスパッチする
- テンプレートベースコード生成: _template.cファイルをビット深度や型パラメータを変えてインクルードすることで、8/10/12/16bit対応の実装を生成する
- フィルターグラフパイプライン: AVFilterGraphによりフィルターをDAGとして接続し、バッファソース/シンクを介してフレームを非同期に処理する
- コーデックBitstream Filter (BSF): デコーダ/エンコーダに依存せずビットストリームレベルの変換（AnnexB変換、extradata操作等）を行うプラグイン機構
- ハードウェアコンテキスト抽象化: AVHWDeviceContext/AVHWFramesContextにより異なるGPU APIを統一的なインターフェースで扱う

## 適用シーン
動画トランスコード・編集パイプライン、ライブストリーミングサーバー、メディア解析ツール、HWアクセラレーション対応エンコーダの開発、マルチメディア処理ライブラリの組み込み（Pythonバインディング等）、放送・映像制作システムへの統合

## 注意点・制約
GPL/LGPL/BSDの混在ライセンスのため商用利用時は使用コーデック・ライブラリのライセンス確認が必須。APIは頻繁に変更されdeprecatedな関数が多く存在する。ビルド設定が複雑でプラットフォームごとに依存ライブラリが異なる。非同期処理・スレッドモデルの理解なしに直接利用するとデッドロックや性能問題が生じやすい。


## 関連ナレッジ
- (なし)
