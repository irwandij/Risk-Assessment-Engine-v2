"""Parameter C: Security & Compliance (15 pts)."""

from typing import List
from ..base import BaseScorer
from ...models.vendor_data import VendorData
from ...models.assessment_result import ParameterScore
from ...config import VENDOR_C_THRESHOLDS


class VendorParameterCScorer(BaseScorer):
    """Scorer for Parameter C: Security & Compliance."""

    parameter_id = "C"
    parameter_name = "Security & Compliance"
    max_score = 15

    def score(self, data: VendorData) -> ParameterScore:
        """Calculate score based on security and compliance findings."""
        findings = data.parameter_c
        evidence: List[str] = []
        gaps: List[str] = []
        points = 0

        # ISO 27001 (4 pts)
        if findings.has_iso_27001:
            points += 3
            evidence.append("Has ISO 27001 certification")

            if findings.certifications_current:
                points += 1
                evidence.append("Certifications are current")
            else:
                gaps.append("ISO 27001 certification may not be current")
        else:
            gaps.append("No ISO 27001 certification")

        # SOC 2 (3 pts)
        if findings.has_soc2:
            points += 3
            evidence.append("Has SOC 2 Type II certification")
        else:
            gaps.append("No SOC 2 certification")

        # PCI DSS (if applicable) (2 pts)
        if findings.has_pci_dss:
            points += 2
            evidence.append("Has PCI DSS compliance")
        # Not a gap if not applicable

        # Other security certifications (2 pts)
        if findings.has_other_security_certs:
            other = findings.other_certs or "other security certifications"
            points += 2
            evidence.append(f"Has {other}")

        # Penetration testing (2 pts)
        if findings.regular_penetration_testing:
            points += 2
            evidence.append("Conducts regular penetration testing")
        else:
            gaps.append("No regular penetration testing")

        # Vulnerability management (2 pts)
        if findings.vulnerability_management:
            points += 2
            evidence.append("Has vulnerability management program")
        else:
            gaps.append("No vulnerability management program")

        # Security policies (2 pts - bonus check)
        if findings.security_policies_documented:
            evidence.append("Security policies are documented")
        else:
            gaps.append("Security policies not documented")

        # Check for minimum certifications for data-handling vendors
        if data.vendor_info.service_criticality in ["critical", "high"]:
            if not findings.has_iso_27001 and not findings.has_soc2:
                gaps.append("Critical/high criticality vendor without major security certifications")

        final_score = min(points, self.max_score)
        rating = self.get_rating(final_score, VENDOR_C_THRESHOLDS)

        return self.build_score(
            score=final_score,
            rating=rating,
            evidence=evidence,
            gaps=gaps,
            notes=findings.notes
        )
