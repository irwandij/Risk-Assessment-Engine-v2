"""FastAPI web interface for Risk Assessment Engine."""

from __future__ import annotations

import uuid
from pathlib import Path
from typing import Any, Callable, Dict, Type

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, ValidationError

from ..engine.ai_assessor import AIAssessor
from ..engine.assessor import Assessor
from ..engine.partner_assessor import PartnerAssessor
from ..engine.vendor_assessor import VendorAssessor
from ..generators.report_generator import ReportGenerator
from ..models.ai_project_data import AIProjectData
from ..models.partner_data import PartnerData
from ..models.research_data import ResearchData
from ..models.vendor_data import VendorData
from .form_config import ASSESSMENT_TYPES, get_form_config, list_assessment_types
from .serializers import normalize_validation_errors, serialize_result_payload

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="Risk Assessment Web",
    description="Local wizard UI for merchant, partner, vendor, and AI assessments.",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


ASSESSMENT_SPEC: Dict[str, Dict[str, Any]] = {
    "merchant": {
        "model": ResearchData,
        "assessor_factory": Assessor,
    },
    "partner": {
        "model": PartnerData,
        "assessor_factory": PartnerAssessor,
    },
    "vendor": {
        "model": VendorData,
        "assessor_factory": VendorAssessor,
    },
    "ai": {
        "model": AIProjectData,
        "assessor_factory": AIAssessor,
    },
}


@app.get("/", response_class=HTMLResponse)
def landing_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "assessment_cards": list_assessment_types(),
            "app_title": "Risk Assessment Studio",
        },
    )


@app.get("/api/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.get("/api/form-config/{assessment_type}")
def form_config(assessment_type: str) -> Dict[str, Any]:
    if assessment_type not in ASSESSMENT_TYPES:
        raise HTTPException(status_code=404, detail=f"Unsupported assessment type: {assessment_type}")

    try:
        return get_form_config(assessment_type)
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Unsupported assessment type: {assessment_type}")


@app.post("/api/assess/{assessment_type}")
async def assess(assessment_type: str, payload: Dict[str, Any]) -> JSONResponse:
    if assessment_type not in ASSESSMENT_SPEC:
        raise HTTPException(status_code=404, detail=f"Unsupported assessment type: {assessment_type}")

    spec = ASSESSMENT_SPEC[assessment_type]
    model_cls: Type[BaseModel] = spec["model"]
    assessor_factory: Callable[[], Any] = spec["assessor_factory"]

    try:
        model_instance = model_cls(**payload)
        assessor = assessor_factory()
        result = assessor.assess(model_instance)
        report = ReportGenerator().generate(result)
        return JSONResponse(status_code=200, content=serialize_result_payload(result, report, assessment_type))
    except ValidationError as exc:
        return JSONResponse(
            status_code=422,
            content={
                "error": "validation_error",
                "message": "Input validation failed",
                "details": normalize_validation_errors(exc),
            },
        )
    except HTTPException:
        raise
    except Exception:
        trace_id = str(uuid.uuid4())
        return JSONResponse(
            status_code=500,
            content={
                "error": "internal_error",
                "message": "Unexpected error while running assessment",
                "trace_id": trace_id,
            },
        )
