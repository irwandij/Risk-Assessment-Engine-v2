"""Decision engine with decision bands and auto-reject logic."""

from typing import List, Tuple, Optional, Dict, Any
from ..models.assessment_result import (
    AssessmentResult,
    DecisionResult,
    ParameterScore,
    AutoRejectTrigger,
    Condition,
    Recommendation,
)
from ..models.research_data import ResearchData
from ..config import (
    Decision,
    RiskLevel,
    Decision as DecisionEnum,
    DECISION_BANDS,
    DECISION_RISK_LEVELS,
    AUTO_REJECT_REASONS,
    MerchantType,
)


class DecisionEngine:
    """
    Handles decision logic including:
    - Decision bands (80-100: PROCEED, 60-79: CONDITIONS, etc.)
    - Auto-reject triggers
    - Gate override for PJP/Aggregators
    """
    
    def __init__(self, merchant_type: MerchantType):
        self.merchant_type = merchant_type
        self._auto_reject_triggers: List[AutoRejectTrigger] = []
    
    def make_decision(
        self,
        total_score: int,
        parameter_scores: Dict[str, ParameterScore],
        data: ResearchData,
        regulatory_auto_reject: bool = False,
        regulatory_auto_reject_reason: str = ""
    ) -> DecisionResult:
        """
        Make final decision based on score and triggers.
        
        Args:
            total_score: Total assessment score (0-100)
            parameter_scores: Dict of parameter ID to ParameterScore
            data: Original research data
            regulatory_auto_reject: Whether Parameter B triggered auto-reject
            regulatory_auto_reject_reason: Reason code for regulatory rejection
            
        Returns:
            DecisionResult with decision, risk level, and conditions
        """
        self._auto_reject_triggers = []
        
        if regulatory_auto_reject:
            self._auto_reject_triggers.append(
                AutoRejectTrigger(
                    code=regulatory_auto_reject_reason or "NO_BI_LICENSE",
                    reason=AUTO_REJECT_REASONS.get(
                        regulatory_auto_reject_reason, "Regulatory non-compliance"
                    ),
                    details="PJP/Aggregator without verifiable BI license"
                )
            )
        
        self._check_auto_reject_triggers(data, parameter_scores)
        
        if self._auto_reject_triggers:
            return self._create_reject_decision(total_score)
        
        if total_score < 40:
            self._auto_reject_triggers.append(
                AutoRejectTrigger(
                    code="SCORE_TOO_LOW",
                    reason=AUTO_REJECT_REASONS["SCORE_TOO_LOW"],
                    details=f"Total score {total_score}/100 is below minimum threshold"
                )
            )
            return self._create_reject_decision(total_score)
        
        decision = self._get_decision_from_score(total_score)
        risk_level = DECISION_RISK_LEVELS[decision]
        
        conditions = []
        if decision == Decision.PROCEED_WITH_CONDITIONS:
            conditions = self._generate_conditions(parameter_scores, data)
        
        return DecisionResult(
            decision=decision,
            risk_level=risk_level,
            total_score=total_score,
            is_auto_rejected=False,
            auto_reject_triggers=[],
            conditions=conditions,
            gate_override=False,
            gate_override_reason=""
        )
    
    def _check_auto_reject_triggers(
        self,
        data: ResearchData,
        parameter_scores: Dict[str, ParameterScore]
    ) -> None:
        """Check for auto-reject triggers."""
        
        if not data.merchant_info.subscription_model:
            self._auto_reject_triggers.append(
                AutoRejectTrigger(
                    code="NON_SUBSCRIPTION_MODEL",
                    reason=AUTO_REJECT_REASONS["NON_SUBSCRIPTION_MODEL"],
                    details="Business model is not subscription-based (required for autodebit)"
                )
            )
        
        if data.parameter_i.regulatory_enforcement:
            self._auto_reject_triggers.append(
                AutoRejectTrigger(
                    code="CONFIRMED_FRAUD",
                    reason=AUTO_REJECT_REASONS["CONFIRMED_FRAUD"],
                    details="Regulatory enforcement action found"
                )
            )
        
        if data.parameter_h.malware_detected:
            self._auto_reject_triggers.append(
                AutoRejectTrigger(
                    code="CONFIRMED_FRAUD",
                    reason=AUTO_REJECT_REASONS["CONFIRMED_FRAUD"],
                    details="Malware detected on merchant website"
                )
            )
        
        if data.parameter_i.scam_allegations and data.parameter_i.app_store_rating:
            if data.parameter_i.app_store_rating < 3.0:
                self._auto_reject_triggers.append(
                    AutoRejectTrigger(
                        code="LOW_APP_RATING",
                        reason=AUTO_REJECT_REASONS["LOW_APP_RATING"],
                        details=f"App rating {data.parameter_i.app_store_rating}/5 with negative news"
                    )
                )
        
        identity_score = parameter_scores.get("A")
        reputation_score = parameter_scores.get("I")
        
        if identity_score and identity_score.score == 0:
            has_presence = (
                data.parameter_i.has_social_media or
                data.parameter_i.has_linkedin or
                (data.merchant_info.website is not None)
            )
            if not has_presence:
                self._auto_reject_triggers.append(
                    AutoRejectTrigger(
                        code="NO_ONLINE_PRESENCE",
                        reason=AUTO_REJECT_REASONS["NO_ONLINE_PRESENCE"],
                        details="No website, social media, or other online presence found"
                    )
                )
    
    def _get_decision_from_score(self, score: int) -> Decision:
        """Get decision from score using decision bands."""
        for (min_score, max_score), decision in DECISION_BANDS.items():
            if min_score <= score <= max_score:
                return decision
        return Decision.REJECT
    
    def _create_reject_decision(self, total_score: int) -> DecisionResult:
        """Create a reject decision result."""
        return DecisionResult(
            decision=Decision.REJECT,
            risk_level=RiskLevel.VERY_HIGH,
            total_score=total_score,
            is_auto_rejected=True,
            auto_reject_triggers=self._auto_reject_triggers,
            conditions=[],
            gate_override=len(self._auto_reject_triggers) > 0,
            gate_override_reason=self._auto_reject_triggers[0].code if self._auto_reject_triggers else ""
        )
    
    def _generate_conditions(
        self,
        parameter_scores: Dict[str, ParameterScore],
        data: ResearchData
    ) -> List[Condition]:
        """Generate conditions for PROCEED WITH CONDITIONS decision."""
        conditions = []
        
        for param_id, score in parameter_scores.items():
            if score.rating in ["weak", "poor", "fail"]:
                for gap in score.gaps:
                    condition = self._gap_to_condition(param_id, gap, score.rating)
                    if condition:
                        conditions.append(condition)
        
        if not data.parameter_b.pse_registered and self.merchant_type == MerchantType.REGULAR:
            conditions.append(Condition(
                condition="Obtain PSE (Electronic System Provider) registration",
                priority="medium",
                timeline_days=60,
                category="compliance"
            ))
        
        return conditions
    
    def _gap_to_condition(
        self,
        param_id: str,
        gap: str,
        rating: str
    ) -> Optional[Condition]:
        """Convert a gap to a condition."""
        priority = "high" if rating == "fail" else "medium" if rating == "poor" else "low"
        
        timeline_map = {
            "A": 14,
            "B": 30,
            "C": 30,
            "D": 14,
            "E": 30,
            "F": 14,
            "G": 30,
            "H": 7,
            "I": 30,
        }
        
        category_map = {
            "A": "documentation",
            "B": "compliance",
            "C": "documentation",
            "D": "documentation",
            "E": "documentation",
            "F": "operational",
            "G": "compliance",
            "H": "operational",
            "I": "operational",
        }
        
        return Condition(
            condition=f"Address: {gap}",
            priority=priority,
            timeline_days=timeline_map.get(param_id, 30),
            category=category_map.get(param_id, "operational")
        )
    
    def generate_recommendations(
        self,
        parameter_scores: Dict[str, ParameterScore],
        data: ResearchData
    ) -> List[Recommendation]:
        """Generate risk treatment recommendations."""
        recommendations = []
        
        for param_id, score in parameter_scores.items():
            if score.rating in ["fair", "weak", "poor", "fail"]:
                for gap in score.gaps[:2]:
                    priority = "high" if score.rating in ["poor", "fail"] else "medium"
                    recommendations.append(Recommendation(
                        recommendation=f"[{score.parameter_name}] {gap}",
                        priority=priority,
                        category="risk_mitigation"
                    ))
        
        return recommendations[:10]
