#!/usr/bin/env python3
"""
Risk Assessment Engine - CLI Entry Point

Usage:
    # Merchant Assessment (existing)
    python -m risk_assessment_engine assess research_data.json --output result.json --report report.md
    python -m risk_assessment_engine validate research_data.json

    # Partner Assessment (new)
    python -m risk_assessment_engine assess-partner partner_data.json --output result.json --report report.md

    # Vendor Assessment (new)
    python -m risk_assessment_engine assess-vendor vendor_data.json --output result.json --report report.md

    # AI Project Assessment (new)
    python -m risk_assessment_engine assess-ai ai_data.json --output result.json --report report.md

    # Generate sample templates
    python -m risk_assessment_engine sample --type merchant
    python -m risk_assessment_engine sample --type partner
    python -m risk_assessment_engine sample --type vendor
    python -m risk_assessment_engine sample --type ai
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional, Dict, Any

from .models.research_data import ResearchData
from .models.partner_data import PartnerData
from .models.vendor_data import VendorData
from .models.ai_project_data import AIProjectData
from .models.assessment_result import AssessmentResult
from .engine.assessor import Assessor
from .engine.partner_assessor import PartnerAssessor
from .engine.vendor_assessor import VendorAssessor
from .engine.ai_assessor import AIAssessor
from .generators.report_generator import ReportGenerator


def load_json_data(filepath: str) -> Dict[str, Any]:
    """Load JSON data from file."""
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {filepath}")

    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_research_data(filepath: str) -> ResearchData:
    """Load research data from JSON file."""
    data = load_json_data(filepath)
    return ResearchData(**data)


def load_partner_data(filepath: str) -> PartnerData:
    """Load partner data from JSON file."""
    data = load_json_data(filepath)
    return PartnerData(**data)


def load_vendor_data(filepath: str) -> VendorData:
    """Load vendor data from JSON file."""
    data = load_json_data(filepath)
    return VendorData(**data)


def load_ai_project_data(filepath: str) -> AIProjectData:
    """Load AI project data from JSON file."""
    data = load_json_data(filepath)
    return AIProjectData(**data)


def save_json(data: dict, filepath: str) -> None:
    """Save data to JSON file."""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, default=str)


def save_markdown(content: str, filepath: str) -> None:
    """Save markdown content to file."""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


def print_assessment_result(result: AssessmentResult, assessment_type: str = "merchant") -> None:
    """Print assessment result summary."""
    print(f"\n{'='*50}")
    print(f"ASSESSMENT COMPLETE")
    print(f"{'='*50}")
    print(f"Name: {result.merchant_name}")
    print(f"Type: {result.classification.get('assessment_type_display', assessment_type)}")
    print(f"Score: {result.total_score}/100")
    print(f"Risk Level: {result.risk_level.value}")
    print(f"Decision: {result.decision.value}")

    if result.decision_result.is_auto_rejected:
        print("\nAuto-Reject Triggers:")
        for trigger in result.decision_result.auto_reject_triggers:
            print(f"  - {trigger.code}: {trigger.reason}")


def cmd_assess(args: argparse.Namespace) -> int:
    """Run merchant assessment command."""
    try:
        print(f"Loading research data from: {args.input}")
        research_data = load_research_data(args.input)
        print(f"  Merchant: {research_data.merchant_info.name}")

        print("\nRunning assessment...")
        assessor = Assessor()
        result = assessor.assess(research_data)

        print_assessment_result(result, "merchant")

        if args.output:
            print(f"\nSaving result to: {args.output}")
            save_json(result.model_dump(), args.output)

        if args.report:
            print(f"Generating report: {args.report}")
            generator = ReportGenerator()
            report = generator.generate(result)
            save_markdown(report, args.report)

        print("\nDone!")
        return 0

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error during assessment: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


def cmd_assess_partner(args: argparse.Namespace) -> int:
    """Run partner assessment command."""
    try:
        print(f"Loading partner data from: {args.input}")
        partner_data = load_partner_data(args.input)
        print(f"  Partner: {partner_data.partner_info.name}")

        print("\nRunning partner assessment...")
        assessor = PartnerAssessor()
        result = assessor.assess(partner_data)

        print_assessment_result(result, "partner")

        if args.output:
            print(f"\nSaving result to: {args.output}")
            save_json(result.model_dump(), args.output)

        if args.report:
            print(f"Generating report: {args.report}")
            generator = ReportGenerator()
            report = generator.generate(result)
            save_markdown(report, args.report)

        print("\nDone!")
        return 0

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error during assessment: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


def cmd_assess_vendor(args: argparse.Namespace) -> int:
    """Run vendor assessment command."""
    try:
        print(f"Loading vendor data from: {args.input}")
        vendor_data = load_vendor_data(args.input)
        print(f"  Vendor: {vendor_data.vendor_info.name}")

        print("\nRunning vendor assessment...")
        assessor = VendorAssessor()
        result = assessor.assess(vendor_data)

        print_assessment_result(result, "vendor")

        if args.output:
            print(f"\nSaving result to: {args.output}")
            save_json(result.model_dump(), args.output)

        if args.report:
            print(f"Generating report: {args.report}")
            generator = ReportGenerator()
            report = generator.generate(result)
            save_markdown(report, args.report)

        print("\nDone!")
        return 0

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error during assessment: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


def cmd_assess_ai(args: argparse.Namespace) -> int:
    """Run AI project assessment command."""
    try:
        print(f"Loading AI project data from: {args.input}")
        ai_data = load_ai_project_data(args.input)
        print(f"  Project: {ai_data.project_info.project_name}")
        print(f"  Owner: {ai_data.project_info.project_owner}")

        print("\nRunning AI project assessment...")
        assessor = AIAssessor()
        result = assessor.assess(ai_data)

        print_assessment_result(result, "ai_project")

        if args.output:
            print(f"\nSaving result to: {args.output}")
            save_json(result.model_dump(), args.output)

        if args.report:
            print(f"Generating report: {args.report}")
            generator = ReportGenerator()
            report = generator.generate(result)
            save_markdown(report, args.report)

        print("\nDone!")
        return 0

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error during assessment: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


def cmd_validate(args: argparse.Namespace) -> int:
    """Validate research data file."""
    try:
        print(f"Validating: {args.input}")
        research_data = load_research_data(args.input)

        print("\nValidation PASSED")
        print(f"  Merchant: {research_data.merchant_info.name}")
        print(f"  Website: {research_data.merchant_info.website or 'N/A'}")
        print(f"  Business Type: {research_data.merchant_info.business_type}")
        print(f"  Is PJP/Aggregator: {research_data.is_pjp}")

        return 0

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Validation FAILED: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


def cmd_validate_partner(args: argparse.Namespace) -> int:
    """Validate partner data file."""
    try:
        print(f"Validating partner data: {args.input}")
        partner_data = load_partner_data(args.input)

        print("\nValidation PASSED")
        print(f"  Partner: {partner_data.partner_info.name}")
        print(f"  Website: {partner_data.partner_info.website or 'N/A'}")
        print(f"  Partnership Type: {partner_data.partner_info.partnership_type}")
        print(f"  Country: {partner_data.partner_info.country_of_incorporation}")

        return 0

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Validation FAILED: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


def cmd_validate_vendor(args: argparse.Namespace) -> int:
    """Validate vendor data file."""
    try:
        print(f"Validating vendor data: {args.input}")
        vendor_data = load_vendor_data(args.input)

        print("\nValidation PASSED")
        print(f"  Vendor: {vendor_data.vendor_info.name}")
        print(f"  Website: {vendor_data.vendor_info.website or 'N/A'}")
        print(f"  Vendor Type: {vendor_data.vendor_info.vendor_type}")
        print(f"  Criticality: {vendor_data.vendor_info.service_criticality}")

        return 0

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Validation FAILED: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


def cmd_validate_ai(args: argparse.Namespace) -> int:
    """Validate AI project data file."""
    try:
        print(f"Validating AI project data: {args.input}")
        ai_data = load_ai_project_data(args.input)

        print("\nValidation PASSED")
        print(f"  Project: {ai_data.project_info.project_name}")
        print(f"  Owner: {ai_data.project_info.project_owner}")
        print(f"  Expected Launch: {ai_data.project_info.expected_launch or 'N/A'}")

        return 0

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Validation FAILED: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


def cmd_sample(args: argparse.Namespace) -> int:
    """Generate sample data file."""
    sample_type = args.type.lower()

    if sample_type == "merchant":
        sample = _get_merchant_sample()
        output_path = args.output or "sample_research_data.json"
    elif sample_type == "partner":
        sample = _get_partner_sample()
        output_path = args.output or "sample_partner_data.json"
    elif sample_type == "vendor":
        sample = _get_vendor_sample()
        output_path = args.output or "sample_vendor_data.json"
    elif sample_type in ["ai", "ai_project"]:
        sample = _get_ai_sample()
        output_path = args.output or "sample_ai_project_data.json"
    else:
        print(f"Unknown sample type: {sample_type}", file=sys.stderr)
        print("Valid types: merchant, partner, vendor, ai")
        return 1

    print(f"Generating sample file: {output_path}")
    save_json(sample, output_path)
    print("Done!")
    return 0


def _get_merchant_sample() -> Dict[str, Any]:
    """Get merchant sample data."""
    return {
        "merchant_info": {
            "name": "PT Sample Merchant",
            "website": "https://example.com",
            "business_type": "subscription service",
            "legal_entity_name": "PT Sample Merchant Indonesia",
            "registration_number": "AHU-12345",
            "address": "Jl. Sudirman No. 1, Jakarta",
            "processes_payments_for_others": False,
            "claimed_bi_license": None,
            "bi_license_number": None,
            "subscription_model": True
        },
        "parameter_a": {
            "has_legal_entity": True,
            "legal_entity_type": "PT",
            "has_address": True,
            "address_verified": True,
            "has_phone": True,
            "has_email": True,
            "has_contact_form": True,
            "info_consistent": True,
            "linkedin_verified": True,
            "google_maps_verified": True,
            "notes": ""
        },
        "parameter_b": {
            "is_pjp_or_aggregator": False,
            "bi_license_verified": False,
            "bi_license_number": None,
            "license_scope_matches": None,
            "ojk_registered": False,
            "pse_registered": True,
            "notes": "Regular merchant - no BI license required"
        },
        "parameter_c": {
            "services_clearly_described": True,
            "has_scope_documentation": True,
            "has_deliverables": True,
            "has_limitations": True,
            "no_misleading_claims": True,
            "notes": ""
        },
        "parameter_d": {
            "has_fee_disclosure": True,
            "has_billing_cycle": True,
            "has_settlement_info": True,
            "has_refund_policy": True,
            "has_dispute_process": True,
            "has_sla": False,
            "pricing_clear": True,
            "notes": ""
        },
        "parameter_e": {
            "has_terms_page": True,
            "has_cancellation_policy": True,
            "has_refund_policy": True,
            "has_dispute_clause": True,
            "has_jurisdiction_clause": True,
            "has_fee_schedule": True,
            "tc_accessible": True,
            "tc_current": True,
            "notes": ""
        },
        "parameter_f": {
            "has_email_support": True,
            "has_phone_support": True,
            "has_chat_support": True,
            "has_faq": True,
            "has_escalation_path": True,
            "has_sla": True,
            "response_time_hours": 24,
            "notes": ""
        },
        "parameter_g": {
            "has_privacy_policy": True,
            "privacy_policy_url": "https://example.com/privacy",
            "has_data_retention_policy": True,
            "has_user_rights_section": True,
            "has_dpo_contact": True,
            "pdp_compliant": True,
            "policy_date": "2024-01-15",
            "notes": ""
        },
        "parameter_h": {
            "has_https": True,
            "website_stable": True,
            "has_secure_login": True,
            "ssl_valid": True,
            "phishing_indicators": False,
            "malware_detected": False,
            "notes": ""
        },
        "parameter_i": {
            "has_social_media": True,
            "has_linkedin": True,
            "has_google_maps": True,
            "has_press_coverage": True,
            "app_store_rating": 4.5,
            "review_count": 1500,
            "negative_news": [],
            "positive_news": ["Featured in Tech in Asia"],
            "scam_allegations": False,
            "regulatory_enforcement": False,
            "notes": ""
        },
        "general_notes": "Sample merchant for testing purposes",
        "researcher": "Risk Assessment Engine",
        "research_date": "2026-02-21T12:00:00"
    }


def _get_partner_sample() -> Dict[str, Any]:
    """Get partner sample data."""
    return {
        "partner_info": {
            "name": "PT Sample Partner",
            "website": "https://partner-example.com",
            "partnership_type": "strategic alliance",
            "legal_entity_name": "PT Sample Partner Indonesia",
            "registration_number": "AHU-54321",
            "country_of_incorporation": "Indonesia",
            "address": "Jl. Thamrin No. 10, Jakarta",
            "industry_sector": "Financial Technology",
            "years_in_business": 5
        },
        "parameter_a": {
            "has_legal_entity": True,
            "legal_entity_type": "PT",
            "registration_verified": True,
            "has_address": True,
            "ownership_structure_clear": True,
            "beneficial_owners_identified": True,
            "politically_exposed": False,
            "subsidiaries_listed": True,
            "notes": ""
        },
        "parameter_b": {
            "financial_statements_available": True,
            "audited_financials": True,
            "revenue_trend_positive": True,
            "profitability_trend_positive": True,
            "debt_to_equity_healthy": True,
            "current_ratio_healthy": True,
            "has_credit_rating": True,
            "credit_rating_value": "A",
            "insurance_coverage_adequate": True,
            "notes": ""
        },
        "parameter_c": {
            "business_model_aligned": True,
            "shared_objectives": True,
            "complementary_capabilities": True,
            "market_position_aligned": True,
            "cultural_fit": True,
            "long_term_commitment": True,
            "partnership_value_proposition": True,
            "notes": ""
        },
        "parameter_d": {
            "has_track_record": True,
            "years_of_experience": 10,
            "has_expertise": True,
            "management_team_qualified": True,
            "has_adequate_resources": True,
            "operational_processes_documented": True,
            "quality_certifications": True,
            "project_management_capability": True,
            "innovation_capability": True,
            "notes": ""
        },
        "parameter_e": {
            "has_required_licenses": True,
            "licenses_verified": True,
            "license_expiry_date": "2026-12-31",
            "no_regulatory_issues": True,
            "compliance_program_exists": True,
            "aml_kyc_compliant": True,
            "sanctions_screened": True,
            "no_legal_issues": True,
            "regulatory_stand": "Good standing",
            "notes": ""
        },
        "parameter_f": {
            "has_market_reputation": True,
            "references_available": True,
            "reference_check_positive": True,
            "has_industry_recognition": True,
            "media_coverage_positive": True,
            "no_negative_news": True,
            "no_past_issues": True,
            "esg_rating_positive": True,
            "notes": ""
        },
        "parameter_g": {
            "has_data_protection_policy": True,
            "has_security_certifications": True,
            "data_handling_documented": True,
            "encryption_standards": True,
            "access_controls": True,
            "incident_response_plan": True,
            "regular_security_audits": True,
            "no_data_breaches": True,
            "notes": ""
        },
        "parameter_h": {
            "contract_draft_available": True,
            "terms_clear": True,
            "liability_clauses_defined": True,
            "exit_clauses_defined": True,
            "ip_rights_clear": True,
            "governance_structure_defined": True,
            "escalation_process_defined": True,
            "notes": ""
        },
        "general_notes": "Sample partner for testing purposes",
        "assessor": "Risk Assessment Engine",
        "assessment_date": "2026-02-21T12:00:00"
    }


def _get_vendor_sample() -> Dict[str, Any]:
    """Get vendor sample data."""
    return {
        "vendor_info": {
            "name": "PT Sample Vendor",
            "website": "https://vendor-example.com",
            "vendor_type": "cloud service",
            "service_criticality": "high",
            "legal_entity_name": "PT Sample Vendor Indonesia",
            "registration_number": "AHU-67890",
            "country_of_operation": "Indonesia",
            "address": "Jl. Gatot Subroto No. 10, Jakarta",
            "years_in_business": 7,
            "number_of_employees": 150,
            "annual_revenue": "$10M - $50M"
        },
        "parameter_a": {
            "has_legal_entity": True,
            "registration_verified": True,
            "established_business": True,
            "has_client_base": True,
            "client_base_size": "100+ enterprise clients",
            "serves_similar_companies": True,
            "has_physical_presence": True,
            "management_team_experienced": True,
            "notes": ""
        },
        "parameter_b": {
            "financial_statements_available": True,
            "financial_health_stable": True,
            "revenue_stable": True,
            "has_insurance": True,
            "insurance_coverage_adequate": True,
            "insurance_type": "Professional liability and cyber insurance",
            "no_financial_distress": True,
            "notes": ""
        },
        "parameter_c": {
            "has_iso_27001": True,
            "has_soc2": True,
            "has_pci_dss": False,
            "has_other_security_certs": True,
            "other_certs": "CSA STAR",
            "certifications_current": True,
            "regular_penetration_testing": True,
            "vulnerability_management": True,
            "security_policies_documented": True,
            "notes": ""
        },
        "parameter_d": {
            "has_pdp_compliance": True,
            "has_privacy_policy": True,
            "has_dpa": True,
            "data_classification": True,
            "encryption_at_rest": True,
            "encryption_in_transit": True,
            "data_retention_policy": True,
            "data_deletion_capability": True,
            "cross_border_transfer": True,
            "cross_border_safeguards": True,
            "notes": ""
        },
        "parameter_e": {
            "has_sla": True,
            "sla_uptime": "99.9%",
            "sla_history_good": True,
            "has_support_team": True,
            "support_hours": "24/7",
            "support_response_time": "< 4 hours for critical issues",
            "has_escalation_process": True,
            "has_account_manager": True,
            "change_management": True,
            "incident_management": True,
            "notes": ""
        },
        "parameter_f": {
            "has_bcp": True,
            "has_drp": True,
            "bcp_documented": True,
            "drp_documented": True,
            "rto_defined": True,
            "rto_value": "4 hours",
            "rpo_defined": True,
            "rpo_value": "1 hour",
            "bcp_tested": True,
            "last_bcp_test": "2025-11-15",
            "has_backup_site": True,
            "geo_redundancy": True,
            "notes": ""
        },
        "parameter_g": {
            "infrastructure_reliable": True,
            "uptime_track_record": "99.95%",
            "has_scalability": True,
            "monitoring_capability": True,
            "has_status_page": True,
            "uses_reputable_providers": True,
            "infrastructure_providers": "AWS, Google Cloud",
            "has_capacity_planning": True,
            "notes": ""
        },
        "parameter_h": {
            "contract_terms_clear": True,
            "liability_caps_defined": True,
            "indemnification_clause": True,
            "exit_clauses_defined": True,
            "data_return_clause": True,
            "audit_rights": True,
            "ip_ownership_clear": True,
            "notes": ""
        },
        "parameter_i": {
            "references_available": True,
            "reference_count": 5,
            "references_verified": True,
            "has_market_reputation": True,
            "no_negative_news": True,
            "no_recent_breaches": True,
            "last_breach_date": None,
            "breach_remediated": False,
            "industry_recognition": True,
            "notes": ""
        },
        "general_notes": "Sample vendor for testing purposes",
        "assessor": "Risk Assessment Engine",
        "assessment_date": "2026-02-21T12:00:00"
    }


def _get_ai_sample() -> Dict[str, Any]:
    """Get AI project sample data."""
    return {
        "project_info": {
            "project_name": "Sample AI Project",
            "project_owner": "John Doe",
            "department": "Data Science",
            "project_description": "AI-powered customer service chatbot",
            "ai_type": "GenAI / LLM",
            "is_external_facing": True,
            "processes_personal_data": True
        },
        "section_a": {
            "processes_personal_data": True,
            "a1_explanation": "Processes customer name, email, and transaction history for context",
            "pdpwg_approved": True,
            "a2_explanation": "PDPWG approval obtained on 2026-01-15",
            "notes": ""
        },
        "section_b": {
            "is_external_facing": True,
            "b1_explanation": "Chatbot is available on public website and mobile app",
            "it_security_reviewed": True,
            "b2_explanation": "Security review completed, pentest scheduled for Q2 2026",
            "notes": ""
        },
        "section_c": {
            "has_clear_problem": True,
            "c1_explanation": "Reduce customer service response time and handle 24/7 inquiries",
            "has_measurable_benefit": True,
            "c2_explanation": "Expected 60% reduction in response time, 40% cost savings",
            "kpi_kri_defined": True,
            "value_exceeds_cost_risk": True,
            "notes": ""
        },
        "section_d": {
            "has_ai_owner": True,
            "d1_explanation": "AI system owner is the Head of Customer Service",
            "ai_owner_name": "Jane Smith",
            "has_human_oversight": True,
            "d2_explanation": "Human agents can take over conversation at any time",
            "override_mechanism": "Escalation to human agent button always visible",
            "notes": ""
        },
        "section_e": {
            "has_testing": True,
            "e1_explanation": "Tested with 1000+ test cases including edge cases",
            "test_coverage": "Normal cases, edge cases, adversarial inputs",
            "has_fallback": True,
            "e2_explanation": "Falls back to search-based FAQ if LLM unavailable",
            "fallback_description": "Rule-based fallback with human escalation",
            "has_monitoring_plan": True,
            "e3_explanation": "Daily monitoring of response quality and user satisfaction",
            "monitoring_metrics": "Response time, user rating, escalation rate, accuracy",
            "notes": ""
        },
        "section_f": {
            "has_bias_check": True,
            "f1_explanation": "Bias testing conducted across demographic groups",
            "bias_check_method": "A/B testing with diverse user groups",
            "can_detect_correct_bias": True,
            "f2_explanation": "Automated bias detection with manual review process",
            "correction_mechanism": "Weekly bias review with model retraining pipeline",
            "notes": ""
        },
        "section_g": {
            "has_user_notification": True,
            "g1_explanation": "Users are informed they are chatting with AI assistant",
            "notification_method": "Clear disclosure at start of chat session",
            "has_explainability": True,
            "g2_explanation": "Can provide reason codes for recommendations",
            "explanation_method": "Natural language explanations with confidence scores",
            "notes": ""
        },
        "general_notes": "Sample AI project data for testing purposes",
        "assessor": "Risk Assessment Engine",
        "assessment_date": "2026-02-21T12:00:00"
    }


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        prog="risk_assessment_engine",
        description="Risk Assessment Engine - Supports Merchant, Partner, Vendor, and AI Project assessments"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Merchant assessment (existing)
    assess_parser = subparsers.add_parser("assess", help="Run merchant risk assessment")
    assess_parser.add_argument("input", help="Path to research_data.json")
    assess_parser.add_argument("--output", "-o", help="Output JSON result file")
    assess_parser.add_argument("--report", "-r", help="Output markdown report file")

    # Partner assessment (new)
    assess_partner_parser = subparsers.add_parser("assess-partner", help="Run partner assessment")
    assess_partner_parser.add_argument("input", help="Path to partner_data.json")
    assess_partner_parser.add_argument("--output", "-o", help="Output JSON result file")
    assess_partner_parser.add_argument("--report", "-r", help="Output markdown report file")

    # Vendor assessment (new)
    assess_vendor_parser = subparsers.add_parser("assess-vendor", help="Run vendor assessment")
    assess_vendor_parser.add_argument("input", help="Path to vendor_data.json")
    assess_vendor_parser.add_argument("--output", "-o", help="Output JSON result file")
    assess_vendor_parser.add_argument("--report", "-r", help="Output markdown report file")

    # AI project assessment (new)
    assess_ai_parser = subparsers.add_parser("assess-ai", help="Run AI project assessment")
    assess_ai_parser.add_argument("input", help="Path to ai_project_data.json")
    assess_ai_parser.add_argument("--output", "-o", help="Output JSON result file")
    assess_ai_parser.add_argument("--report", "-r", help="Output markdown report file")

    # Validate (existing)
    validate_parser = subparsers.add_parser("validate", help="Validate research data file")
    validate_parser.add_argument("input", help="Path to research_data.json")

    # Validate partner/vendor/ai (v2)
    validate_partner_parser = subparsers.add_parser("validate-partner", help="Validate partner data file")
    validate_partner_parser.add_argument("input", help="Path to partner_data.json")

    validate_vendor_parser = subparsers.add_parser("validate-vendor", help="Validate vendor data file")
    validate_vendor_parser.add_argument("input", help="Path to vendor_data.json")

    validate_ai_parser = subparsers.add_parser("validate-ai", help="Validate AI project data file")
    validate_ai_parser.add_argument("input", help="Path to ai_project_data.json")

    # Sample (enhanced)
    sample_parser = subparsers.add_parser("sample", help="Generate sample data file")
    sample_parser.add_argument("--type", "-t", default="merchant",
                               choices=["merchant", "partner", "vendor", "ai"],
                               help="Type of sample to generate (default: merchant)")
    sample_parser.add_argument("--output", "-o", help="Output file path")

    args = parser.parse_args()

    if args.command == "assess":
        return cmd_assess(args)
    elif args.command == "assess-partner":
        return cmd_assess_partner(args)
    elif args.command == "assess-vendor":
        return cmd_assess_vendor(args)
    elif args.command == "assess-ai":
        return cmd_assess_ai(args)
    elif args.command == "validate":
        return cmd_validate(args)
    elif args.command == "validate-partner":
        return cmd_validate_partner(args)
    elif args.command == "validate-vendor":
        return cmd_validate_vendor(args)
    elif args.command == "validate-ai":
        return cmd_validate_ai(args)
    elif args.command == "sample":
        return cmd_sample(args)
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
