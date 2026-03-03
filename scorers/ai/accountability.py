"""Section D: Accountability & Human Oversight (4 pts max)."""

from typing import List
from ..base import BaseScorer
from ...models.ai_project_data import AIProjectData
from ...models.assessment_result import ParameterScore


class AIParameterDScorer(BaseScorer):
    """
    Scorer for Section D: Accountability & Human Oversight.

    Max 4 points (2 points per question).
    """

    parameter_id = "D"
    parameter_name = "Accountability & Human Oversight"
    max_score = 4

    def score(self, data: AIProjectData) -> ParameterScore:
        """Evaluate accountability and human oversight."""
        findings = data.section_d
        evidence: List[str] = []
        gaps: List[str] = []
        points = 0

        # D1: Named AI system owner (2 pts)
        if findings.has_ai_owner is True:
            points += 2
            owner_name = findings.ai_owner_name or "designated owner"
            evidence.append(f"Named AI system owner: {owner_name}")
            if findings.d1_explanation:
                evidence.append(f"Details: {findings.d1_explanation[:100]}")
        else:
            gaps.append("No named AI system owner designated")

        # D2: Human oversight capability (2 pts)
        if findings.has_human_oversight is True:
            points += 2
            evidence.append("Humans can review, override, or stop AI decisions")
            if findings.override_mechanism:
                evidence.append(f"Override mechanism: {findings.override_mechanism[:100]}")
        else:
            gaps.append("No human override capability defined")

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

        return self.build_score(
            score=points,
            rating=rating,
            evidence=evidence,
            gaps=gaps,
            notes=findings.notes
        )
