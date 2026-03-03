"""AI Project assessment orchestrator.

Migrated from Node.js ai-assessment project.
Based on DANA AI Policy framework.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from ..models.ai_project_data import AIProjectData
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
    AI_DECISION_BANDS,
    AI_RISK_LEVELS,
    AI_AUTO_REJECT_REASONS,
    AI_HARD_STOP_SECTIONS,
    ASSESSMENT_TYPE_INFO,
)
from ..scorers.ai import (
    AIParameterAScorer,
    AIParameterBScorer,
    AIParameterCScorer,
    AIParameterDScorer,
    AIParameterEScorer,
    AIParameterFScorer,
    AIParameterGScorer,
)


class AIAssessor:
    """
    AI Project assessment orchestrator.

    Coordinates:
    1. Hard stop checks (Sections A, B, C)
    2. Scoring sections (D, E, F, G) - 16 points max
    3. Risk classification
    4. Result generation
    """

    def __init__(self):
        self._parameter_scores: Dict[str, ParameterScore] = {}
        self._hard_stop_sections: List[str] = []
        self._hard_stop_triggers: List[AutoRejectTrigger] = []

    def assess(self, data: AIProjectData) -> AssessmentResult:
        """
        Conduct full AI project assessment.

        Args:
            data: AI project data from assessment form

        Returns:
            AssessmentResult with all scores and decision
        """
        self._hard_stop_sections = []
        self._hard_stop_triggers = []

        # Score all sections
        self._score_all_sections(data)

        # Check hard stops first
        if self._hard_stop_sections:
            return self._create_stop_result(data)

        # Calculate total score (only D, E, F, G contribute)
        total_score = self._calculate_total_score()

        # Make risk classification
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
            merchant_name=data.project_info.project_name,
            merchant_type=AssessmentType.AI_PROJECT,
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

    def _score_all_sections(self, data: AIProjectData) -> None:
        """Score all 7 sections."""
        # Section A: Privacy & PDP (Hard Stop)
        scorer_a = AIParameterAScorer()
        self._parameter_scores["A"] = scorer_a.score(data)
        if scorer_a.is_hard_stop:
            self._hard_stop_sections.append("Privacy & PDP Compliance")
            self._hard_stop_triggers.append(
                AutoRejectTrigger(
                    code="PRIVACY_HARD_STOP",
                    reason=AI_AUTO_REJECT_REASONS["PRIVACY_HARD_STOP"],
                    details="AI processes personal data without PDPWG approval"
                )
            )

        # Section B: Security (Hard Stop - conditional)
        scorer_b = AIParameterBScorer()
        self._parameter_scores["B"] = scorer_b.score(data)
        if scorer_b.is_hard_stop:
            self._hard_stop_sections.append("Security")
            self._hard_stop_triggers.append(
                AutoRejectTrigger(
                    code="SECURITY_HARD_STOP",
                    reason=AI_AUTO_REJECT_REASONS["SECURITY_HARD_STOP"],
                    details="External-facing AI without IT/Security review"
                )
            )

        # Section C: Value (Hard Stop)
        scorer_c = AIParameterCScorer()
        self._parameter_scores["C"] = scorer_c.score(data)
        if scorer_c.is_hard_stop:
            self._hard_stop_sections.append("Value")
            self._hard_stop_triggers.append(
                AutoRejectTrigger(
                    code="VALUE_HARD_STOP",
                    reason=AI_AUTO_REJECT_REASONS["VALUE_HARD_STOP"],
                    details="No clear business problem or measurable benefit defined"
                )
            )

        # Section D: Accountability (Scoring - 4 pts max)
        scorer_d = AIParameterDScorer()
        self._parameter_scores["D"] = scorer_d.score(data)

        # Section E: Reliability (Scoring - 4 pts max)
        scorer_e = AIParameterEScorer()
        self._parameter_scores["E"] = scorer_e.score(data)

        # Section F: Fairness (Scoring - 4 pts max)
        scorer_f = AIParameterFScorer()
        self._parameter_scores["F"] = scorer_f.score(data)

        # Section G: Transparency (Scoring - 4 pts max)
        scorer_g = AIParameterGScorer()
        self._parameter_scores["G"] = scorer_g.score(data)

    def _calculate_total_score(self) -> int:
        """Calculate total score from scoring sections only (D, E, F, G)."""
        scoring_sections = ["D", "E", "F", "G"]
        total = sum(
            self._parameter_scores[s].score
            for s in scoring_sections
            if s in self._parameter_scores
        )
        return min(max(total, 0), 16)

    def _create_stop_result(self, data: AIProjectData) -> AssessmentResult:
        """Create a STOP result when hard stops are triggered."""
        classification = self._build_classification(data)

        concerns = []
        for section in self._hard_stop_sections:
            concerns.append(f"Hard stop failed: {section}")

        mandatory_actions = (
            f"Cannot proceed to launch. Failed hard stop sections: "
            f"{', '.join(self._hard_stop_sections)}. "
            f"These must be resolved before reassessment."
        )

        # Build reference URLs
        reference_urls = self._build_reference_urls(data)

        return AssessmentResult(
            merchant_name=data.project_info.project_name,
            merchant_type=AssessmentType.AI_PROJECT,
            classification=classification,
            parameter_scores=self._parameter_scores,
            total_score=self._calculate_total_score(),
            decision_result=DecisionResult(
                decision="STOP",
                risk_level=RiskLevel.STOP,
                total_score=self._calculate_total_score(),
                is_auto_rejected=True,
                auto_reject_triggers=self._hard_stop_triggers,
                conditions=[],
                gate_override=False,
                gate_override_reason=", ".join(self._hard_stop_sections)
            ),
            strengths=[],
            concerns=concerns,
            recommendations=[
                Recommendation(
                    recommendation=f"Resolve hard stop: {section}",
                    priority="high",
                    category="compliance"
                )
                for section in self._hard_stop_sections
            ],
            regulatory_gate={"mandatory_actions": mandatory_actions},
            reference_urls=reference_urls,
            assessment_date=datetime.now(),
            framework_version="2.0"
        )

    def _make_decision(self, total_score: int) -> DecisionResult:
        """Make risk classification decision based on score."""
        # Get risk level from score bands
        risk_level_str = self._get_risk_from_score(total_score)
        risk_level = AI_RISK_LEVELS.get(risk_level_str, RiskLevel.MEDIUM)

        # Generate mandatory actions based on risk level
        mandatory_actions = self._get_mandatory_actions(risk_level_str, total_score)

        # Generate conditions for MEDIUM risk
        conditions = []
        if risk_level_str == "MEDIUM":
            conditions = self._generate_conditions()

        return DecisionResult(
            decision=risk_level_str,
            risk_level=risk_level,
            total_score=total_score,
            is_auto_rejected=False,
            auto_reject_triggers=[],
            conditions=conditions,
            gate_override=False,
            gate_override_reason=""
        )

    def _get_risk_from_score(self, score: int) -> str:
        """Get risk level from score using decision bands."""
        for (min_score, max_score), risk_level in AI_DECISION_BANDS.items():
            if min_score <= score <= max_score:
                return risk_level
        return "HIGH"

    def _get_mandatory_actions(self, risk_level: str, total_score: int) -> str:
        """Get mandatory actions based on risk level."""
        if risk_level == "HIGH":
            return "AI Governance Committee approval required before launch."
        elif risk_level == "MEDIUM":
            return "Department review and remediation required."
        else:
            return "Proceed with standard monitoring."

    def _generate_conditions(self) -> List[Condition]:
        """Generate conditions for MEDIUM risk."""
        conditions = []

        for param_id in ["D", "E", "F", "G"]:
            score = self._parameter_scores.get(param_id)
            if score and score.rating in ["weak", "poor", "fair"]:
                for gap in score.gaps[:2]:
                    conditions.append(Condition(
                        condition=f"Address: {gap}",
                        priority="medium",
                        timeline_days=30,
                        category="risk_mitigation"
                    ))

        return conditions[:10]

    def _identify_strengths(self) -> List[str]:
        """Identify strengths from high-scoring sections."""
        strengths = []
        for param_id in ["D", "E", "F", "G"]:
            score = self._parameter_scores.get(param_id)
            if score:
                if score.rating == "excellent":
                    strengths.append(f"{score.parameter_name}: {score.score}/{score.max_score}")
                elif score.rating == "good" and len(strengths) < 3:
                    strengths.append(f"{score.parameter_name}: {score.score}/{score.max_score}")
        return strengths

    def _identify_concerns(self) -> List[str]:
        """Identify concerns from low-scoring sections."""
        concerns = []
        for param_id in ["D", "E", "F", "G"]:
            score = self._parameter_scores.get(param_id)
            if score and score.rating in ["fail", "poor", "weak"]:
                for gap in score.gaps[:2]:
                    concerns.append(gap)
        return concerns[:8]

    def _generate_recommendations(self) -> List[Recommendation]:
        """Generate risk treatment recommendations."""
        recommendations = []

        for param_id in ["D", "E", "F", "G"]:
            score = self._parameter_scores.get(param_id)
            if score and score.rating in ["fair", "weak", "poor", "fail"]:
                for gap in score.gaps[:2]:
                    priority = "high" if score.rating in ["poor", "fail"] else "medium"
                    recommendations.append(Recommendation(
                        recommendation=f"[{score.parameter_name}] {gap}",
                        priority=priority,
                        category="ai_governance"
                    ))

        return recommendations[:8]

    def _build_classification(self, data: AIProjectData) -> Dict[str, Any]:
        """Build classification details."""
        return {
            "assessment_type": "ai_project",
            "assessment_type_display": ASSESSMENT_TYPE_INFO["ai_project"]["name"],
            "project_owner": data.project_info.project_owner,
            "department": data.project_info.department,
            "ai_type": data.project_info.ai_type,
            "is_external_facing": data.project_info.is_external_facing,
            "processes_personal_data": data.project_info.processes_personal_data,
        }

    def _build_reference_urls(self, data: AIProjectData) -> Dict[str, str]:
        """Build reference URLs from input data."""
        # AI project data doesn't have URL fields currently
        # This can be extended if needed in the future
        return {}
