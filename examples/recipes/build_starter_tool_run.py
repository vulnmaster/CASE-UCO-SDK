#!/usr/bin/env python3
from pathlib import Path
from tools.recipe_catalog_builders import build_and_write

HERE = Path(__file__).resolve().parent
if __name__ == "__main__":
    build_and_write('starter-tool-run', HERE / 'starter-tool-run.jsonld')
