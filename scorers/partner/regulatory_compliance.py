"""Parameter E: Regulatory Compliance (15 pts)."""

from typing import List
from ..base import BaseScorer
from ...models.partner_data import PartnerData
from ...models.assessment_result import ParameterScore
from ...config import PARTNER_E_THRESHOLDS


class PartnerParameterEScorer(BaseScorer):
    """Scorer for Parameter E: Regulatory Compliance."""

    parameter_id = "E"
    parameter_name = "Regulatory Compliance"
    max_score = 15

    def score(self, data: PartnerData) -> ParameterScore:
        """Calculate score based on regulatory compliance findings."""
        findings = data.parameter_e
        evidence: List[str] = []
        gaps: List[str] = []
        points = 0

        # Required licenses (4 pts)
        if not findings.has_required_licenses:
            gaps.append("Required licenses not confirmed")
        else:
            points += 2
            evidence.append("Has required licenses for business")

            if findings.licenses_verified:
                points += 2
                evidence.append("Licenses verified with authorities")
            else:
                gaps.append("License verification pending")

        # License validity (2 pts)
        if findings.license_expiry_date:
            # Check if license is valid (not expired)
            evidence.append(f"License expiry: {findings.license_expiry_date}")
            points += 2

        # Regulatory standing (3 pts)
        if findings.no_regulatory_issues:
            points += 3
            evidence.append("No regulatory issues or sanctions")
        else:
            gaps.append("Regulatory issues identified")

        # Compliance program (2 pts)
        if findings.compliance_program_exists:
            points += 2
            evidence.append("Compliance program exists")
        else:
            gaps.append("No formal compliance program")

        # AML/KYC compliance (2 pts)
        if findings.aml_kyc_compliant:
            points += 2
            evidence.append("AML/KYC compliant")
        else:
            gaps.append("AML/KYC compliance unclear")

        # Sanctions screening (2 pts)
        if findings.sanctions_screened:
            points += 2
            evidence.append("Screened against sanctions lists")
        else:
            gaps.append("Sanctions screening not confirmed")

        # Legal issues (bonus check - can reduce score)
        if findings.no_legal_issues:
            evidence.append("No pending legal issues or litigation")
        else:
            gaps.append("Pending legal issues or litigation identified")
            points = max(0, points - 2)  # Penalty for legal issues

        final_score = min(points, self.max_score)
        rating = self.get_rating(final_score, PARTNER_E_THRESHOLDS)

        return self.build_score(
            score=final_score,
            rating=rating,
            evidence=evidence,
            gaps=gaps,
            notes=findings.notes
        )
