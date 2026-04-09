#!/bin/bash
set -euo pipefail
META_JSON="${1:?Usage: $0 <meta.json> [-o output_dir]}"
OUTPUT_DIR="${3:-.}"
REPO_NAME=$(python3 -c "import json; m=json.load(open('$META_JSON')); print(m.get('repo_name', m.get('name', 'unknown')))")

mkdir -p "$OUTPUT_DIR"
SKILL_PATH="$OUTPUT_DIR/${REPO_NAME}.SKILL.md"

echo "SKILL.md生成中（skill-creator経由）: $REPO_NAME..."

cd /docker/lightrag
claude -p "
skill-creatorの手法に従って、以下のメタデータからSKILL.mdを作成してください。

メタデータ:
$(cat "$META_JSON")

要件:
- YAMLフロントマター（name + description）必須
- descriptionはトリガー条件を明確に、やや押しが強めに
- 本体500行以下
- コマンド例は具体的でコピペ可能に
- ワークフロー例を含める
- 注意点・ハマりポイントを含める
- 関連スキルを含める

SKILL.md全文のみを出力。前置き・説明不要。
" > "$SKILL_PATH"

echo "OK: $SKILL_PATH"
