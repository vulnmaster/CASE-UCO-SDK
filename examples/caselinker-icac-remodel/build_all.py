#!/usr/bin/env python3
from pathlib import Path
from tools.caselinker_icac_remodel import SCENARIOS, build_and_write

HERE = Path(__file__).resolve().parent
if __name__ == "__main__":
    import sys
    names = sys.argv[1:] or list(SCENARIOS)
    for name in names:
        path = HERE / f"{name}.jsonld"
        build_and_write(name, path)
        print(path)
