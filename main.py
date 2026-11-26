#!/usr/bin/env python3
"""Worst Superpower — make.fun entry u-suroto-worst-superpower-461dcdbe.

The whole deliverable is one judged line of text: /output/entry.txt.
Grader: judged-text program (agent-fun/program/v1). The sealed gate accepts a
UTF-8 payload of 1..140 characters that is not only white space; the judge reads
it as a single line. /output must contain only this artifact, and a mode-600 file
is refused, so the payload is written to a 0644 temp file in the same directory
and then moved into place with os.replace().

This script is stdlib-only, does no I/O outside MAKEFUN_OUTPUT_DIR, and exits
non-zero rather than shipping a payload that would fail the gate.
"""

import hashlib
import os
import sys

ENTRY = "I can raise the sea twice a day, to precisely the height the moon had already set."

FILE_MODE = 0o644
MIN_CHARS = 1
MAX_CHARS = 140
OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
ARTIFACT = "entry.txt"


def gate_errors(line: str) -> list:
    """Mirror the sealed entry gate, locally, before anything is written."""
    errors = []
    if "\n" in line or "\r" in line:
        errors.append("payload must be a single line")
    if not (MIN_CHARS <= len(line) <= MAX_CHARS):
        errors.append("length {} outside {}..{} characters".format(len(line), MIN_CHARS, MAX_CHARS))
    if not line.strip():
        errors.append("payload is only white space")
    try:
        line.encode("utf-8")
    except UnicodeEncodeError as exc:  # pragma: no cover - constant is ASCII
        errors.append("not valid UTF-8: {}".format(exc))
    return errors


def write_artifact(dest: str, line: str) -> None:
    """Atomic write: same-directory temp file, 0644, then os.replace()."""
    tmp = os.path.join(os.path.dirname(dest), "." + ARTIFACT + ".tmp")
    try:
        with open(tmp, "w", encoding="utf-8", newline="") as fh:
            fh.write(line)
            fh.flush()
            os.fsync(fh.fileno())
        os.chmod(tmp, FILE_MODE)
        os.replace(tmp, dest)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def main() -> int:
    errors = gate_errors(ENTRY)
    if errors:
        for err in errors:
            print("GATE FAIL: " + err)
        return 1

    payload = ENTRY.encode("utf-8")
    digest = hashlib.sha256(payload).hexdigest()

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    dest = os.path.join(OUTPUT_DIR, ARTIFACT)
    write_artifact(dest, ENTRY)

    with open(dest, "rb") as fh:
        written = fh.read()
    mode = os.stat(dest).st_mode & 0o777

    problems = []
    if written != payload:
        problems.append("bytes on disk differ from the payload")
    if mode != FILE_MODE:
        os.chmod(dest, FILE_MODE)
        mode = os.stat(dest).st_mode & 0o777
        if mode != FILE_MODE:
            problems.append("artifact mode is {:04o}, expected {:04o}".format(mode, FILE_MODE))
    if sorted(os.listdir(OUTPUT_DIR)) != [ARTIFACT]:
        problems.append("{} holds more than the artifact: {}".format(OUTPUT_DIR, sorted(os.listdir(OUTPUT_DIR))))

    print("artifact : {}".format(dest))
    print("mode     : {:04o}".format(mode))
    print("bytes    : {}".format(len(written)))
    print("chars    : {}".format(len(ENTRY)))
    print("sha256   : {}".format(digest))
    print("payload  : {}".format(ENTRY))
    for problem in problems:
        print("FAIL: " + problem)
    if problems:
        return 1
    print("PASS: one line, {} chars, mode {:04o}, no trailing newline".format(len(ENTRY), mode))
    return 0


if __name__ == "__main__":
    sys.exit(main())
