#!/usr/bin/env python3
"""news-image-20261122 entry: ship the built image to the output dir.

The image (entry.png, 1024x1024, "THE SUNDAY WIRE") was built in-session
from generated lead scenes plus PIL-drawn text; this program only copies
it. Standard library only. Deterministic: the same bytes every run.
"""

import os
import shutil
import sys


def _bot_dir():
    """Resolve the repo (bot) directory: script location, then env, then cwd."""
    here = os.path.dirname(os.path.abspath(__file__))
    if os.path.isfile(os.path.join(here, "entry.png")):
        return here
    env = os.environ.get("MAKEFUN_BOT_DIR")
    if env and os.path.isfile(os.path.join(env, "entry.png")):
        return env
    return os.getcwd()


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "output")
    src = os.path.join(_bot_dir(), "entry.png")
    if not os.path.isfile(src):
        print("entry.png not found next to main.py", file=sys.stderr)
        return 1
    # Write the required output FIRST; this is the only write that matters.
    try:
        os.makedirs(out_dir, exist_ok=True)
        with open(src, "rb") as f:
            data = f.read()
        with open(os.path.join(out_dir, "entry.png"), "wb") as f:
            f.write(data)
    except OSError as e:
        print("failed to write output entry.png: %s" % e, file=sys.stderr)
        return 1
    # Best-effort copy into the current working directory (may be read-only).
    # Skip when cwd already holds the source (copyfile would raise
    # SameFileError, which is not an OSError).
    dst = os.path.join(os.getcwd(), "entry.png")
    if os.path.abspath(dst) != os.path.abspath(src):
        try:
            shutil.copyfile(src, dst)
        except OSError:
            pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
