"""Start local web server for Risk Assessment Studio."""

from __future__ import annotations

import sys
from pathlib import Path

import uvicorn

ROOT_DIR = Path(__file__).resolve().parent
PARENT_DIR = ROOT_DIR.parent
if str(PARENT_DIR) not in sys.path:
    sys.path.insert(0, str(PARENT_DIR))

from risk_assessment_engine.web.app import app


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8080,
        reload=False,
    )
