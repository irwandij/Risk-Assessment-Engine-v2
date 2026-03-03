"""Parameter A: Vendor Profile (10 pts)."""

from typing import List
from ..base import BaseScorer
from ...models.vendor_data import VendorData
from ...models.assessment_result import ParameterScore
from ...config import VENDOR_A_THRESHOLDS


class VendorParameterAScorer(BaseScorer):
    """Scorer for Parameter A: Vendor Profile."""

    parameter_id = "A"
    parameter_name = "Vendor Profile"
    max_score = 10

    def score(self, data: VendorData) -> ParameterScore:
        """Calculate score based on vendor profile findings."""
        findings = data.parameter_a
        evidence: List[str] = []
        gaps: List[str] = []
        points = 0

        # Legal entity (2 pts)
        if findings.has_legal_entity:
            points += 1
            evidence.append("Has valid legal entity registration")

            if findings.registration_verified:
                points += 1
                evidence.append("Registration verified")
            else:
                gaps.append("Registration not verified")
        else:
            gaps.append("No valid legal entity registration")

        # Business establishment (2 pts)
        if findings.established_business:
            points += 2
            evidence.append("Established business (3+ years)")
        else:
            gaps.append("Business not established (less than 3 years)")

        # Client base (2 pts)
        if findings.has_client_base:
            points += 1
            client_size = findings.client_base_size or "established client base"
            evidence.append(f"Has {client_size}")

            if findings.serves_similar_companies:
                points += 1
                evidence.append("Serves similar companies/industries")
            else:
                gaps.append("Limited experience with similar companies")
        else:
            gaps.append("Limited client base")

        # Physical presence (2 pts)
        if findings.has_physical_presence:
            points += 1
            evidence.append("Has physical office presence")
        else:
            gaps.append("No physical presence identified")

        if findings.management_team_experienced:
            points += 1
            evidence.append("Experienced management team")
        else:
            gaps.append("Management team experience unclear")

        # Company size indicators (2 pts)
        years = data.vendor_info.years_in_business
        employees = data.vendor_info.number_of_employees

        if years and years >= 5:
            points += 1
            evidence.append(f"Operating for {years} years")
        elif years:
            evidence.append(f"Operating for {years} years")

        if employees and employees >= 50:
            points += 1
            evidence.append(f"Employee count: {employees}")

        final_score = min(points, self.max_score)
        rating = self.get_rating(final_score, VENDOR_A_THRESHOLDS)

        return self.build_score(
            score=final_score,
            rating=rating,
            evidence=evidence,
            gaps=gaps,
            notes=findings.notes
        )
