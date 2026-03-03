"""
Input schema for Partner assessment data.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class PartnerInfo(BaseModel):
    """Basic partner information."""
    name: str = Field(..., description="Partner/company name")
    website: Optional[str] = Field(None, description="Primary website URL")
    partnership_type: str = Field(
        ...,
        description="Type of partnership (e.g., 'strategic alliance', 'joint venture', 'distribution')"
    )
    legal_entity_name: Optional[str] = Field(None, description="Registered legal entity name (PT/CV)")
    registration_number: Optional[str] = Field(None, description="Business registration number")
    country_of_incorporation: str = Field(
        "Indonesia",
        description="Country where the partner is incorporated"
    )
    address: Optional[str] = Field(None, description="Physical business address")
    industry_sector: Optional[str] = Field(None, description="Industry sector of the partner")
    years_in_business: Optional[int] = Field(None, description="Number of years in business")


class CompanyProfileFindings(BaseModel):
    """Parameter A: Company Profile findings."""
    has_legal_entity: bool = Field(False, description="Has valid legal entity registration")
    legal_entity_type: Optional[str] = Field(None, description="PT, CV, etc.")
    registration_verified: bool = Field(False, description="Registration verified with authorities")
    has_address: bool = Field(False, description="Physical address available")
    ownership_structure_clear: bool = Field(False, description="Ownership structure is transparent")
    beneficial_owners_identified: bool = Field(False, description="Ultimate beneficial owners identified")
    politically_exposed: bool = Field(False, description="Any PEP (Politically Exposed Person) connection")
    subsidiaries_listed: bool = Field(False, description="Subsidiaries and affiliates listed")
    notes: str = Field("", description="Additional notes")


class FinancialStabilityFindings(BaseModel):
    """Parameter B: Financial Stability findings."""
    financial_statements_available: bool = Field(False, description="Financial statements available")
    audited_financials: bool = Field(False, description="Financials are audited")
    revenue_trend_positive: bool = Field(False, description="Revenue trend is positive over 3 years")
    profitability_trend_positive: bool = Field(False, description="Profitability trend is positive")
    debt_to_equity_healthy: bool = Field(False, description="Debt-to-equity ratio is healthy")
    current_ratio_healthy: bool = Field(False, description="Current ratio is healthy (1.5+)")
    has_credit_rating: bool = Field(False, description="Has credit rating from rating agency")
    credit_rating_value: Optional[str] = Field(None, description="Credit rating value (e.g., AAA, AA)")
    insurance_coverage_adequate: bool = Field(False, description="Insurance coverage is adequate")
    notes: str = Field("", description="Additional notes")


class StrategicAlignmentFindings(BaseModel):
    """Parameter C: Strategic Alignment findings."""
    business_model_aligned: bool = Field(False, description="Business model aligns with our strategy")
    shared_objectives: bool = Field(False, description="Shared strategic objectives")
    complementary_capabilities: bool = Field(False, description="Capabilities complement each other")
    market_position_aligned: bool = Field(False, description="Market position is compatible")
    cultural_fit: bool = Field(False, description="Corporate culture is compatible")
    long_term_commitment: bool = Field(False, description="Evidence of long-term commitment")
    partnership_value_proposition: bool = Field(False, description="Clear value proposition for partnership")
    notes: str = Field("", description="Additional notes")


class OperationalCapabilityFindings(BaseModel):
    """Parameter D: Operational Capability findings."""
    has_track_record: bool = Field(False, description="Proven track record in relevant field")
    years_of_experience: Optional[int] = Field(None, description="Years of relevant experience")
    has_expertise: bool = Field(False, description="Has required expertise and skills")
    management_team_qualified: bool = Field(False, description="Management team is qualified")
    has_adequate_resources: bool = Field(False, description="Has adequate resources (people, technology)")
    operational_processes_documented: bool = Field(False, description="Operational processes are documented")
    quality_certifications: bool = Field(False, description="Has relevant quality certifications (ISO, etc.)")
    project_management_capability: bool = Field(False, description="Demonstrates project management capability")
    innovation_capability: bool = Field(False, description="Demonstrates innovation capability")
    notes: str = Field("", description="Additional notes")


class RegulatoryComplianceFindings(BaseModel):
    """Parameter E: Regulatory Compliance findings."""
    has_required_licenses: bool = Field(False, description="Has all required licenses for business")
    licenses_verified: bool = Field(False, description="Licenses verified with authorities")
    license_expiry_date: Optional[str] = Field(None, description="License expiry date")
    no_regulatory_issues: bool = Field(False, description="No regulatory issues or sanctions")
    compliance_program_exists: bool = Field(False, description="Compliance program exists")
    aml_kyc_compliant: bool = Field(False, description="AML/KYC compliant")
    sanctions_screened: bool = Field(False, description="Screened against sanctions lists")
    no_legal_issues: bool = Field(False, description="No pending legal issues or litigation")
    regulatory_stand: Optional[str] = Field(None, description="Current regulatory standing")
    notes: str = Field("", description="Additional notes")


class ReputationFindings(BaseModel):
    """Parameter F: Reputation & Track Record findings."""
    has_market_reputation: bool = Field(False, description="Has positive market reputation")
    references_available: bool = Field(False, description="Client/partner references available")
    reference_check_positive: bool = Field(False, description="Reference checks are positive")
    has_industry_recognition: bool = Field(False, description="Has industry recognition or awards")
    media_coverage_positive: bool = Field(False, description="Media coverage is generally positive")
    no_negative_news: bool = Field(False, description="No significant negative news")
    no_past_issues: bool = Field(False, description="No past partnership failures or issues")
    esg_rating_positive: bool = Field(False, description="Positive ESG (Environmental, Social, Governance) rating")
    notes: str = Field("", description="Additional notes")


class DataSecurityFindings(BaseModel):
    """Parameter G: Data & Security findings."""
    has_data_protection_policy: bool = Field(False, description="Has data protection policy")
    has_security_certifications: bool = Field(False, description="Has security certifications (ISO 27001, SOC 2)")
    data_handling_documented: bool = Field(False, description="Data handling procedures documented")
    encryption_standards: bool = Field(False, description="Uses encryption standards for data")
    access_controls: bool = Field(False, description="Has proper access controls")
    incident_response_plan: bool = Field(False, description="Has incident response plan")
    regular_security_audits: bool = Field(False, description="Conducts regular security audits")
    no_data_breaches: bool = Field(False, description="No history of data breaches")
    notes: str = Field("", description="Additional notes")


class ContractGovernanceFindings(BaseModel):
    """Parameter H: Contract & Governance findings."""
    contract_draft_available: bool = Field(False, description="Contract draft available for review")
    terms_clear: bool = Field(False, description="Contract terms are clear and fair")
    liability_clauses_defined: bool = Field(False, description="Liability clauses are well-defined")
    exit_clauses_defined: bool = Field(False, description="Exit/termination clauses defined")
    ip_rights_clear: bool = Field(False, description="Intellectual property rights are clear")
    governance_structure_defined: bool = Field(False, description="Governance structure defined")
    escalation_process_defined: bool = Field(False, description="Escalation process defined")
    notes: str = Field("", description="Additional notes")


class PartnerData(BaseModel):
    """
    Complete partner data structure for assessment.
    """
    partner_info: PartnerInfo = Field(..., description="Basic partner information")

    parameter_a: CompanyProfileFindings = Field(
        default_factory=CompanyProfileFindings,
        description="Parameter A: Company Profile findings"
    )
    parameter_b: FinancialStabilityFindings = Field(
        default_factory=FinancialStabilityFindings,
        description="Parameter B: Financial Stability findings"
    )
    parameter_c: StrategicAlignmentFindings = Field(
        default_factory=StrategicAlignmentFindings,
        description="Parameter C: Strategic Alignment findings"
    )
    parameter_d: OperationalCapabilityFindings = Field(
        default_factory=OperationalCapabilityFindings,
        description="Parameter D: Operational Capability findings"
    )
    parameter_e: RegulatoryComplianceFindings = Field(
        default_factory=RegulatoryComplianceFindings,
        description="Parameter E: Regulatory Compliance findings"
    )
    parameter_f: ReputationFindings = Field(
        default_factory=ReputationFindings,
        description="Parameter F: Reputation & Track Record findings"
    )
    parameter_g: DataSecurityFindings = Field(
        default_factory=DataSecurityFindings,
        description="Parameter G: Data & Security findings"
    )
    parameter_h: ContractGovernanceFindings = Field(
        default_factory=ContractGovernanceFindings,
        description="Parameter H: Contract & Governance findings"
    )

    general_notes: str = Field("", description="General assessment notes")

    assessment_date: datetime = Field(
        default_factory=datetime.now,
        description="Date assessment was conducted"
    )

    assessor: str = Field("", description="Assessor identifier")
