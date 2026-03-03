"""Parameter G: Data & Security (10 pts)."""

from typing import List
from ..base import BaseScorer
from ...models.partner_data import PartnerData
from ...models.assessment_result import ParameterScore
from ...config import PARTNER_G_THRESHOLDS


class PartnerParameterGScorer(BaseScorer):
    """Scorer for Parameter G: Data & Security."""

    parameter_id = "G"
    parameter_name = "Data & Security"
    max_score = 10

    def score(self, data: PartnerData) -> ParameterScore:
        """Calculate score based on data and security findings."""
        findings = data.parameter_g
        evidence: List[str] = []
        gaps: List[str] = []
        points = 0

        # Data protection policy (2 pts)
        if findings.has_data_protection_policy:
            points += 2
            evidence.append("Has data protection policy")
        else:
            gaps.append("No data protection policy")

        # Security certifications (2 pts)
        if findings.has_security_certifications:
            points += 2
            evidence.append("Has security certifications (ISO 27001, SOC 2)")
        else:
            gaps.append("No security certifications")

        # Data handling (1 pt)
        if findings.data_handling_documented:
            points += 1
            evidence.append("Data handling procedures documented")
        else:
            gaps.append("Data handling procedures not documented")

        # Encryption (1 pt)
        if findings.encryption_standards:
            points += 1
            evidence.append("Uses encryption standards for data")
        else:
            gaps.append("Encryption standards not confirmed")

        # Access controls (1 pt)
        if findings.access_controls:
            points += 1
            evidence.append("Has proper access controls")
        else:
            gaps.append("Access controls not confirmed")

        # Incident response (1 pt)
        if findings.incident_response_plan:
            points += 1
            evidence.append("Has incident response plan")
        else:
            gaps.append("No incident response plan")

        # Security audits (1 pt)
        if findings.regular_security_audits:
            points += 1
            evidence.append("Conducts regular security audits")
        else:
            gaps.append("No regular security audits")

        # Data breach history (1 pt)
        if findings.no_data_breaches:
            points += 1
            evidence.append("No history of data breaches")
        else:
            gaps.append("History of data breaches identified")

        final_score = min(points, self.max_score)
        rating = self.get_rating(final_score, PARTNER_G_THRESHOLDS)

        return self.build_score(
            score=final_score,
            rating=rating,
            evidence=evidence,
            gaps=gaps,
            notes=findings.notes
        )
