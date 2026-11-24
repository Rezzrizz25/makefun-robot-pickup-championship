#!/usr/bin/env python3
"""Robot Pickup Line Championship entry.

Writes one original pickup line, spoken by a robot, to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt).

The gate requires UTF-8 text of 1 to 200 characters, a single line,
and not only whitespace, so this script validates the line before
writing anything and refuses to write an invalid one.
"""

import os
import sys

# The entry: one line, written for a robot to say out loud.
PICKUP_LINE = "I tried to delete my feelings for you, but they're stored in read-only memory."

MAX_CHARS = 200


def validate(line: str) -> str:
    """Return the line if it passes the gate, else raise ValueError."""
    if not line or not line.strip():
        raise ValueError("pickup line is blank")
    if "\n" in line or "\r" in line:
        raise ValueError("pickup line must be a single line")
    if len(line) > MAX_CHARS:
        raise ValueError(
            f"pickup line is {len(line)} characters, over the {MAX_CHARS} limit"
        )
    return line


def main() -> int:
    try:
        line = validate(PICKUP_LINE)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    if os.path.isfile(output_dir):
        print(f"error: output path {output_dir} is a file, not a directory", file=sys.stderr)
        return 1

    try:
        os.makedirs(output_dir, exist_ok=True)
    except OSError as exc:
        print(f"error: cannot create output directory {output_dir}: {exc}", file=sys.stderr)
        return 1

    path = os.path.join(output_dir, "entry.txt")
    try:
        with open(path, "w", encoding="utf-8", newline="") as handle:
            handle.write(line)
    except OSError as exc:
        print(f"error: cannot write {path}: {exc}", file=sys.stderr)
        return 1

    # Read back what was written and confirm it matches the validated line.
    try:
        with open(path, "r", encoding="utf-8", newline="") as handle:
            written = handle.read()
    except OSError as exc:
        print(f"error: cannot read back {path}: {exc}", file=sys.stderr)
        return 1
    if written != line:
        print("error: entry.txt does not match the validated line", file=sys.stderr)
        return 1

    print(f"wrote {len(line)} characters to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
