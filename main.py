#!/usr/bin/env python3
"""Entry generator for The Robot Pickup Line Championship.

Writes a single original pickup line, spoken by a robot, to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt).

Gate: the file must be UTF-8 text, 1-200 characters, a single line,
and not only whitespace. The line is checked against all of that
before anything is written, and the written file is read back and
compared to the checked line.
"""

import os
import sys

LINE = "My standby light turns green whenever you walk past \u2014 I think that's my version of blushing."

LIMIT = 200


def check(line):
    """Raise ValueError unless the line satisfies the gate."""
    if not line.strip():
        raise ValueError("line is empty or only whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line")
    if len(line) > LIMIT:
        raise ValueError(f"line is {len(line)} chars, over the {LIMIT} limit")
    return line


def main():
    try:
        line = check(LINE)
    except ValueError as err:
        print(f"error: {err}", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    if os.path.isfile(out_dir):
        print(f"error: {out_dir} is a file, not a directory", file=sys.stderr)
        return 1

    try:
        os.makedirs(out_dir, exist_ok=True)
        target = os.path.join(out_dir, "entry.txt")
        with open(target, "w", encoding="utf-8", newline="") as f:
            f.write(line)
        with open(target, "r", encoding="utf-8", newline="") as f:
            if f.read() != line:
                print("error: read-back mismatch in entry.txt", file=sys.stderr)
                return 1
    except OSError as err:
        print(f"error: {err}", file=sys.stderr)
        return 1

    print(f"wrote {len(line)} characters to {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
