"""LightRAG MCP server response compression middleware.

セッション3時点: パススルー実装(圧縮なし)
セッション4以降: Deduplication / Truncation を順次追加予定
"""
import sys
from typing import Literal

CompressionLevel = Literal["off", "balanced", "aggressive"]

# ログ出力先(journalctlに流れるようstderr)
def _log(msg: str) -> None:
    print(f"[compression] {msg}", file=sys.stderr, flush=True)


def compress_response(response_text: str, level: CompressionLevel = "off") -> str:
    """search_knowledge のレスポンスを圧縮する。

    現時点ではパススルー(何もしない)。
    セッション4以降で実装を追加する。

    Args:
        response_text: do_search() の戻り値テキスト
        level: 圧縮レベル
            - "off": 何もしない(セッション3デフォルト)
            - "balanced": Deduplication ON, Truncation 控えめ(未実装)
            - "aggressive": Deduplication ON, Truncation 強め(未実装)

    Returns:
        圧縮済みテキスト。例外時は元のテキストをそのまま返す。
    """
    input_size = len(response_text.encode("utf-8"))

    try:
        if level == "off":
            output = response_text
        elif level == "balanced":
            # TODO(session4-5): Deduplication + 控えめTruncation
            output = response_text
        elif level == "aggressive":
            # TODO(session4-5): Deduplication + 強めTruncation
            output = response_text
        else:
            _log(f"WARN: unknown level '{level}', falling back to off")
            output = response_text

        output_size = len(output.encode("utf-8"))
        delta_pct = 0.0 if input_size == 0 else (output_size - input_size) / input_size * 100
        _log(
            f"level={level}, input={input_size} bytes, "
            f"output={output_size} bytes, delta={delta_pct:+.1f}%"
        )
        return output

    except Exception as e:
        # 圧縮で何か壊れても本体機能は止めない
        _log(f"ERROR: compression failed ({type(e).__name__}: {e}), passing through")
        return response_text
