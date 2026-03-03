"""Section A: Privacy & PDP Compliance (Hard Stop)."""

from typing import List
from ..base import BaseScorer
from ...models.ai_project_data import AIProjectData
from ...models.assessment_result import ParameterScore


class AIParameterAScorer(BaseScorer):
    """
    Scorer for Section A: Privacy & PDP Compliance.

    This is a HARD STOP section - no points awarded.
    If processes personal data AND not PDPWG approved = STOP.
    """

    parameter_id = "A"
    parameter_name = "Privacy & PDP Compliance"
    max_score = 0  # Hard stop section - no points
    is_hard_stop: bool = False
    hard_stop_reason: str = ""

    def score(self, data: AIProjectData) -> ParameterScore:
        """Evaluate privacy and PDP compliance."""
        findings = data.section_a
        evidence: List[str] = []
        gaps: List[str] = []
        self.is_hard_stop = False
        self.hard_stop_reason = ""

        # Check A1: Processes personal data
        if findings.processes_personal_data is True:
            evidence.append("AI processes personal data (customer, merchant, employee)")

            # Check A2: PDPWG approval
            if findings.pdpwg_approved is True:
                evidence.append("PDPWG has formally approved this AI use")
                if findings.a2_explanation:
                    evidence.append(f"Approval details: {findings.a2_explanation[:100]}")
            else:
                # HARD STOP - processes personal data without approval
                self.is_hard_stop = True
                self.hard_stop_reason = "PRIVACY_HARD_STOP"
                gaps.append("PDPWG approval required for AI processing personal data")
        else:
            evidence.append("AI does not process personal data")
            if findings.a1_explanation:
                evidence.append(f"Clarification: {findings.a1_explanation[:100]}")

        # Build the score (always 0 for hard stop sections)
        rating = "fail" if self.is_hard_stop else "pass"

        return self.build_score(
            score=0,
            rating=rating,
            evidence=evidence,
            gaps=gaps,
            notes=findings.notes or f"Hard Stop Status: {'FAILED' if self.is_hard_stop else 'PASSED'}"
        )
