"""Section F: Fairness (4 pts max)."""

from typing import List
from ..base import BaseScorer
from ...models.ai_project_data import AIProjectData
from ...models.assessment_result import ParameterScore


class AIParameterFScorer(BaseScorer):
    """
    Scorer for Section F: Fairness.

    Max 4 points (2 points per question).
    """

    parameter_id = "F"
    parameter_name = "Fairness"
    max_score = 4

    def score(self, data: AIProjectData) -> ParameterScore:
        """Evaluate fairness capabilities."""
        findings = data.section_f
        evidence: List[str] = []
        gaps: List[str] = []
        points = 0

        # F1: Bias checking (2 pts)
        if findings.has_bias_check is True:
            points += 2
            evidence.append("AI checked for unfair bias")
            if findings.bias_check_method:
                evidence.append(f"Bias check: {findings.bias_check_method[:100]}")
            if findings.f1_explanation:
                evidence.append(f"Details: {findings.f1_explanation[:100]}")
        else:
            gaps.append("AI has not been checked for unfair bias")

        # F2: Bias detection and correction (2 pts)
        if findings.can_detect_correct_bias is True:
            points += 2
            evidence.append("Unfair outcomes can be detected and corrected")
            if findings.correction_mechanism:
                evidence.append(f"Correction: {findings.correction_mechanism[:100]}")
        else:
            gaps.append("No mechanism to detect and correct unfair outcomes")

        # Determine rating
        if points >= 4:
            rating = "excellent"
        elif points >= 3:
            rating = "good"
        elif points >= 2:
            rating = "fair"
        elif points >= 1:
            rating = "weak"
        else:
            rating = "fail"

        final_score = min(points, self.max_score)

        return self.build_score(
            score=final_score,
            rating=rating,
            evidence=evidence,
            gaps=gaps,
            notes=findings.notes
        )
