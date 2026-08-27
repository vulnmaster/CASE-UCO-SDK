#!/usr/bin/env python3
from pathlib import Path
from tools.recipe_catalog_builders import build_and_write

HERE = Path(__file__).resolve().parent
if __name__ == "__main__":
    build_and_write('cargo-theft-route-staging', HERE / 'cargo-theft-route-staging.jsonld')
