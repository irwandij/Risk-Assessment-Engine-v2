"""
Input schema for research data produced by LLM research phase.
This is the structured output from Phase 1 (Deep Research Agent).
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class MerchantInfo(BaseModel):
    """Basic merchant information."""
    name: str = Field(..., description="Merchant/company name")
    website: Optional[str] = Field(None, description="Primary website URL")
    business_type: str = Field(..., description="Type of business (e.g., 'subscription service', 'payment gateway')")
    legal_entity_name: Optional[str] = Field(None, description="Registered legal entity name (PT/CV)")
    registration_number: Optional[str] = Field(None, description="Business registration number")
    address: Optional[str] = Field(None, description="Physical business address")
    
    processes_payments_for_others: bool = Field(
        False,
        description="CRITICAL: Does this merchant process payments on behalf of OTHER merchants? (True = PJP/Aggregator)"
    )
    
    claimed_bi_license: Optional[bool] = Field(None, description="Merchant claims to have BI PJP license")
    bi_license_number: Optional[str] = Field(None, description="BI PJP license number if claimed")
    
    subscription_model: bool = Field(
        True,
        description="Does the merchant operate on a subscription/recurring billing model?"
    )


class ChecklistItem(BaseModel):
    """A single checklist item with verification status."""
    item: str = Field(..., description="Checklist item description")
    verified: bool = Field(False, description="Whether this item is verified/true")
    evidence: Optional[str] = Field(None, description="Evidence URL or description")
    notes: Optional[str] = Field(None, description="Additional notes")


class ParameterFindings(BaseModel):
    """Research findings for a single parameter."""
    
    parameter_id: str = Field(..., description="Parameter identifier (A-I)")
    
    checklist: List[ChecklistItem] = Field(
        default_factory=list,
        description="Verified checklist items for this parameter"
    )
    
    raw_findings: str = Field(
        "",
        description="Raw research notes and findings from LLM"
    )
    
    sources: List[str] = Field(
        default_factory=list,
        description="List of source URLs used for this parameter"
    )
    
    confidence: str = Field(
        "medium",
        description="Confidence level of findings: high, medium, low"
    )


class RegulatoryFindings(BaseModel):
    """Special findings for Parameter B (Regulatory)."""
    is_pjp_or_aggregator: bool = Field(False, description="Is this a PJP/Aggregator?")
    bi_license_verified: bool = Field(False, description="BI license verified in official registry")
    bi_license_number: Optional[str] = Field(None, description="License number if verified")
    license_scope_matches: Optional[bool] = Field(None, description="Does license scope match business?")
    ojk_registered: bool = Field(False, description="OJK registration if applicable")
    pse_registered: bool = Field(False, description="PSE (electronic system provider) registration")
    notes: str = Field("", description="Additional regulatory notes")
    
    bi_registry_checked: bool = Field(False, description="Whether BI registry was manually checked")
    bi_registry_found: bool = Field(False, description="Whether license was found in BI registry")
    bi_registry_category: Optional[str] = Field(None, description="BI registry category (e.g., 'PJP Kategori 3', 'PTD')")
    bi_registry_license_number: Optional[str] = Field(None, description="License number from BI registry")
    bi_registry_decision_number: Optional[str] = Field(None, description="Decision number from BI registry")
    bi_registry_date: Optional[str] = Field(None, description="License date from BI registry")
    bi_registry_status: Optional[str] = Field(None, description="Status: 'Berizin (Telah Operasional)', 'Berizin (Belum Operasional)', 'Izin Dicabut', 'Terdaftar'")
    bi_registry_url: Optional[str] = Field(None, description="Direct link to BI registry detail page")
    bi_verification_notes: str = Field("", description="Notes from BI registry verification process")


class ReputationFindings(BaseModel):
    """Special findings for Parameter I (Reputation)."""
    has_social_media: bool = Field(False)
    has_linkedin: bool = Field(False)
    has_google_maps: bool = Field(False)
    has_press_coverage: bool = Field(False)
    app_store_rating: Optional[float] = Field(None, description="App rating if available")
    review_count: Optional[int] = Field(None, description="Number of reviews")
    negative_news: List[str] = Field(default_factory=list, description="Negative news found")
    positive_news: List[str] = Field(default_factory=list, description="Positive news found")
    scam_allegations: bool = Field(False, description="Any scam allegations found")
    regulatory_enforcement: bool = Field(False, description="Any regulatory enforcement actions")
    notes: str = Field("", description="Additional reputation notes")


class SecurityFindings(BaseModel):
    """Special findings for Parameter H (Security)."""
    has_https: bool = Field(False)
    website_stable: bool = Field(False)
    has_secure_login: bool = Field(False)
    ssl_valid: bool = Field(False)
    phishing_indicators: bool = Field(False)
    malware_detected: bool = Field(False)
    notes: str = Field("", description="Additional security notes")


class ConsumerProtectionFindings(BaseModel):
    """Special findings for Parameter F (Consumer Protection)."""
    has_email_support: bool = Field(False)
    has_phone_support: bool = Field(False)
    has_chat_support: bool = Field(False)
    has_faq: bool = Field(False)
    has_escalation_path: bool = Field(False)
    has_sla: bool = Field(False)
    response_time_hours: Optional[int] = Field(None)
    notes: str = Field("", description="Additional consumer protection notes")


class PrivacyFindings(BaseModel):
    """Special findings for Parameter G (Privacy & PDP)."""
    has_privacy_policy: bool = Field(False)
    privacy_policy_url: Optional[str] = Field(None)
    has_data_retention_policy: bool = Field(False)
    has_user_rights_section: bool = Field(False)
    has_dpo_contact: bool = Field(False)
    pdp_compliant: bool = Field(False, description="Appears PDP Law compliant")
    policy_date: Optional[str] = Field(None, description="Privacy policy last updated date")
    notes: str = Field("", description="Additional privacy notes")


class PaymentTransparencyFindings(BaseModel):
    """Special findings for Parameter D (Payment Transparency)."""
    has_fee_disclosure: bool = Field(False)
    has_billing_cycle: bool = Field(False)
    has_settlement_info: bool = Field(False)
    has_refund_policy: bool = Field(False)
    has_dispute_process: bool = Field(False)
    has_sla: bool = Field(False)
    pricing_clear: bool = Field(False)
    notes: str = Field("", description="Additional payment transparency notes")


class TCFindings(BaseModel):
    """Special findings for Parameter E (T&C Completeness)."""
    has_terms_page: bool = Field(False)
    has_cancellation_policy: bool = Field(False)
    has_refund_policy: bool = Field(False)
    has_dispute_clause: bool = Field(False)
    has_jurisdiction_clause: bool = Field(False)
    has_fee_schedule: bool = Field(False)
    tc_accessible: bool = Field(False)
    tc_current: bool = Field(False, description="T&C appears current/not outdated")
    notes: str = Field("", description="Additional T&C notes")


class ProductClarityFindings(BaseModel):
    """Special findings for Parameter C (Product Clarity)."""
    services_clearly_described: bool = Field(False)
    has_scope_documentation: bool = Field(False)
    has_deliverables: bool = Field(False)
    has_limitations: bool = Field(False)
    no_misleading_claims: bool = Field(True)
    notes: str = Field("", description="Additional product clarity notes")


class CompanyIdentityFindings(BaseModel):
    """Special findings for Parameter A (Company Identity)."""
    has_legal_entity: bool = Field(False)
    legal_entity_type: Optional[str] = Field(None, description="PT, CV, etc.")
    has_address: bool = Field(False)
    address_verified: bool = Field(False)
    has_phone: bool = Field(False)
    has_email: bool = Field(False)
    has_contact_form: bool = Field(False)
    info_consistent: bool = Field(False, description="Info consistent across sources")
    linkedin_verified: bool = Field(False)
    google_maps_verified: bool = Field(False)
    notes: str = Field("", description="Additional identity notes")


class ResearchData(BaseModel):
    """
    Complete research data structure for merchant assessment.
    This is the INPUT to the Python assessment engine.
    """
    
    merchant_info: MerchantInfo = Field(..., description="Basic merchant information")
    
    parameter_a: CompanyIdentityFindings = Field(
        default_factory=CompanyIdentityFindings,
        description="Parameter A: Company Identity findings"
    )
    parameter_b: RegulatoryFindings = Field(
        default_factory=RegulatoryFindings,
        description="Parameter B: Regulatory findings"
    )
    parameter_c: ProductClarityFindings = Field(
        default_factory=ProductClarityFindings,
        description="Parameter C: Product Clarity findings"
    )
    parameter_d: PaymentTransparencyFindings = Field(
        default_factory=PaymentTransparencyFindings,
        description="Parameter D: Payment Transparency findings"
    )
    parameter_e: TCFindings = Field(
        default_factory=TCFindings,
        description="Parameter E: T&C Completeness findings"
    )
    parameter_f: ConsumerProtectionFindings = Field(
        default_factory=ConsumerProtectionFindings,
        description="Parameter F: Consumer Protection findings"
    )
    parameter_g: PrivacyFindings = Field(
        default_factory=PrivacyFindings,
        description="Parameter G: Privacy & PDP findings"
    )
    parameter_h: SecurityFindings = Field(
        default_factory=SecurityFindings,
        description="Parameter H: Security findings"
    )
    parameter_i: ReputationFindings = Field(
        default_factory=ReputationFindings,
        description="Parameter I: Reputation findings"
    )
    
    general_notes: str = Field("", description="General research notes")
    
    research_date: datetime = Field(
        default_factory=datetime.now,
        description="Date research was conducted"
    )
    
    researcher: str = Field("", description="Researcher/agent identifier")
    
    @property
    def is_pjp(self) -> bool:
        """Convenience property to check if merchant is PJP/Aggregator."""
        return (
            self.merchant_info.processes_payments_for_others or
            self.parameter_b.is_pjp_or_aggregator
        )
