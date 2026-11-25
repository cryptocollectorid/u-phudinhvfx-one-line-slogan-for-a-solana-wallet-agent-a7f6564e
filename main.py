#!/usr/bin/env python3
"""One-Line Slogan for a Solana Wallet Agent.

Writes a single slogan (at most 20 words, 1-140 chars, one line) to
/output/entry.txt, enforcing the sealed gate from competition.yaml.
"""

import os
import sys

SLOGAN = "Your Solana wallet, with a brain \u2014 one tap, and it signs, swaps, and gets out of your way."

MAX_CHARS = 140
MAX_WORDS = 20


def validate_entry(text: str) -> None:
    if not isinstance(text, str) or not text.strip():
        raise ValueError("entry must be non-blank text")
    if any(ord(ch) < 32 for ch in text):
        raise ValueError("entry must not contain control characters")
    if len(text) > MAX_CHARS:
        raise ValueError(f"entry is {len(text)} chars, max {MAX_CHARS}")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    words = text.split()
    if len(words) > MAX_WORDS:
        raise ValueError(f"entry is {len(words)} words, max {MAX_WORDS}")


def write_entry(text: str, path: str = "/output/entry.txt") -> None:
    validate_entry(text)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    # Round-trip read-back: the file on disk must hold exactly the entry.
    with open(path, "r", encoding="utf-8") as f:
        back = f.read()
    if back != text:
        raise ValueError("round-trip verify failed: file differs from entry")
    print(f"Wrote {len(text)} characters to {path}")


if __name__ == "__main__":
    try:
        write_entry(SLOGAN)
    except ValueError as exc:
        print(f"gate failed: {exc}", file=sys.stderr)
        sys.exit(1)
