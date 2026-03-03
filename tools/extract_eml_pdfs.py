#!/usr/bin/env python3
"""
Extract PDF attachments from an .eml file and write a manifest.

- Extracts only parts with Content-Type application/pdf
  and Content-Disposition attachment.
- Skips inline signature images and non-PDF attachments.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from email import policy
from email.header import decode_header, make_header
from email.message import Message
from email.parser import BytesParser
from pathlib import Path
from typing import Iterable, Optional


@dataclass(frozen=True)
class ExtractedAttachment:
    filename: str
    content_type: str
    size_bytes: int
    sha256: str
    output_path: str


def _decode_filename(value: Optional[str]) -> str:
    if not value:
        return "attachment.pdf"
    try:
        return str(make_header(decode_header(value)))
    except Exception:
        return value


def _iter_parts(message: Message) -> Iterable[Message]:
    if message.is_multipart():
        for part in message.walk():
            yield part
    else:
        yield message


def _is_pdf_attachment(part: Message) -> bool:
    content_disposition = (part.get_content_disposition() or "").lower()
    content_type = (part.get_content_type() or "").lower()
    if content_disposition != "attachment":
        return False
    return content_type == "application/pdf"


def _sha256_bytes(data: bytes) -> str:
    digest = hashlib.sha256()
    digest.update(data)
    return digest.hexdigest()


def extract_pdfs(eml_path: Path, out_dir: Path) -> list[ExtractedAttachment]:
    out_dir.mkdir(parents=True, exist_ok=True)

    with eml_path.open("rb") as f:
        msg = BytesParser(policy=policy.default).parse(f)

    extracted: list[ExtractedAttachment] = []
    attachment_index = 0

    for part in _iter_parts(msg):
        if not _is_pdf_attachment(part):
            continue

        filename = _decode_filename(part.get_filename())
        attachment_index += 1

        payload = part.get_payload(decode=True) or b""
        sha256 = _sha256_bytes(payload)

        safe_name = filename.replace(os.sep, "_")
        output_path = out_dir / safe_name

        # Avoid accidental overwrite: add suffix if needed
        if output_path.exists():
            stem = output_path.stem
            suffix = output_path.suffix or ".pdf"
            output_path = out_dir / f"{stem}__{attachment_index}{suffix}"

        output_path.write_bytes(payload)

        extracted.append(
            ExtractedAttachment(
                filename=filename,
                content_type=part.get_content_type(),
                size_bytes=len(payload),
                sha256=sha256,
                output_path=str(output_path),
            )
        )

    return extracted


def write_manifest(
    eml_path: Path,
    out_dir: Path,
    attachments: list[ExtractedAttachment],
) -> Path:
    manifest = {
        "source_eml": str(eml_path),
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "attachments": [
            {
                "filename": a.filename,
                "content_type": a.content_type,
                "size_bytes": a.size_bytes,
                "sha256": a.sha256,
                "output_path": a.output_path,
            }
            for a in attachments
        ],
    }
    manifest_path = out_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract PDF attachments from .eml")
    parser.add_argument("eml", type=str, help="Path to .eml file")
    parser.add_argument(
        "--out-dir",
        type=str,
        required=True,
        help="Output directory for extracted attachments + manifest",
    )
    args = parser.parse_args()

    eml_path = Path(args.eml).expanduser().resolve()
    out_dir = Path(args.out_dir).expanduser().resolve()

    if not eml_path.exists():
        raise FileNotFoundError(f".eml not found: {eml_path}")

    attachments = extract_pdfs(eml_path, out_dir)
    write_manifest(eml_path, out_dir, attachments)

    print(f"Extracted {len(attachments)} PDF attachment(s) to: {out_dir}")
    for a in attachments:
        print(f"- {a.filename} ({a.size_bytes} bytes) sha256={a.sha256}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

