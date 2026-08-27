#!/usr/bin/env python3
from pathlib import Path
from tools.press_release_legal import build_and_write

HERE = Path(__file__).resolve().parent
if __name__ == "__main__":
    build_and_write("state-plea-sentence", HERE / "state-plea-sentence.jsonld")
