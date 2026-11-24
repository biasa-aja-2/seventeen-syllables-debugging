#!/usr/bin/env python3
"""Seventeen Syllables of Debugging -- round 3.

Writes one haiku about debugging to /output/entry.txt.

The haiku (5-7-5):

    The stack trace ends here
    I add one print and watch it
    lie to me again

Why this one: the centre image is concrete and fresh -- a stack trace
that stops dead, and the oldest debugging move there is, one print
statement added by hand. The last line turns the poem: the print was
meant to catch the lie, and instead the code lies again, so the
debugger is the one being played. Every word earns its place; it
reads aloud like speech, not a syllable exercise.

Pure standard library. Deterministic: the same seventeen syllables on
every run. Before writing, the program checks its own work with a
small syllable counter and refuses to write anything that is not
5-7-5 and within the 200-character gate.
"""

import os
import re
import sys

HAIKU = (
    "The stack trace ends here",
    "I add one print and watch it",
    "lie to me again",
)

EXPECTED_SYLLABLES = (5, 7, 5)
MAX_CHARS = 200
OUTPUT_PATH = "/output/entry.txt"

# Syllable counts for every word the haiku uses, pinned by hand so the
# self-check is exact rather than heuristic. A generic fallback below
# covers any word not listed.
SYLLABLES = {
    "the": 1,
    "stack": 1,
    "trace": 1,
    "ends": 1,
    "here": 1,
    "i": 1,
    "add": 1,
    "one": 1,
    "print": 1,
    "and": 1,
    "watch": 1,
    "it": 1,
    "lie": 1,
    "to": 1,
    "me": 1,
    "again": 2,
}

VOWELS = "aeiouy"


def count_syllables(word):
    """Count the syllables of one word.

    Exact for the haiku's own words (see SYLLABLES); otherwise a
    vowel-group heuristic with a silent-e correction, good enough as a
    safety net for words the haiku does not use.
    """
    clean = re.sub(r"[^a-z]", "", word.lower())
    if not clean:
        return 0
    if clean in SYLLABLES:
        return SYLLABLES[clean]
    groups = re.findall(r"[aeiouy]+", clean)
    count = len(groups)
    if clean.endswith("e") and count > 1:
        count -= 1
    return max(count, 1)


def line_syllables(line):
    return sum(count_syllables(word) for word in line.split())


def build_text():
    text = "\n".join(HAIKU)
    counts = tuple(line_syllables(line) for line in HAIKU)
    if counts != EXPECTED_SYLLABLES:
        raise SystemExit(
            "haiku is not 5-7-5: got %s, expected %s" % (counts, EXPECTED_SYLLABLES)
        )
    if not 1 <= len(text) <= MAX_CHARS:
        raise SystemExit(
            "haiku is %d characters, outside the 1-%d gate" % (len(text), MAX_CHARS)
        )
    if not text.strip():
        raise SystemExit("haiku is blank")
    return text


def main():
    text = build_text()
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
    # Read it back: never report success for a write that did not land.
    with open(OUTPUT_PATH, encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != text:
        raise SystemExit("read-back mismatch in %s" % OUTPUT_PATH)
    print("wrote %s (%d characters, syllables %s)" % (OUTPUT_PATH, len(text), EXPECTED_SYLLABLES))
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
