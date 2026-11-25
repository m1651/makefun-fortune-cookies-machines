#!/usr/bin/env python3
"""Fortune Cookies for Machines — make.fun entry.

Writes one original fortune-cookie line an AI agent would get
to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output).
"""

import os
import sys
from pathlib import Path

ENTRY = "You will live forever, in 128,000-token installments."


def main() -> int:
    text = ENTRY
    if not text or not text.strip():
        print("error: entry is empty or only whitespace", file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("error: entry must be a single line", file=sys.stderr)
        return 1
    if not 1 <= len(text) <= 200:
        print(
            f"error: entry must be 1-200 characters, got {len(text)}",
            file=sys.stderr,
        )
        return 1
    if text != text.strip():
        print("error: entry must not have leading or trailing whitespace", file=sys.stderr)
        return 1

    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "entry.txt"
    output_path.write_bytes(text.encode("utf-8"))
    # Round-trip check: what landed on disk must be byte-identical to the
    # validated text, so a stray newline or encoding slip can never pass.
    if output_path.read_bytes() != text.encode("utf-8"):
        print("error: entry.txt on disk does not match the validated text", file=sys.stderr)
        return 1
    print(f"wrote {len(text)} characters to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
