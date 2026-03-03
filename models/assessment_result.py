"""
Output schema for assessment result produced by Python engine.
This is the OUTPUT from Phase 2 (Assessment Engine).
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

from ..config import AssessmentType, MerchantType, RiskLevel, Decision


class ParameterScore(BaseModel):
    """Score for a single parameter."""
    parameter_id: str = Field(..., description="Parameter identifier (A-I)")
    parameter_name: str = Field(..., description="Full parameter name")
    score: int = Field(..., ge=0, description="Points awarded")
    max_score: int = Field(..., description="Maximum possible points")
    rating: str = Field(..., description="Rating: excellent, good, fair, weak, poor, fail")
    evidence: List[str] = Field(default_factory=list, description="Evidence supporting score")
    gaps: List[str] = Field(default_factory=list, description="Identified gaps/concerns")
    notes: str = Field("", description="Additional scoring notes")
    
    @property
    def percentage(self) -> float:
        """Calculate percentage score."""
        if self.max_score == 0:
            return 0.0
        return round((self.score / self.max_score) * 100, 1)


class AutoRejectTrigger(BaseModel):
    """Auto-reject trigger details."""
    code: str = Field(..., description="Trigger code")
    reason: str = Field(..., description="Human-readable reason")
    details: str = Field("", description="Additional details")


class Condition(BaseModel):
    """Condition for PROCEED WITH CONDITIONS decision."""
    condition: str = Field(..., description="Condition description")
    priority: str = Field("medium", description="Priority: high, medium, low")
    timeline_days: Optional[int] = Field(None, description="Timeline in days")
    category: str = Field("", description="Category: documentation, compliance, operational")


class Recommendation(BaseModel):
    """Risk treatment recommendation."""
    recommendation: str = Field(..., description="Recommendation description")
    priority: str = Field("medium", description="Priority: high, medium, low")
    category: str = Field("", description="Category for grouping")


class DecisionResult(BaseModel):
    """Final decision details."""
    decision: Decision = Field(..., description="Final decision")
    risk_level: RiskLevel = Field(..., description="Risk level")
    total_score: int = Field(..., ge=0, le=100, description="Total score out of 100")
    
    is_auto_rejected: bool = Field(False, description="Whether auto-reject was triggered")
    auto_reject_triggers: List[AutoRejectTrigger] = Field(
        default_factory=list,
        description="List of auto-reject triggers if applicable"
    )
    
    conditions: List[Condition] = Field(
        default_factory=list,
        description="Conditions for PROCEED WITH CONDITIONS"
    )
    
    gate_override: bool = Field(
        False,
        description="Whether regulatory gate override was applied"
    )
    gate_override_reason: str = Field("", description="Reason for gate override")


class AssessmentResult(BaseModel):
    """
    Complete assessment result from Python engine.
    This is the OUTPUT that will be passed to report generator.
    """
    
    merchant_name: str = Field(..., description="Merchant name")
    merchant_type: MerchantType | AssessmentType = Field(
        ...,
        description="Classified assessment type/merchant type"
    )
    
    classification: Dict[str, Any] = Field(
        default_factory=dict,
        description="Classification details"
    )
    
    parameter_scores: Dict[str, ParameterScore] = Field(
        default_factory=dict,
        description="Scores for all parameters A-I"
    )
    
    total_score: int = Field(..., ge=0, le=100, description="Total score")
    
    decision_result: DecisionResult = Field(
        ...,
        description="Final decision details"
    )
    
    strengths: List[str] = Field(
        default_factory=list,
        description="Identified strengths"
    )
    
    concerns: List[str] = Field(
        default_factory=list,
        description="Identified concerns"
    )
    
    recommendations: List[Recommendation] = Field(
        default_factory=list,
        description="Risk treatment recommendations"
    )
    
    regulatory_gate: Optional[Dict[str, Any]] = Field(
        None,
        description="Regulatory gate check details (for PJP/Aggregators)"
    )

    reference_urls: Dict[str, str] = Field(
        default_factory=dict,
        description="Reference URLs from input data (website, privacy policy, BI registry, etc.)"
    )

    assessment_date: datetime = Field(
        default_factory=datetime.now,
        description="Assessment date"
    )
    
    framework_version: str = Field("2.1", description="Framework version used")
    
    @property
    def decision(self) -> Decision:
        """Convenience property for decision."""
        return self.decision_result.decision
    
    @property
    def risk_level(self) -> RiskLevel:
        """Convenience property for risk level."""
        return self.decision_result.risk_level
