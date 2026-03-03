"""Partner assessment orchestrator."""

from typing import Dict, List, Optional, Any
from datetime import datetime
from ..models.partner_data import PartnerData
from ..models.assessment_result import (
    AssessmentResult,
    ParameterScore,
    DecisionResult,
    AutoRejectTrigger,
    Condition,
    Recommendation,
)
from ..config import (
    AssessmentType,
    RiskLevel,
    PARTNER_DECISION_BANDS,
    PARTNER_RISK_LEVELS,
    PARTNER_AUTO_REJECT_REASONS,
    ASSESSMENT_TYPE_INFO,
)
from ..scorers.partner import (
    PartnerParameterAScorer,
    PartnerParameterBScorer,
    PartnerParameterCScorer,
    PartnerParameterDScorer,
    PartnerParameterEScorer,
    PartnerParameterFScorer,
    PartnerParameterGScorer,
    PartnerParameterHScorer,
)


class PartnerAssessor:
    """
    Partner assessment orchestrator.

    Coordinates:
    1. Parameter scoring (8 parameters)
    2. Decision making
    3. Auto-reject checks
    4. Result generation
    """

    def __init__(self):
        self._parameter_scores: Dict[str, ParameterScore] = {}
        self._auto_reject_triggers: List[AutoRejectTrigger] = []

    def assess(self, data: PartnerData) -> AssessmentResult:
        """
        Conduct full partner assessment.

        Args:
            data: Partner data from research

        Returns:
            AssessmentResult with all scores and decision
        """
        self._auto_reject_triggers = []

        # Score all parameters
        self._score_all_parameters(data)

        # Check for auto-reject triggers
        self._check_auto_reject_triggers(data)

        # Calculate total score
        total_score = self._calculate_total_score()

        # Make decision
        decision_result = self._make_decision(total_score)

        # Generate insights
        strengths = self._identify_strengths()
        concerns = self._identify_concerns()
        recommendations = self._generate_recommendations()

        # Build classification info
        classification = self._build_classification(data)

        # Build reference URLs
        reference_urls = self._build_reference_urls(data)

        return AssessmentResult(
            merchant_name=data.partner_info.name,
            merchant_type=AssessmentType.PARTNER,
            classification=classification,
            parameter_scores=self._parameter_scores,
            total_score=total_score,
            decision_result=decision_result,
            strengths=strengths,
            concerns=concerns,
            recommendations=recommendations,
            regulatory_gate=None,
            reference_urls=reference_urls,
            assessment_date=datetime.now(),
            framework_version="2.0"
        )

    def _score_all_parameters(self, data: PartnerData) -> None:
        """Score all 8 parameters."""
        scorers = [
            ("A", PartnerParameterAScorer()),
            ("B", PartnerParameterBScorer()),
            ("C", PartnerParameterCScorer()),
            ("D", PartnerParameterDScorer()),
            ("E", PartnerParameterEScorer()),
            ("F", PartnerParameterFScorer()),
            ("G", PartnerParameterGScorer()),
            ("H", PartnerParameterHScorer()),
        ]

        for param_id, scorer in scorers:
            self._parameter_scores[param_id] = scorer.score(data)

    def _calculate_total_score(self) -> int:
        """Calculate total score from parameter scores."""
        total = sum(score.score for score in self._parameter_scores.values())
        return min(max(total, 0), 100)

    def _check_auto_reject_triggers(self, data: PartnerData) -> None:
        """Check for auto-reject triggers."""
        # Sanctioned entity
        if not data.parameter_e.no_regulatory_issues:
            self._auto_reject_triggers.append(
                AutoRejectTrigger(
                    code="SANCTIONED_ENTITY",
                    reason=PARTNER_AUTO_REJECT_REASONS["SANCTIONED_ENTITY"],
                    details="Partner has regulatory issues or sanctions"
                )
            )

        # No business registration
        if not data.parameter_a.has_legal_entity:
            self._auto_reject_triggers.append(
                AutoRejectTrigger(
                    code="NO_REGISTRATION",
                    reason=PARTNER_AUTO_REJECT_REASONS["NO_REGISTRATION"],
                    details="No valid business registration found"
                )
            )

        # Confirmed fraud
        if not data.parameter_f.no_past_issues:
            # This might indicate fraud or serious issues
            pass  # Not auto-reject, but flagged as concern

    def _make_decision(self, total_score: int) -> DecisionResult:
        """Make final decision based on score and triggers."""
        if self._auto_reject_triggers:
            return DecisionResult(
                decision="DECLINE",
                risk_level=RiskLevel.VERY_HIGH,
                total_score=total_score,
                is_auto_rejected=True,
                auto_reject_triggers=self._auto_reject_triggers,
                conditions=[],
                gate_override=False,
                gate_override_reason=""
            )

        if total_score < 40:
            return DecisionResult(
                decision="DECLINE",
                risk_level=RiskLevel.VERY_HIGH,
                total_score=total_score,
                is_auto_rejected=True,
                auto_reject_triggers=[
                    AutoRejectTrigger(
                        code="SCORE_TOO_LOW",
                        reason=PARTNER_AUTO_REJECT_REASONS["SCORE_TOO_LOW"],
                        details=f"Total score {total_score}/100 is below minimum threshold"
                    )
                ],
                conditions=[],
                gate_override=False,
                gate_override_reason=""
            )

        # Get decision from score bands
        decision = self._get_decision_from_score(total_score)
        risk_level = PARTNER_RISK_LEVELS.get(decision, RiskLevel.MEDIUM)

        # Generate conditions for CONDITIONS decision
        conditions = []
        if decision == "CONDITIONS":
            conditions = self._generate_conditions()

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

    def _get_decision_from_score(self, score: int) -> str:
        """Get decision from score using decision bands."""
        for (min_score, max_score), decision in PARTNER_DECISION_BANDS.items():
            if min_score <= score <= max_score:
                return decision
        return "DECLINE"

    def _generate_conditions(self) -> List[Condition]:
        """Generate conditions for CONDITIONS decision."""
        conditions = []

        for param_id, score in self._parameter_scores.items():
            if score.rating in ["weak", "poor", "fair"]:
                for gap in score.gaps[:2]:
                    conditions.append(Condition(
                        condition=f"Address: {gap}",
                        priority="high" if score.rating == "poor" else "medium",
                        timeline_days=30,
                        category="risk_mitigation"
                    ))

        return conditions[:10]

    def _identify_strengths(self) -> List[str]:
        """Identify strengths from high-scoring parameters."""
        strengths = []
        for param_id, score in self._parameter_scores.items():
            if score.rating == "excellent":
                strengths.append(f"{score.parameter_name}: {score.score}/{score.max_score}")
            elif score.rating == "good" and len(strengths) < 5:
                strengths.append(f"{score.parameter_name}: {score.score}/{score.max_score}")
        return strengths

    def _identify_concerns(self) -> List[str]:
        """Identify concerns from low-scoring parameters."""
        concerns = []
        for param_id, score in self._parameter_scores.items():
            if score.rating in ["fail", "poor", "weak"]:
                for gap in score.gaps[:2]:
                    concerns.append(gap)
        return concerns[:10]

    def _generate_recommendations(self) -> List[Recommendation]:
        """Generate risk treatment recommendations."""
        recommendations = []

        for param_id, score in self._parameter_scores.items():
            if score.rating in ["fair", "weak", "poor", "fail"]:
                for gap in score.gaps[:2]:
                    priority = "high" if score.rating in ["poor", "fail"] else "medium"
                    recommendations.append(Recommendation(
                        recommendation=f"[{score.parameter_name}] {gap}",
                        priority=priority,
                        category="risk_mitigation"
                    ))

        return recommendations[:10]

    def _build_classification(self, data: PartnerData) -> Dict[str, Any]:
        """Build classification details."""
        return {
            "assessment_type": "partner",
            "assessment_type_display": ASSESSMENT_TYPE_INFO["partner"]["name"],
            "partnership_type": data.partner_info.partnership_type,
            "industry_sector": data.partner_info.industry_sector or "Not specified",
            "country": data.partner_info.country_of_incorporation,
        }

    def _build_reference_urls(self, data: PartnerData) -> Dict[str, str]:
        """Build reference URLs from input data."""
        urls = {}

        if data.partner_info.website:
            urls["website"] = data.partner_info.website

        return urls
