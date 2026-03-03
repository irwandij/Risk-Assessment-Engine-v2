"""Parameter B: Financial Health (10 pts)."""

from typing import List
from ..base import BaseScorer
from ...models.vendor_data import VendorData
from ...models.assessment_result import ParameterScore
from ...config import VENDOR_B_THRESHOLDS


class VendorParameterBScorer(BaseScorer):
    """Scorer for Parameter B: Financial Health."""

    parameter_id = "B"
    parameter_name = "Financial Health"
    max_score = 10

    def score(self, data: VendorData) -> ParameterScore:
        """Calculate score based on financial health findings."""
        findings = data.parameter_b
        evidence: List[str] = []
        gaps: List[str] = []
        points = 0

        # Financial statements (3 pts)
        if findings.financial_statements_available:
            points += 1
            evidence.append("Financial statements available")

            if findings.financial_health_stable:
                points += 2
                evidence.append("Financial health is stable")
            else:
                gaps.append("Financial health concerns identified")
        else:
            gaps.append("Financial statements not available")

        # Revenue stability (2 pts)
        if findings.revenue_stable:
            points += 2
            evidence.append("Revenue is stable/growing")
        else:
            gaps.append("Revenue stability concerns")

        # Insurance coverage (3 pts)
        if findings.has_insurance:
            points += 1
            insurance_type = findings.insurance_type or "liability insurance"
            evidence.append(f"Has {insurance_type}")

            if findings.insurance_coverage_adequate:
                points += 2
                evidence.append("Insurance coverage is adequate")
            else:
                gaps.append("Insurance coverage may be inadequate")
        else:
            gaps.append("No liability insurance")

        # Financial distress check (2 pts)
        if findings.no_financial_distress:
            points += 2
            evidence.append("No signs of financial distress")
        else:
            gaps.append("Signs of financial distress identified")

        final_score = min(points, self.max_score)
        rating = self.get_rating(final_score, VENDOR_B_THRESHOLDS)

        return self.build_score(
            score=final_score,
            rating=rating,
            evidence=evidence,
            gaps=gaps,
            notes=findings.notes
        )
