"""Section E: Reliability & Monitoring (4 pts max)."""

from typing import List
from ..base import BaseScorer
from ...models.ai_project_data import AIProjectData
from ...models.assessment_result import ParameterScore


class AIParameterEScorer(BaseScorer):
    """
    Scorer for Section E: Reliability & Monitoring.

    Max 4 points:
    - E1: Testing (1-2 pts)
    - E2: Fallback process (1 pt)
    - E3: Monitoring plan (1 pt)
    """

    parameter_id = "E"
    parameter_name = "Reliability & Monitoring"
    max_score = 4

    def score(self, data: AIProjectData) -> ParameterScore:
        """Evaluate reliability and monitoring."""
        findings = data.section_e
        evidence: List[str] = []
        gaps: List[str] = []
        points = 0

        # E1: Testing (2 pts)
        if findings.has_testing is True:
            # Check if comprehensive testing
            test_coverage = findings.test_coverage or ""
            if "edge" in test_coverage.lower() or "comprehensive" in test_coverage.lower():
                points += 2
                evidence.append("Comprehensive testing including edge cases")
            else:
                points += 1
                evidence.append("AI tested in normal and edge cases")

            if findings.e1_explanation:
                evidence.append(f"Testing: {findings.e1_explanation[:100]}")
        else:
            gaps.append("AI has not been adequately tested")

        # E2: Fallback process (1 pt)
        if findings.has_fallback is True:
            points += 1
            evidence.append("Fallback/manual process exists if AI fails")
            if findings.fallback_description:
                evidence.append(f"Fallback: {findings.fallback_description[:100]}")
        else:
            gaps.append("No fallback process defined for AI failures")

        # E3: Monitoring plan (1 pt)
        if findings.has_monitoring_plan is True:
            points += 1
            evidence.append("Monitoring plan exists for accuracy, errors, drift")
            if findings.monitoring_metrics:
                evidence.append(f"Metrics: {findings.monitoring_metrics[:100]}")
        else:
            gaps.append("No monitoring plan for AI performance")

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
