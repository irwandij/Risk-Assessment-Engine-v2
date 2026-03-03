"""
Input schema for Vendor assessment data.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class VendorInfo(BaseModel):
    """Basic vendor information."""
    name: str = Field(..., description="Vendor/company name")
    website: Optional[str] = Field(None, description="Primary website URL")
    vendor_type: str = Field(
        ...,
        description="Type of vendor (e.g., 'cloud service', 'software provider', 'consulting')"
    )
    service_criticality: str = Field(
        ...,
        description="Service criticality level: 'critical', 'high', 'medium', 'low'"
    )
    legal_entity_name: Optional[str] = Field(None, description="Registered legal entity name")
    registration_number: Optional[str] = Field(None, description="Business registration number")
    country_of_operation: str = Field(
        "Indonesia",
        description="Primary country of operation"
    )
    address: Optional[str] = Field(None, description="Physical business address")
    years_in_business: Optional[int] = Field(None, description="Number of years in business")
    number_of_employees: Optional[int] = Field(None, description="Number of employees")
    annual_revenue: Optional[str] = Field(None, description="Annual revenue range")


class VendorProfileFindings(BaseModel):
    """Parameter A: Vendor Profile findings."""
    has_legal_entity: bool = Field(False, description="Has valid legal entity registration")
    registration_verified: bool = Field(False, description="Registration verified")
    established_business: bool = Field(False, description="Established business (3+ years)")
    has_client_base: bool = Field(False, description="Has established client base")
    client_base_size: Optional[str] = Field(None, description="Client base size (e.g., '50+ enterprise clients')")
    serves_similar_companies: bool = Field(False, description="Serves similar companies/industries")
    has_physical_presence: bool = Field(False, description="Has physical office presence")
    management_team_experienced: bool = Field(False, description="Management team is experienced")
    notes: str = Field("", description="Additional notes")


class FinancialHealthFindings(BaseModel):
    """Parameter B: Financial Health findings."""
    financial_statements_available: bool = Field(False, description="Financial statements available")
    financial_health_stable: bool = Field(False, description="Financial health is stable")
    revenue_stable: bool = Field(False, description="Revenue is stable/growing")
    has_insurance: bool = Field(False, description="Has liability insurance")
    insurance_coverage_adequate: bool = Field(False, description="Insurance coverage is adequate")
    insurance_type: Optional[str] = Field(None, description="Type of insurance coverage")
    no_financial_distress: bool = Field(False, description="No signs of financial distress")
    notes: str = Field("", description="Additional notes")


class SecurityComplianceFindings(BaseModel):
    """Parameter C: Security & Compliance findings."""
    has_iso_27001: bool = Field(False, description="Has ISO 27001 certification")
    has_soc2: bool = Field(False, description="Has SOC 2 Type II certification")
    has_pci_dss: bool = Field(False, description="Has PCI DSS compliance (if applicable)")
    has_other_security_certs: bool = Field(False, description="Has other security certifications")
    other_certs: Optional[str] = Field(None, description="Other certifications listed")
    certifications_current: bool = Field(False, description="Certifications are current/valid")
    regular_penetration_testing: bool = Field(False, description="Conducts regular penetration testing")
    vulnerability_management: bool = Field(False, description="Has vulnerability management program")
    security_policies_documented: bool = Field(False, description="Security policies are documented")
    notes: str = Field("", description="Additional notes")


class DataProtectionFindings(BaseModel):
    """Parameter D: Data Protection findings."""
    has_pdp_compliance: bool = Field(False, description="Compliant with PDP Law requirements")
    has_privacy_policy: bool = Field(False, description="Has privacy policy")
    has_dpa: bool = Field(False, description="Data Processing Agreement available")
    data_classification: bool = Field(Field=False, description="Has data classification scheme")
    encryption_at_rest: bool = Field(False, description="Encryption at rest implemented")
    encryption_in_transit: bool = Field(False, description="Encryption in transit implemented")
    data_retention_policy: bool = Field(False, description="Has data retention policy")
    data_deletion_capability: bool = Field(False, description="Can delete data on request")
    cross_border_transfer: bool = Field(False, description="Cross-border data transfer occurs")
    cross_border_safeguards: bool = Field(False, description="Has safeguards for cross-border transfer")
    notes: str = Field("", description="Additional notes")


class OperationalCapabilityFindings(BaseModel):
    """Parameter E: Operational Capability findings."""
    has_sla: bool = Field(False, description="Has Service Level Agreement")
    sla_uptime: Optional[str] = Field(None, description="SLA uptime commitment (e.g., '99.9%')")
    sla_history_good: bool = Field(False, description="SLA compliance history is good")
    has_support_team: bool = Field(False, description="Has dedicated support team")
    support_hours: Optional[str] = Field(None, description="Support hours (e.g., '24/7')")
    support_response_time: Optional[str] = Field(None, description="Support response time")
    has_escalation_process: bool = Field(False, description="Has escalation process")
    has_account_manager: bool = Field(False, description="Has dedicated account manager")
    change_management: bool = Field(False, description="Has change management process")
    incident_management: bool = Field(False, description="Has incident management process")
    notes: str = Field("", description="Additional notes")


class BCPDRPFindings(BaseModel):
    """Parameter F: BCP/DRP Readiness findings."""
    has_bcp: bool = Field(False, description="Has Business Continuity Plan")
    has_drp: bool = Field(False, description="Has Disaster Recovery Plan")
    bcp_documented: bool = Field(False, description="BCP is documented")
    drp_documented: bool = Field(False, description="DRP is documented")
    rto_defined: bool = Field(False, description="RTO (Recovery Time Objective) defined")
    rto_value: Optional[str] = Field(None, description="RTO value (e.g., '4 hours')")
    rpo_defined: bool = Field(False, description="RPO (Recovery Point Objective) defined")
    rpo_value: Optional[str] = Field(None, description="RPO value (e.g., '1 hour')")
    bcp_tested: bool = Field(False, description="BCP tested regularly")
    last_bcp_test: Optional[str] = Field(None, description="Last BCP test date")
    has_backup_site: bool = Field(False, description="Has backup/recovery site")
    geo_redundancy: bool = Field(False, description="Has geographic redundancy")
    notes: str = Field("", description="Additional notes")


class ITInfrastructureFindings(BaseModel):
    """Parameter G: IT Infrastructure findings."""
    infrastructure_reliable: bool = Field(False, description="Infrastructure is reliable")
    uptime_track_record: Optional[str] = Field(None, description="Historical uptime (e.g., '99.95%')")
    has_scalability: bool = Field(False, description="Has scalability capability")
    monitoring_capability: bool = Field(False, description="Has monitoring capability")
    has_status_page: bool = Field(False, description="Has public status page")
    uses_reputable_providers: bool = Field(False, description="Uses reputable infrastructure providers")
    infrastructure_providers: Optional[str] = Field(None, description="Infrastructure providers used")
    has_capacity_planning: bool = Field(False, description="Has capacity planning process")
    notes: str = Field("", description="Additional notes")


class ContractSLAFindings(BaseModel):
    """Parameter H: Contract & SLA findings."""
    contract_terms_clear: bool = Field(False, description="Contract terms are clear")
    liability_caps_defined: bool = Field(False, description="Liability caps are defined")
    indemnification_clause: bool = Field(False, description="Indemnification clause exists")
    exit_clauses_defined: bool = Field(False, description="Exit/termination clauses defined")
    data_return_clause: bool = Field(False, description="Data return/deletion clause exists")
    audit_rights: bool = Field(False, description="Audit rights included")
    ip_ownership_clear: bool = Field(False, description="IP ownership is clear")
    notes: str = Field("", description="Additional notes")


class ReferencesReputationFindings(BaseModel):
    """Parameter I: References & Reputation findings."""
    references_available: bool = Field(False, description="References available")
    reference_count: Optional[int] = Field(None, description="Number of references")
    references_verified: bool = Field(False, description="References verified")
    has_market_reputation: bool = Field(False, description="Has positive market reputation")
    no_negative_news: bool = Field(False, description="No significant negative news")
    no_recent_breaches: bool = Field(False, description="No recent security breaches")
    last_breach_date: Optional[str] = Field(None, description="Last breach date if any")
    breach_remediated: bool = Field(False, description="Breach remediated if occurred")
    industry_recognition: bool = Field(False, description="Has industry recognition")
    notes: str = Field("", description="Additional notes")


class VendorData(BaseModel):
    """
    Complete vendor data structure for assessment.
    """
    vendor_info: VendorInfo = Field(..., description="Basic vendor information")

    parameter_a: VendorProfileFindings = Field(
        default_factory=VendorProfileFindings,
        description="Parameter A: Vendor Profile findings"
    )
    parameter_b: FinancialHealthFindings = Field(
        default_factory=FinancialHealthFindings,
        description="Parameter B: Financial Health findings"
    )
    parameter_c: SecurityComplianceFindings = Field(
        default_factory=SecurityComplianceFindings,
        description="Parameter C: Security & Compliance findings"
    )
    parameter_d: DataProtectionFindings = Field(
        default_factory=DataProtectionFindings,
        description="Parameter D: Data Protection findings"
    )
    parameter_e: OperationalCapabilityFindings = Field(
        default_factory=OperationalCapabilityFindings,
        description="Parameter E: Operational Capability findings"
    )
    parameter_f: BCPDRPFindings = Field(
        default_factory=BCPDRPFindings,
        description="Parameter F: BCP/DRP Readiness findings"
    )
    parameter_g: ITInfrastructureFindings = Field(
        default_factory=ITInfrastructureFindings,
        description="Parameter G: IT Infrastructure findings"
    )
    parameter_h: ContractSLAFindings = Field(
        default_factory=ContractSLAFindings,
        description="Parameter H: Contract & SLA findings"
    )
    parameter_i: ReferencesReputationFindings = Field(
        default_factory=ReferencesReputationFindings,
        description="Parameter I: References & Reputation findings"
    )

    general_notes: str = Field("", description="General assessment notes")

    assessment_date: datetime = Field(
        default_factory=datetime.now,
        description="Date assessment was conducted"
    )

    assessor: str = Field("", description="Assessor identifier")
