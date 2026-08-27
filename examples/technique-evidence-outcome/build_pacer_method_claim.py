#!/usr/bin/env python3
from pathlib import Path
from tools.technique_evidence_outcome import build_and_write

HERE = Path(__file__).resolve().parent
if __name__ == "__main__":
    build_and_write("pacer-method-claim", HERE / "pacer-method-claim.jsonld")
