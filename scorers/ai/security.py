"""Section B: Security (Hard Stop - conditional)."""

from typing import List
from ..base import BaseScorer
from ...models.ai_project_data import AIProjectData
from ...models.assessment_result import ParameterScore


class AIParameterBScorer(BaseScorer):
    """
    Scorer for Section B: Security.

    HARD STOP only if external facing AND not IT reviewed.
    """

    parameter_id = "B"
    parameter_name = "Security"
    max_score = 0  # Hard stop section - no points
    is_hard_stop: bool = False
    hard_stop_reason: str = ""

    def score(self, data: AIProjectData) -> ParameterScore:
        """Evaluate security requirements."""
        findings = data.section_b
        evidence: List[str] = []
        gaps: List[str] = []
        self.is_hard_stop = False
        self.hard_stop_reason = ""

        # Check B1: External facing
        if findings.is_external_facing is True:
            evidence.append("AI is customer/external facing")

            # Check B2: IT Security review
            if findings.it_security_reviewed is True:
                evidence.append("IT/Security has reviewed the system")
                if findings.b2_explanation:
                    evidence.append(f"Review details: {findings.b2_explanation[:100]}")
            else:
                # HARD STOP - external facing without IT review
                self.is_hard_stop = True
                self.hard_stop_reason = "SECURITY_HARD_STOP"
                gaps.append("IT/Security review required for external-facing AI systems")
        else:
            evidence.append("AI is internal-use only")
            if findings.b1_explanation:
                evidence.append(f"Clarification: {findings.b1_explanation[:100]}")

        # Build the score (always 0 for hard stop sections)
        rating = "fail" if self.is_hard_stop else "pass"

        return self.build_score(
            score=0,
            rating=rating,
            evidence=evidence,
            gaps=gaps,
            notes=findings.notes or f"Hard Stop Status: {'FAILED' if self.is_hard_stop else 'PASSED'}"
        )
