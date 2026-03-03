"""Serialization and normalization helpers for web API responses."""

from __future__ import annotations

import re
from datetime import datetime
from typing import Any, Dict, List

from pydantic import ValidationError


def normalize_validation_errors(exc: ValidationError) -> List[Dict[str, str]]:
    """Convert Pydantic validation errors to frontend-friendly structure."""
    normalized: List[Dict[str, str]] = []
    for err in exc.errors():
        loc = [str(part) for part in err.get("loc", []) if part != "body"]
        path = ".".join(loc)
        normalized.append(
            {
                "path": path,
                "message": err.get("msg", "Invalid value"),
                "type": err.get("type", "validation_error"),
            }
        )
    return normalized


def slugify(value: str) -> str:
    sanitized = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower())
    sanitized = re.sub(r"-{2,}", "-", sanitized).strip("-")
    return sanitized or "assessment"


def build_download_filenames(name: str, assessment_type: str) -> Dict[str, str]:
    base = slugify(name)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return {
        "json_filename": f"{base}-{assessment_type}-result-{stamp}.json",
        "markdown_filename": f"{base}-{assessment_type}-report-{stamp}.md",
    }


def serialize_result_payload(result: Any, report_markdown: str, assessment_type: str) -> Dict[str, Any]:
    result_dict = result.model_dump(mode="json")
    files = build_download_filenames(result_dict.get("merchant_name", "assessment"), assessment_type)
    return {
        "result": result_dict,
        "report_markdown": report_markdown,
        "download": files,
    }
