"""Parameter B: Financial Stability (15 pts)."""

from typing import List
from ..base import BaseScorer
from ...models.partner_data import PartnerData
from ...models.assessment_result import ParameterScore
from ...config import PARTNER_B_THRESHOLDS


class PartnerParameterBScorer(BaseScorer):
    """Scorer for Parameter B: Financial Stability."""

    parameter_id = "B"
    parameter_name = "Financial Stability"
    max_score = 15

    def score(self, data: PartnerData) -> ParameterScore:
        """Calculate score based on financial stability findings."""
        findings = data.parameter_b
        evidence: List[str] = []
        gaps: List[str] = []
        points = 0

        # Financial statements availability (3 pts)
        if not findings.financial_statements_available:
            gaps.append("No financial statements available")
        else:
            points += 1
            evidence.append("Financial statements available")

            if findings.audited_financials:
                points += 2
                evidence.append("Audited financial statements")
            else:
                gaps.append("Financials not audited")

        # Revenue trend (3 pts)
        if findings.revenue_trend_positive:
            points += 3
            evidence.append("Positive revenue trend over 3 years")
        else:
            gaps.append("Revenue trend not positive")

        # Profitability (3 pts)
        if findings.profitability_trend_positive:
            points += 3
            evidence.append("Positive profitability trend")
        else:
            gaps.append("Profitability concerns identified")

        # Financial ratios (3 pts)
        ratio_points = 0
        if findings.debt_to_equity_healthy:
            ratio_points += 1
            evidence.append("Healthy debt-to-equity ratio")
        else:
            gaps.append("Debt-to-equity ratio concerns")

        if findings.current_ratio_healthy:
            ratio_points += 1
            evidence.append("Healthy current ratio (1.5+)")
        else:
            gaps.append("Current ratio below threshold")

        points += ratio_points

        # Credit rating (3 pts)
        if findings.has_credit_rating:
            rating_value = findings.credit_rating_value or "rated"
            points += 2
            evidence.append(f"Has credit rating: {rating_value}")

            # Investment grade gets full points
            if findings.credit_rating_value and findings.credit_rating_value.startswith(('AAA', 'AA', 'A', 'BBB')):
                points += 1
                evidence.append("Investment grade rating")
        else:
            gaps.append("No credit rating available")

        # Insurance coverage (bonus check)
        if findings.insurance_coverage_adequate:
            evidence.append("Adequate insurance coverage")
        else:
            gaps.append("Insurance coverage may be inadequate")

        final_score = min(points, self.max_score)
        rating = self.get_rating(final_score, PARTNER_B_THRESHOLDS)

        return self.build_score(
            score=final_score,
            rating=rating,
            evidence=evidence,
            gaps=gaps,
            notes=findings.notes
        )
