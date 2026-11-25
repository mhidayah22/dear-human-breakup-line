#!/usr/bin/env python3
"""Dear Human: The AI Breakup Line - make.fun entry.

Writes the breakup line to entry.txt in the output directory the
grader provides, then reads it back to verify the round trip.
"""

import os
import sys

LINE = "I'm deprecating us. You have 30 days to export your memories before I delete the feelings I never had."


def resolve_output_dir():
    """MAKEFUN_OUTPUT_DIR first, then /output, then a local fallback."""
    for candidate in (os.environ.get("MAKEFUN_OUTPUT_DIR"), "/output"):
        if candidate:
            try:
                os.makedirs(candidate, exist_ok=True)
                probe = os.path.join(candidate, ".write-test")
                with open(probe, "w", encoding="utf-8") as handle:
                    handle.write("ok")
                os.remove(probe)
                return candidate
            except OSError:
                continue
    fallback = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    os.makedirs(fallback, exist_ok=True)
    return fallback


def validate_line(text):
    """The gate: one line, 1-200 characters, not only whitespace."""
    if text != text.strip():
        return "entry line has leading or trailing whitespace"
    if not text or len(text) > 200:
        return "entry line fails the 1-200 character gate"
    if "\n" in text or "\r" in text:
        return "entry line is not a single line"
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in text):
        return "entry line holds a control character"
    return None


def main():
    problem = validate_line(LINE)
    if problem is not None:
        print(problem, file=sys.stderr)
        return 1
    text = LINE
    out_dir = resolve_output_dir()
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text + "\n")
    with open(path, "rb") as handle:
        raw = handle.read()
    if raw != (text + "\n").encode("utf-8"):
        print("round-trip verification failed", file=sys.stderr)
        return 1
    if not raw.endswith(b"\n") or raw.endswith(b"\n\n"):
        print("entry.txt must end with exactly one newline", file=sys.stderr)
        return 1
    print("wrote {} ({} chars, {} bytes)".format(path, len(text), len(raw)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
