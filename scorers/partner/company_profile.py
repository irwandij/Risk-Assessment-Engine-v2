"""Parameter A: Company Profile (15 pts)."""

from typing import List
from ..base import BaseScorer
from ...models.partner_data import PartnerData
from ...models.assessment_result import ParameterScore
from ...config import PARTNER_A_THRESHOLDS


class PartnerParameterAScorer(BaseScorer):
    """Scorer for Parameter A: Company Profile."""

    parameter_id = "A"
    parameter_name = "Company Profile"
    max_score = 15

    def score(self, data: PartnerData) -> ParameterScore:
        """Calculate score based on company profile findings."""
        findings = data.parameter_a
        evidence: List[str] = []
        gaps: List[str] = []
        points = 0

        # Legal entity verification (3 pts)
        if not findings.has_legal_entity:
            gaps.append("No valid legal entity registration found")
        else:
            points += 2
            entity_type = findings.legal_entity_type or "registered entity"
            evidence.append(f"Legal entity type: {entity_type}")

            if findings.registration_verified:
                points += 1
                evidence.append("Registration verified with authorities")

        # Ownership structure (3 pts)
        if findings.ownership_structure_clear:
            points += 2
            evidence.append("Ownership structure is transparent")

            if findings.beneficial_owners_identified:
                points += 1
                evidence.append("Ultimate beneficial owners identified")
            else:
                gaps.append("Ultimate beneficial owners not identified")
        else:
            gaps.append("Ownership structure not transparent")

        # Political exposure check (2 pts - negative if PEP)
        if findings.politically_exposed:
            gaps.append("PEP (Politically Exposed Person) connection identified")
            # Note: PEP doesn't disqualify, but requires enhanced due diligence
            points += 1  # Still gets partial points if disclosed
            evidence.append("PEP connection disclosed (requires enhanced due diligence)")
        else:
            points += 2
            evidence.append("No PEP connections identified")

        # Corporate structure (2 pts)
        if findings.subsidiaries_listed:
            points += 2
            evidence.append("Subsidiaries and affiliates listed")
        else:
            gaps.append("Subsidiaries and affiliates not disclosed")

        # Address verification (2 pts)
        if findings.has_address:
            points += 2
            evidence.append("Physical address available")
        else:
            gaps.append("No physical address found")

        # Business tenure (3 pts)
        years = data.partner_info.years_in_business
        if years:
            if years >= 5:
                points += 3
                evidence.append(f"Established business ({years} years)")
            elif years >= 3:
                points += 2
                evidence.append(f"Business operating for {years} years")
            elif years >= 1:
                points += 1
                evidence.append(f"Relatively new business ({years} years)")
            else:
                gaps.append("Very new business (less than 1 year)")

        final_score = min(points, self.max_score)
        rating = self.get_rating(final_score, PARTNER_A_THRESHOLDS)

        return self.build_score(
            score=final_score,
            rating=rating,
            evidence=evidence,
            gaps=gaps,
            notes=findings.notes
        )
