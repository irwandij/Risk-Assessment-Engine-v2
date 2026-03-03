"""Parameter I: References & Reputation (5 pts)."""

from typing import List
from ..base import BaseScorer
from ...models.vendor_data import VendorData
from ...models.assessment_result import ParameterScore
from ...config import VENDOR_I_THRESHOLDS


class VendorParameterIScorer(BaseScorer):
    """Scorer for Parameter I: References & Reputation."""

    parameter_id = "I"
    parameter_name = "References & Reputation"
    max_score = 5
    auto_reject_triggered: bool = False
    auto_reject_reason: str = ""

    def score(self, data: VendorData) -> ParameterScore:
        """Calculate score based on references and reputation findings."""
        findings = data.parameter_i
        evidence: List[str] = []
        gaps: List[str] = []
        points = 0
        self.auto_reject_triggered = False
        self.auto_reject_reason = ""

        # References (2 pts)
        if findings.references_available:
            points += 1
            ref_count = findings.reference_count or "several"
            evidence.append(f"References available ({ref_count})")

            if findings.references_verified:
                points += 1
                evidence.append("References verified")
            else:
                gaps.append("References not verified")
        else:
            gaps.append("No references available")

        # Market reputation (1 pt)
        if findings.has_market_reputation:
            points += 1
            evidence.append("Has positive market reputation")
        else:
            gaps.append("Market reputation unclear")

        # Negative news (1 pt)
        if findings.no_negative_news:
            points += 1
            evidence.append("No significant negative news")
        else:
            gaps.append("Negative news coverage identified")

        # Security breaches (1 pt)
        if findings.no_recent_breaches:
            points += 1
            evidence.append("No recent security breaches")
        else:
            # Check if breach was remediated
            if findings.breach_remediated:
                points += 1
                evidence.append("Recent breach properly remediated")
                breach_date = findings.last_breach_date or "recent"
                gaps.append(f"Security breach occurred ({breach_date}) - remediated")
            else:
                gaps.append("Recent security breach without evidence of remediation")
                self.auto_reject_triggered = True
                self.auto_reject_reason = "DATA_BREACH"

        # Industry recognition (bonus check)
        if findings.industry_recognition:
            evidence.append("Has industry recognition")

        final_score = min(points, self.max_score)
        rating = self.get_rating(final_score, VENDOR_I_THRESHOLDS)

        return self.build_score(
            score=final_score,
            rating=rating,
            evidence=evidence,
            gaps=gaps,
            notes=findings.notes
        )
