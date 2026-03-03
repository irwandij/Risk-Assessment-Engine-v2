"""Section C: Value (Hard Stop)."""

from typing import List
from ..base import BaseScorer
from ...models.ai_project_data import AIProjectData
from ...models.assessment_result import ParameterScore


class AIParameterCScorer(BaseScorer):
    """
    Scorer for Section C: Value.

    HARD STOP if no clear problem OR no measurable benefit.
    """

    parameter_id = "C"
    parameter_name = "Value"
    max_score = 0  # Hard stop section - no points
    is_hard_stop: bool = False
    hard_stop_reason: str = ""

    def score(self, data: AIProjectData) -> ParameterScore:
        """Evaluate value proposition."""
        findings = data.section_c
        evidence: List[str] = []
        gaps: List[str] = []
        self.is_hard_stop = False
        self.hard_stop_reason = ""

        # Check C1: Clear business problem
        if findings.has_clear_problem is True:
            evidence.append("Clear business/operational problem defined")
            if findings.c1_explanation:
                evidence.append(f"Problem: {findings.c1_explanation[:100]}")

            # Check for KPI/KRI
            if findings.kpi_kri_defined is True:
                evidence.append("KPI/KRI defined for measuring success")
        else:
            gaps.append("No clear business or operational problem defined")
            self.is_hard_stop = True

        # Check C2: Measurable benefit
        if findings.has_measurable_benefit is True:
            evidence.append("AI delivers measurable benefit")
            if findings.c2_explanation:
                evidence.append(f"Benefit: {findings.c2_explanation[:100]}")

            # Check value vs cost/risk
            if findings.value_exceeds_cost_risk is True:
                evidence.append("Expected value exceeds total cost and risk")
            elif findings.value_exceeds_cost_risk is False:
                gaps.append("Value may not justify cost and risk")
        else:
            gaps.append("No measurable benefit identified")
            self.is_hard_stop = True

        # Set hard stop reason if either condition failed
        if self.is_hard_stop:
            self.hard_stop_reason = "VALUE_HARD_STOP"

        # Build the score (always 0 for hard stop sections)
        rating = "fail" if self.is_hard_stop else "pass"

        return self.build_score(
            score=0,
            rating=rating,
            evidence=evidence,
            gaps=gaps,
            notes=findings.notes or f"Hard Stop Status: {'FAILED' if self.is_hard_stop else 'PASSED'}"
        )
