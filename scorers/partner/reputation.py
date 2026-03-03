"""Parameter F: Reputation & Track Record (10 pts)."""

from typing import List
from ..base import BaseScorer
from ...models.partner_data import PartnerData
from ...models.assessment_result import ParameterScore
from ...config import PARTNER_F_THRESHOLDS


class PartnerParameterFScorer(BaseScorer):
    """Scorer for Parameter F: Reputation & Track Record."""

    parameter_id = "F"
    parameter_name = "Reputation & Track Record"
    max_score = 10

    def score(self, data: PartnerData) -> ParameterScore:
        """Calculate score based on reputation findings."""
        findings = data.parameter_f
        evidence: List[str] = []
        gaps: List[str] = []
        points = 0

        # Market reputation (2 pts)
        if findings.has_market_reputation:
            points += 2
            evidence.append("Has positive market reputation")
        else:
            gaps.append("Market reputation unclear")

        # References (2 pts)
        if findings.references_available:
            points += 1
            evidence.append("Client/partner references available")

            if findings.reference_check_positive:
                points += 1
                evidence.append("Reference checks are positive")
            else:
                gaps.append("Reference checks revealed concerns")
        else:
            gaps.append("No references available")

        # Industry recognition (2 pts)
        if findings.has_industry_recognition:
            points += 2
            evidence.append("Has industry recognition or awards")
        else:
            gaps.append("No industry recognition identified")

        # Media coverage (2 pts)
        if findings.media_coverage_positive and findings.no_negative_news:
            points += 2
            evidence.append("Positive media coverage")
        elif not findings.no_negative_news:
            gaps.append("Negative news coverage identified")
            points += 1  # Partial points if positive coverage exists
        else:
            gaps.append("Limited media presence")

        # Past issues (2 pts)
        if findings.no_past_issues:
            points += 2
            evidence.append("No past partnership failures or issues")
        else:
            gaps.append("Past partnership issues identified")

        # ESG rating (bonus check)
        if findings.esg_rating_positive:
            evidence.append("Positive ESG rating")
        else:
            gaps.append("ESG rating not available or concerns identified")

        final_score = min(points, self.max_score)
        rating = self.get_rating(final_score, PARTNER_F_THRESHOLDS)

        return self.build_score(
            score=final_score,
            rating=rating,
            evidence=evidence,
            gaps=gaps,
            notes=findings.notes
        )
