#!/usr/bin/env python3
from pathlib import Path
from tools.caselinker_icac_remodel import build_and_write

HERE = Path(__file__).resolve().parent
if __name__ == "__main__":
    build_and_write("legalproc-dual-type", HERE / "legalproc-dual-type.jsonld")
