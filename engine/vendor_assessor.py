"""Vendor assessment orchestrator."""

from typing import Dict, List, Optional, Any
from datetime import datetime
from ..models.vendor_data import VendorData
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
    VENDOR_DECISION_BANDS,
    VENDOR_RISK_LEVELS,
    VENDOR_AUTO_REJECT_REASONS,
    ASSESSMENT_TYPE_INFO,
)
from ..scorers.vendor import (
    VendorParameterAScorer,
    VendorParameterBScorer,
    VendorParameterCScorer,
    VendorParameterDScorer,
    VendorParameterEScorer,
    VendorParameterFScorer,
    VendorParameterGScorer,
    VendorParameterHScorer,
    VendorParameterIScorer,
)


class VendorAssessor:
    """
    Vendor assessment orchestrator.

    Coordinates:
    1. Parameter scoring (9 parameters)
    2. Decision making
    3. Auto-reject checks
    4. Result generation
    """

    def __init__(self):
        self._parameter_scores: Dict[str, ParameterScore] = {}
        self._auto_reject_triggers: List[AutoRejectTrigger] = []

    def assess(self, data: VendorData) -> AssessmentResult:
        """
        Conduct full vendor assessment.

        Args:
            data: Vendor data from research

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
            merchant_name=data.vendor_info.name,
            merchant_type=AssessmentType.VENDOR,
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

    def _score_all_parameters(self, data: VendorData) -> None:
        """Score all 9 parameters."""
        # Parameter A
        scorer_a = VendorParameterAScorer()
        self._parameter_scores["A"] = scorer_a.score(data)

        # Parameter B
        scorer_b = VendorParameterBScorer()
        self._parameter_scores["B"] = scorer_b.score(data)

        # Parameter C - Security (check for auto-reject)
        scorer_c = VendorParameterCScorer()
        self._parameter_scores["C"] = scorer_c.score(data)

        # Parameter D
        scorer_d = VendorParameterDScorer()
        self._parameter_scores["D"] = scorer_d.score(data)

        # Parameter E
        scorer_e = VendorParameterEScorer()
        self._parameter_scores["E"] = scorer_e.score(data)

        # Parameter F - BCP/DRP (check for auto-reject)
        scorer_f = VendorParameterFScorer()
        self._parameter_scores["F"] = scorer_f.score(data)
        if scorer_f.auto_reject_triggered:
            self._auto_reject_triggers.append(
                AutoRejectTrigger(
                    code=scorer_f.auto_reject_reason,
                    reason=VENDOR_AUTO_REJECT_REASONS.get(
                        scorer_f.auto_reject_reason, "BCP/DRP issue"
                    ),
                    details="Critical/high criticality vendor without BCP/DRP documentation"
                )
            )

        # Parameter G
        scorer_g = VendorParameterGScorer()
        self._parameter_scores["G"] = scorer_g.score(data)

        # Parameter H
        scorer_h = VendorParameterHScorer()
        self._parameter_scores["H"] = scorer_h.score(data)

        # Parameter I - References (check for auto-reject)
        scorer_i = VendorParameterIScorer()
        self._parameter_scores["I"] = scorer_i.score(data)
        if scorer_i.auto_reject_triggered:
            self._auto_reject_triggers.append(
                AutoRejectTrigger(
                    code=scorer_i.auto_reject_reason,
                    reason=VENDOR_AUTO_REJECT_REASONS.get(
                        scorer_i.auto_reject_reason, "Security breach issue"
                    ),
                    details="Data breach in past 12 months without remediation evidence"
                )
            )

    def _calculate_total_score(self) -> int:
        """Calculate total score from parameter scores."""
        total = sum(score.score for score in self._parameter_scores.values())
        return min(max(total, 0), 100)

    def _check_auto_reject_triggers(self, data: VendorData) -> None:
        """Check for auto-reject triggers."""
        # Security certifications check for data-handling vendors
        if data.vendor_info.vendor_type in ["cloud service", "software provider"]:
            if not data.parameter_c.has_iso_27001 and not data.parameter_c.has_soc2:
                self._auto_reject_triggers.append(
                    AutoRejectTrigger(
                        code="NO_SECURITY_CERT",
                        reason=VENDOR_AUTO_REJECT_REASONS["NO_SECURITY_CERT"],
                        details="Data-handling vendor without security certifications"
                    )
                )

    def _make_decision(self, total_score: int) -> DecisionResult:
        """Make final decision based on score and triggers."""
        if self._auto_reject_triggers:
            return DecisionResult(
                decision="REJECT",
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
                decision="REJECT",
                risk_level=RiskLevel.VERY_HIGH,
                total_score=total_score,
                is_auto_rejected=True,
                auto_reject_triggers=[
                    AutoRejectTrigger(
                        code="SCORE_TOO_LOW",
                        reason=VENDOR_AUTO_REJECT_REASONS["SCORE_TOO_LOW"],
                        details=f"Total score {total_score}/100 is below minimum threshold"
                    )
                ],
                conditions=[],
                gate_override=False,
                gate_override_reason=""
            )

        # Get decision from score bands
        decision = self._get_decision_from_score(total_score)
        risk_level = VENDOR_RISK_LEVELS.get(decision, RiskLevel.MEDIUM)

        # Generate conditions for CONDITIONAL decision
        conditions = []
        if decision == "CONDITIONAL":
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
        for (min_score, max_score), decision in VENDOR_DECISION_BANDS.items():
            if min_score <= score <= max_score:
                return decision
        return "REJECT"

    def _generate_conditions(self) -> List[Condition]:
        """Generate conditions for CONDITIONAL decision."""
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

    def _build_classification(self, data: VendorData) -> Dict[str, Any]:
        """Build classification details."""
        return {
            "assessment_type": "vendor",
            "assessment_type_display": ASSESSMENT_TYPE_INFO["vendor"]["name"],
            "vendor_type": data.vendor_info.vendor_type,
            "service_criticality": data.vendor_info.service_criticality,
            "country": data.vendor_info.country_of_operation,
        }

    def _build_reference_urls(self, data: VendorData) -> Dict[str, str]:
        """Build reference URLs from input data."""
        urls = {}

        if data.vendor_info.website:
            urls["website"] = data.vendor_info.website

        if data.parameter_g.has_status_page and data.parameter_g.infrastructure_providers:
            # Note: Could be extended if status page URL is tracked
            pass

        return urls
