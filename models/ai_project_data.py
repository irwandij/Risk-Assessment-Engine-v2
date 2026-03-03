"""
Input schema for AI Project assessment data.
Based on DANA AI Policy assessment framework.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class AIProjectInfo(BaseModel):
    """Basic AI project information."""
    project_name: str = Field(..., description="AI project name")
    project_owner: str = Field(..., description="AI project owner name")
    department: Optional[str] = Field(None, description="Department/team")
    project_description: Optional[str] = Field(None, description="Brief project description")
    ai_type: Optional[str] = Field(None, description="Type of AI (e.g., 'ML model', 'GenAI', 'NLP')")
    is_external_facing: bool = Field(False, description="Is the AI system customer/external facing?")
    processes_personal_data: bool = Field(False, description="Does the AI process personal data?")


class QuestionResponse(BaseModel):
    """A single question response."""
    answer: Optional[bool] = Field(None, description="Yes/No answer")
    explanation: Optional[str] = Field(None, description="Explanation/justification for the answer")


class PrivacyPDPFindings(BaseModel):
    """
    Section A: Privacy & PDP Compliance (HARD STOP).

    If AI processes personal data, PDPWG approval is required.
    """
    # A1: Does this AI process personal data?
    processes_personal_data: Optional[bool] = Field(None)
    a1_explanation: Optional[str] = Field(None)

    # A2: If Yes, has PDPWG formally approved this AI use?
    pdpwg_approved: Optional[bool] = Field(None)
    a2_explanation: Optional[str] = Field(None)

    notes: str = Field("", description="Additional notes")

    @property
    def is_hard_stop(self) -> bool:
        """Check if this section triggers a hard stop."""
        # Hard stop if processes personal data AND not PDPWG approved
        if self.processes_personal_data is True and self.pdpwg_approved is False:
            return True
        return False


class SecurityFindings(BaseModel):
    """
    Section B: Security (HARD STOP - conditional).

    Hard stop only if external facing AND not reviewed by IT.
    """
    # B1: Will this AI be used by Customer / External Facing users?
    is_external_facing: Optional[bool] = Field(None)
    b1_explanation: Optional[str] = Field(None)

    # B2: If Yes, has IT / Security reviewed the system?
    it_security_reviewed: Optional[bool] = Field(None)
    b2_explanation: Optional[str] = Field(None)

    notes: str = Field("", description="Additional notes")

    @property
    def is_hard_stop(self) -> bool:
        """Check if this section triggers a hard stop."""
        # Hard stop if external facing AND not IT reviewed
        if self.is_external_facing is True and self.it_security_reviewed is False:
            return True
        return False


class ValueFindings(BaseModel):
    """
    Section C: Value (HARD STOP).

    Clear business problem and measurable benefit required.
    """
    # C1: Is there a clear business or operational problem being solved?
    has_clear_problem: Optional[bool] = Field(None)
    c1_explanation: Optional[str] = Field(None)

    # C2: Does the AI deliver measurable benefit?
    has_measurable_benefit: Optional[bool] = Field(None)
    c2_explanation: Optional[str] = Field(None)

    kpi_kri_defined: Optional[bool] = Field(None, description="Are KPI/KRI defined?")
    value_exceeds_cost_risk: Optional[bool] = Field(None, description="Expected value outweighs cost and risk?")

    notes: str = Field("", description="Additional notes")

    @property
    def is_hard_stop(self) -> bool:
        """Check if this section triggers a hard stop."""
        # Hard stop if no clear problem OR no measurable benefit
        if self.has_clear_problem is False or self.has_measurable_benefit is False:
            return True
        return False


class AccountabilityFindings(BaseModel):
    """
    Section D: Accountability & Human Oversight (4 pts max).

    AI owner designation and human override capability.
    """
    # D1: Is there a named AI system owner?
    has_ai_owner: Optional[bool] = Field(None)
    d1_explanation: Optional[str] = Field(None)
    ai_owner_name: Optional[str] = Field(None)

    # D2: Can humans review, override, or stop AI decisions?
    has_human_oversight: Optional[bool] = Field(None)
    d2_explanation: Optional[str] = Field(None)
    override_mechanism: Optional[str] = Field(None, description="Description of override mechanism")

    notes: str = Field("", description="Additional notes")


class ReliabilityFindings(BaseModel):
    """
    Section E: Reliability & Monitoring (4 pts max).

    Testing, fallback, and monitoring capabilities.
    """
    # E1: Has the AI been tested in normal and edge cases?
    has_testing: Optional[bool] = Field(None)
    e1_explanation: Optional[str] = Field(None)
    test_coverage: Optional[str] = Field(None, description="Test coverage description")

    # E2: Is there a fallback or manual process if AI fails?
    has_fallback: Optional[bool] = Field(None)
    e2_explanation: Optional[str] = Field(None)
    fallback_description: Optional[str] = Field(None)

    # E3: Is there a monitoring plan for accuracy, errors, or drift?
    has_monitoring_plan: Optional[bool] = Field(None)
    e3_explanation: Optional[str] = Field(None)
    monitoring_metrics: Optional[str] = Field(None, description="Key monitoring metrics")

    notes: str = Field("", description="Additional notes")


class FairnessFindings(BaseModel):
    """
    Section F: Fairness (4 pts max).

    Bias checking and correction capabilities.
    """
    # F1: Has the AI been checked for unfair bias?
    has_bias_check: Optional[bool] = Field(None)
    f1_explanation: Optional[str] = Field(None)
    bias_check_method: Optional[str] = Field(None)

    # F2: Can unfair outcomes be detected and corrected?
    can_detect_correct_bias: Optional[bool] = Field(None)
    f2_explanation: Optional[str] = Field(None)
    correction_mechanism: Optional[str] = Field(None)

    notes: str = Field("", description="Additional notes")


class TransparencyFindings(BaseModel):
    """
    Section G: Transparency (4 pts max).

    User notification and explainability.
    """
    # G1: Are users/stakeholders informed when interacting with AI?
    has_user_notification: Optional[bool] = Field(None)
    g1_explanation: Optional[str] = Field(None)
    notification_method: Optional[str] = Field(None)

    # G2: Can decisions be explained at a business level?
    has_explainability: Optional[bool] = Field(None)
    g2_explanation: Optional[str] = Field(None)
    explanation_method: Optional[str] = Field(None, description="How decisions are explained")

    notes: str = Field("", description="Additional notes")


class AIProjectData(BaseModel):
    """
    Complete AI project data structure for assessment.
    Based on DANA AI Policy framework.
    """
    project_info: AIProjectInfo = Field(..., description="Basic project information")

    section_a: PrivacyPDPFindings = Field(
        default_factory=PrivacyPDPFindings,
        description="Section A: Privacy & PDP Compliance (Hard Stop)"
    )
    section_b: SecurityFindings = Field(
        default_factory=SecurityFindings,
        description="Section B: Security (Hard Stop if external)"
    )
    section_c: ValueFindings = Field(
        default_factory=ValueFindings,
        description="Section C: Value (Hard Stop)"
    )
    section_d: AccountabilityFindings = Field(
        default_factory=AccountabilityFindings,
        description="Section D: Accountability & Human Oversight"
    )
    section_e: ReliabilityFindings = Field(
        default_factory=ReliabilityFindings,
        description="Section E: Reliability & Monitoring"
    )
    section_f: FairnessFindings = Field(
        default_factory=FairnessFindings,
        description="Section F: Fairness"
    )
    section_g: TransparencyFindings = Field(
        default_factory=TransparencyFindings,
        description="Section G: Transparency"
    )

    general_notes: str = Field("", description="General assessment notes")

    assessment_date: datetime = Field(
        default_factory=datetime.now,
        description="Date assessment was conducted"
    )

    assessor: str = Field("", description="Assessor identifier")

    @property
    def has_hard_stop(self) -> bool:
        """Check if any hard stop section failed."""
        return (
            self.section_a.is_hard_stop or
            self.section_b.is_hard_stop or
            self.section_c.is_hard_stop
        )

    @property
    def hard_stop_sections(self) -> List[str]:
        """Get list of sections that triggered hard stop."""
        sections = []
        if self.section_a.is_hard_stop:
            sections.append("Privacy & PDP Compliance")
        if self.section_b.is_hard_stop:
            sections.append("Security")
        if self.section_c.is_hard_stop:
            sections.append("Value")
        return sections
