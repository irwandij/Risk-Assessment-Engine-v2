"""Curated form configuration for Risk Assessment web wizard."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional, get_args, get_origin

from pydantic import BaseModel

from ..models.ai_project_data import AIProjectData
from ..models.partner_data import PartnerData
from ..models.research_data import ResearchData
from ..models.vendor_data import VendorData

BASE_DIR = Path(__file__).resolve().parents[1]
TEMPLATES_DIR = BASE_DIR / "templates"

ASSESSMENT_TYPES = {"merchant", "partner", "vendor", "ai"}


SECTION_TITLES: Dict[str, Dict[str, str]] = {
    "merchant": {
        "merchant_info": "Merchant Profile",
        "parameter_a": "A. Company Identity",
        "parameter_b": "B. Regulatory & Licensing",
        "parameter_c": "C. Product Clarity",
        "parameter_d": "D. Payment Transparency",
        "parameter_e": "E. Terms & Conditions",
        "parameter_f": "F. Consumer Protection",
        "parameter_g": "G. Privacy & PDP",
        "parameter_h": "H. Security Indicators",
        "parameter_i": "I. Reputation & Footprint",
        "_meta": "Assessment Notes",
    },
    "partner": {
        "partner_info": "Partner Profile",
        "parameter_a": "A. Company Profile",
        "parameter_b": "B. Financial Stability",
        "parameter_c": "C. Strategic Alignment",
        "parameter_d": "D. Operational Capability",
        "parameter_e": "E. Regulatory Compliance",
        "parameter_f": "F. Reputation & Track Record",
        "parameter_g": "G. Data & Security",
        "parameter_h": "H. Contract & Governance",
        "_meta": "Assessment Notes",
    },
    "vendor": {
        "vendor_info": "Vendor Profile",
        "parameter_a": "A. Vendor Profile",
        "parameter_b": "B. Financial Health",
        "parameter_c": "C. Security & Compliance",
        "parameter_d": "D. Data Protection",
        "parameter_e": "E. Operational Capability",
        "parameter_f": "F. BCP/DRP Readiness",
        "parameter_g": "G. IT Infrastructure",
        "parameter_h": "H. Contract & SLA",
        "parameter_i": "I. References & Reputation",
        "_meta": "Assessment Notes",
    },
    "ai": {
        "project_info": "Project Profile",
        "section_a": "A. Privacy & PDP Compliance",
        "section_b": "B. Security",
        "section_c": "C. Business Value",
        "section_d": "D. Accountability",
        "section_e": "E. Reliability",
        "section_f": "F. Fairness",
        "section_g": "G. Transparency",
        "_meta": "Assessment Notes",
    },
}


SECTION_DESCRIPTIONS: Dict[str, Dict[str, str]] = {
    "merchant": {
        "merchant_info": "Basic business profile and payment model.",
        "parameter_b": "Critical gate for PJP/Aggregator licensing.",
        "_meta": "Analyst notes and assessment metadata.",
    },
    "partner": {
        "partner_info": "Legal, sector, and operating profile.",
        "parameter_e": "Regulatory posture and licensing validity.",
        "_meta": "Analyst notes and timestamp metadata.",
    },
    "vendor": {
        "vendor_info": "Vendor role, criticality, and geography.",
        "parameter_f": "Business continuity and disaster recovery readiness.",
        "_meta": "Analyst notes and timestamp metadata.",
    },
    "ai": {
        "project_info": "Project owner, scope, and external impact.",
        "section_a": "Hard-stop privacy control checks.",
        "section_b": "Hard-stop security control checks.",
        "section_c": "Hard-stop value justification checks.",
        "_meta": "Assessor notes and timestamp metadata.",
    },
}


LABEL_OVERRIDES: Dict[str, str] = {
    "merchant_info.name": "Merchant Name",
    "merchant_info.website": "Website URL",
    "merchant_info.business_type": "Business Type",
    "merchant_info.processes_payments_for_others": "Processes Payments for Other Merchants",
    "merchant_info.subscription_model": "Subscription Model for Autodebit",
    "parameter_b.bi_registry_checked": "BI Registry Checked",
    "parameter_b.bi_registry_found": "BI Registry Match Found",
    "parameter_i.app_store_rating": "App Store Rating",
    "parameter_i.review_count": "Review Count",
    "partner_info.name": "Partner Name",
    "vendor_info.name": "Vendor Name",
    "project_info.project_name": "AI Project Name",
    "project_info.project_owner": "Project Owner",
    "project_info.is_external_facing": "External Facing",
    "project_info.processes_personal_data": "Processes Personal Data",
}


HELP_OVERRIDES: Dict[str, str] = {
    "merchant_info.processes_payments_for_others": "Set to Yes when the merchant handles payments on behalf of other merchants.",
    "merchant_info.subscription_model": "Autodebit is intended for recurring/subscription-style payment models.",
    "parameter_b.bi_registry_checked": "Required for regulated payment activity verification.",
    "parameter_b.bi_registry_found": "Set to Yes only when an exact BI registry record is confirmed.",
    "parameter_i.negative_news": "Enter one item per line.",
    "parameter_i.positive_news": "Enter one item per line.",
    "project_info.processes_personal_data": "If Yes, privacy approval controls become critical.",
}


ASSESSMENT_DEFS: Dict[str, Dict[str, Any]] = {
    "merchant": {
        "title": "Merchant Risk Assessment",
        "description": "Assess merchant onboarding risk for recurring/autodebit use cases.",
        "max_score": 100,
        "template": "research_template.json",
        "model": ResearchData,
        "steps": [
            "merchant_info",
            "parameter_a",
            "parameter_b",
            "parameter_c",
            "parameter_d",
            "parameter_e",
            "parameter_f",
            "parameter_g",
            "parameter_h",
            "parameter_i",
            "_meta",
        ],
        "meta_fields": ["general_notes", "researcher", "research_date"],
    },
    "partner": {
        "title": "Partner Risk Assessment",
        "description": "Evaluate partnership risk across strategic, compliance, and operational controls.",
        "max_score": 100,
        "template": "partner_template.json",
        "model": PartnerData,
        "steps": [
            "partner_info",
            "parameter_a",
            "parameter_b",
            "parameter_c",
            "parameter_d",
            "parameter_e",
            "parameter_f",
            "parameter_g",
            "parameter_h",
            "_meta",
        ],
        "meta_fields": ["general_notes", "assessor", "assessment_date"],
    },
    "vendor": {
        "title": "Vendor Risk Assessment",
        "description": "Assess third-party vendor security, resilience, and contractual risk posture.",
        "max_score": 100,
        "template": "vendor_template.json",
        "model": VendorData,
        "steps": [
            "vendor_info",
            "parameter_a",
            "parameter_b",
            "parameter_c",
            "parameter_d",
            "parameter_e",
            "parameter_f",
            "parameter_g",
            "parameter_h",
            "parameter_i",
            "_meta",
        ],
        "meta_fields": ["general_notes", "assessor", "assessment_date"],
    },
    "ai": {
        "title": "AI Project Risk Assessment",
        "description": "Assess AI project readiness against governance, safety, and policy controls.",
        "max_score": 16,
        "template": "ai_project_template.json",
        "model": AIProjectData,
        "steps": [
            "project_info",
            "section_a",
            "section_b",
            "section_c",
            "section_d",
            "section_e",
            "section_f",
            "section_g",
            "_meta",
        ],
        "meta_fields": ["general_notes", "assessor", "assessment_date"],
    },
}


def _humanize(name: str) -> str:
    return name.replace("_", " ").strip().title()


def _unwrap_model(annotation: Any) -> Optional[type[BaseModel]]:
    origin = get_origin(annotation)
    if origin is None:
        if isinstance(annotation, type) and issubclass(annotation, BaseModel):
            return annotation
        return None
    for arg in get_args(annotation):
        if isinstance(arg, type) and issubclass(arg, BaseModel):
            return arg
    return None


def _unwrap_scalar_annotation(annotation: Any) -> Any:
    origin = get_origin(annotation)
    if origin is None:
        return annotation
    args = [arg for arg in get_args(annotation) if arg is not type(None)]
    if len(args) == 1:
        return args[0]
    return annotation


def _infer_field_type(path: str, sample: Any, annotation: Any) -> str:
    ann = _unwrap_scalar_annotation(annotation)
    origin = get_origin(ann)

    if ann is bool or isinstance(sample, bool):
        return "boolean"
    if ann in (int, float) or isinstance(sample, (int, float)):
        return "number"
    if origin in (list, List) or isinstance(sample, list):
        return "list_text"
    if isinstance(sample, str) and "date" in path.lower():
        return "date"
    if isinstance(sample, str) and ("notes" in path.lower() or len(sample) > 80):
        return "textarea"
    if ann is str or isinstance(sample, str) or sample is None:
        if "notes" in path.lower() or "description" in path.lower() or "explanation" in path.lower():
            return "textarea"
        return "text"
    return "text"


def _default_for_field(field_type: str, sample: Any) -> Any:
    if field_type == "boolean":
        return None
    if field_type == "number":
        return sample if isinstance(sample, (int, float)) else None
    if field_type == "list_text":
        return "\n".join(sample) if isinstance(sample, list) else ""
    if field_type == "date":
        return sample or ""
    if field_type in {"text", "textarea"}:
        return sample or ""
    return sample


def _build_section_fields(
    assessment_type: str,
    section_name: str,
    section_data: Dict[str, Any],
    section_model: Optional[type[BaseModel]],
) -> List[Dict[str, Any]]:
    fields: List[Dict[str, Any]] = []
    model_fields = section_model.model_fields if section_model else {}

    for name, sample in section_data.items():
        path = f"{section_name}.{name}" if section_name != "_meta" else name
        model_field = model_fields.get(name)
        annotation = model_field.annotation if model_field else type(sample)

        field_type = _infer_field_type(path, sample, annotation)
        required = model_field.is_required() if model_field else False

        number_mode = None
        ann = _unwrap_scalar_annotation(annotation)
        if ann is int:
            number_mode = "int"
        elif ann is float:
            number_mode = "float"

        fields.append(
            {
                "path": path,
                "name": name,
                "label": LABEL_OVERRIDES.get(path, _humanize(name)),
                "help": HELP_OVERRIDES.get(path, ""),
                "type": field_type,
                "required": required,
                "default": _default_for_field(field_type, sample),
                "number_mode": number_mode,
            }
        )

    return fields


@lru_cache(maxsize=None)
def get_form_config(assessment_type: str) -> Dict[str, Any]:
    if assessment_type not in ASSESSMENT_DEFS:
        raise KeyError(f"Unknown assessment type: {assessment_type}")

    definition = ASSESSMENT_DEFS[assessment_type]
    template_path = TEMPLATES_DIR / definition["template"]
    template_data = json.loads(template_path.read_text(encoding="utf-8"))

    meta_section: Dict[str, Any] = {}
    for key in definition["meta_fields"]:
        meta_section[key] = template_data.get(key)

    normalized_data = {k: v for k, v in template_data.items() if k not in definition["meta_fields"]}
    normalized_data["_meta"] = meta_section

    model_cls: type[BaseModel] = definition["model"]
    root_model_fields = model_cls.model_fields

    steps: List[Dict[str, Any]] = []
    for section_name in definition["steps"]:
        section_payload = normalized_data.get(section_name, {})
        if not isinstance(section_payload, dict):
            continue

        if section_name == "_meta":
            section_model = model_cls
        else:
            parent_field = root_model_fields.get(section_name)
            section_model = _unwrap_model(parent_field.annotation) if parent_field else None

        fields = _build_section_fields(
            assessment_type=assessment_type,
            section_name=section_name,
            section_data=section_payload,
            section_model=section_model,
        )

        steps.append(
            {
                "id": section_name,
                "title": SECTION_TITLES[assessment_type].get(section_name, _humanize(section_name)),
                "description": SECTION_DESCRIPTIONS.get(assessment_type, {}).get(section_name, ""),
                "fields": fields,
            }
        )

    return {
        "assessment_type": assessment_type,
        "title": definition["title"],
        "description": definition["description"],
        "max_score": definition["max_score"],
        "steps": steps,
    }


def list_assessment_types() -> List[Dict[str, Any]]:
    cards = []
    for key, definition in ASSESSMENT_DEFS.items():
        cards.append(
            {
                "id": key,
                "title": definition["title"],
                "description": definition["description"],
                "max_score": definition["max_score"],
                "step_count": len(definition["steps"]),
            }
        )
    return cards
