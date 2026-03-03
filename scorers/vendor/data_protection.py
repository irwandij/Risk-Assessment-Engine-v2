"""Parameter D: Data Protection (15 pts)."""

from typing import List
from ..base import BaseScorer
from ...models.vendor_data import VendorData
from ...models.assessment_result import ParameterScore
from ...config import VENDOR_D_THRESHOLDS


class VendorParameterDScorer(BaseScorer):
    """Scorer for Parameter D: Data Protection."""

    parameter_id = "D"
    parameter_name = "Data Protection"
    max_score = 15

    def score(self, data: VendorData) -> ParameterScore:
        """Calculate score based on data protection findings."""
        findings = data.parameter_d
        evidence: List[str] = []
        gaps: List[str] = []
        points = 0

        # PDP Compliance (3 pts)
        if findings.has_pdp_compliance:
            points += 3
            evidence.append("Compliant with PDP Law requirements")
        else:
            gaps.append("PDP Law compliance not confirmed")

        # Privacy policy (2 pts)
        if findings.has_privacy_policy:
            points += 2
            evidence.append("Has privacy policy")
        else:
            gaps.append("No privacy policy")

        # Data Processing Agreement (2 pts)
        if findings.has_dpa:
            points += 2
            evidence.append("Data Processing Agreement available")
        else:
            gaps.append("No Data Processing Agreement")

        # Data classification (1 pt)
        if findings.data_classification:
            points += 1
            evidence.append("Has data classification scheme")
        else:
            gaps.append("No data classification scheme")

        # Encryption at rest (2 pts)
        if findings.encryption_at_rest:
            points += 2
            evidence.append("Encryption at rest implemented")
        else:
            gaps.append("Encryption at rest not confirmed")

        # Encryption in transit (2 pts)
        if findings.encryption_in_transit:
            points += 2
            evidence.append("Encryption in transit implemented")
        else:
            gaps.append("Encryption in transit not confirmed")

        # Data retention (1 pt)
        if findings.data_retention_policy:
            points += 1
            evidence.append("Has data retention policy")
        else:
            gaps.append("No data retention policy")

        # Data deletion (1 pt)
        if findings.data_deletion_capability:
            points += 1
            evidence.append("Can delete data on request")
        else:
            gaps.append("Data deletion capability not confirmed")

        # Cross-border transfer (1 pt)
        if findings.cross_border_transfer:
            if findings.cross_border_safeguards:
                points += 1
                evidence.append("Cross-border safeguards in place")
            else:
                gaps.append("Cross-border transfer without adequate safeguards")
        else:
            evidence.append("No cross-border data transfer")

        final_score = min(points, self.max_score)
        rating = self.get_rating(final_score, VENDOR_D_THRESHOLDS)

        return self.build_score(
            score=final_score,
            rating=rating,
            evidence=evidence,
            gaps=gaps,
            notes=findings.notes
        )
