#!/usr/bin/env bash
# measure_dedup.sh — 段階1v: 画面録画のdedup圧縮率実測ツール
# layout-preserving-retrieval-hybrid-l2c の検証段階1v を実行する。
# claude-video方式: 1fps抽出 → 16x16グレースケール → 平均絶対差分でdedup
# 使い方: ./scripts/measure_dedup.sh <video-file> [threshold]
#   threshold: 平均絶対差分の閾値(0-255)。既定8。小さいほど厳しく残す。
set -euo pipefail
VIDEO="${1:?usage: measure_dedup.sh <video> [threshold]}"
THRESH="${2:-8}"
TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT

DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$VIDEO")
ffmpeg -y -loglevel error -i "$VIDEO" -vf "fps=1,scale=16:16" \
  -pix_fmt gray -f rawvideo "$TMP/frames.raw"

python3 - "$TMP/frames.raw" "$THRESH" "$DUR" << 'PY'
import sys
raw, thresh, dur = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
data = open(raw, 'rb').read()
n = len(data) // 256
frames = [data[i*256:(i+1)*256] for i in range(n)]
kept, spans, last = [], [], None
for i, f in enumerate(frames):
    if last is None or sum(abs(a-b) for a, b in zip(f, last))/256.0 > thresh:
        kept.append(i)
        spans.append([i, i])
        last = f
    else:
        spans[-1][1] = i
comp = n / max(len(kept), 1)
print(f"動画長          : {dur:.0f}秒")
print(f"抽出フレーム(1fps): {n}")
print(f"dedup後の代表数  : {len(kept)}")
print(f"圧縮率          : {comp:.1f}x  (閾値={thresh})")
print(f"1時間あたり換算  : {len(kept)/max(dur,1)*3600:.0f}枚")
print()
print("代表フレームのカバー区間(論点7の実データ / mm:ss形式):")
for s, e in spans:
    print(f"  {s//60:02d}:{s%60:02d} - {e//60:02d}:{e%60:02d}  ({e-s+1}秒)")
PY
