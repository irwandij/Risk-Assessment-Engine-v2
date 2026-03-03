"""Parameter C: Strategic Alignment (15 pts)."""

from typing import List
from ..base import BaseScorer
from ...models.partner_data import PartnerData
from ...models.assessment_result import ParameterScore
from ...config import PARTNER_C_THRESHOLDS


class PartnerParameterCScorer(BaseScorer):
    """Scorer for Parameter C: Strategic Alignment."""

    parameter_id = "C"
    parameter_name = "Strategic Alignment"
    max_score = 15

    def score(self, data: PartnerData) -> ParameterScore:
        """Calculate score based on strategic alignment findings."""
        findings = data.parameter_c
        evidence: List[str] = []
        gaps: List[str] = []
        points = 0

        # Business model alignment (3 pts)
        if findings.business_model_aligned:
            points += 3
            evidence.append("Business model aligns with our strategy")
        else:
            gaps.append("Business model alignment unclear")

        # Shared objectives (3 pts)
        if findings.shared_objectives:
            points += 3
            evidence.append("Shared strategic objectives identified")
        else:
            gaps.append("Strategic objectives not clearly aligned")

        # Complementary capabilities (3 pts)
        if findings.complementary_capabilities:
            points += 3
            evidence.append("Capabilities complement each other")
        else:
            gaps.append("Capabilities not clearly complementary")

        # Market position (2 pts)
        if findings.market_position_aligned:
            points += 2
            evidence.append("Market position is compatible")
        else:
            gaps.append("Market position compatibility concerns")

        # Cultural fit (2 pts)
        if findings.cultural_fit:
            points += 2
            evidence.append("Corporate culture is compatible")
        else:
            gaps.append("Cultural fit concerns identified")

        # Long-term commitment (2 pts)
        if findings.long_term_commitment:
            points += 2
            evidence.append("Evidence of long-term commitment")
        else:
            gaps.append("Long-term commitment unclear")

        # Value proposition (bonus check)
        if findings.partnership_value_proposition:
            evidence.append("Clear partnership value proposition")
        else:
            gaps.append("Partnership value proposition not clearly defined")

        final_score = min(points, self.max_score)
        rating = self.get_rating(final_score, PARTNER_C_THRESHOLDS)

        return self.build_score(
            score=final_score,
            rating=rating,
            evidence=evidence,
            gaps=gaps,
            notes=findings.notes
        )
