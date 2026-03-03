"""Section G: Transparency (4 pts max)."""

from typing import List
from ..base import BaseScorer
from ...models.ai_project_data import AIProjectData
from ...models.assessment_result import ParameterScore


class AIParameterGScorer(BaseScorer):
    """
    Scorer for Section G: Transparency.

    Max 4 points (2 points per question).
    """

    parameter_id = "G"
    parameter_name = "Transparency"
    max_score = 4

    def score(self, data: AIProjectData) -> ParameterScore:
        """Evaluate transparency capabilities."""
        findings = data.section_g
        evidence: List[str] = []
        gaps: List[str] = []
        points = 0

        # G1: User notification (2 pts)
        if findings.has_user_notification is True:
            points += 2
            evidence.append("Users/stakeholders informed when interacting with AI")
            if findings.notification_method:
                evidence.append(f"Notification: {findings.notification_method[:100]}")
            if findings.g1_explanation:
                evidence.append(f"Details: {findings.g1_explanation[:100]}")
        else:
            # Check if this is applicable
            if data.section_b.is_external_facing is True:
                gaps.append("External-facing AI should notify users")
            else:
                evidence.append("Internal AI - user notification may not be applicable")

        # G2: Explainability (2 pts)
        if findings.has_explainability is True:
            points += 2
            evidence.append("AI decisions can be explained at business level")
            if findings.explanation_method:
                evidence.append(f"Explanation: {findings.explanation_method[:100]}")
        else:
            gaps.append("AI decisions cannot be explained at business level")

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
