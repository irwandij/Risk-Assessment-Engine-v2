"""Parameter D: Operational Capability (15 pts)."""

from typing import List
from ..base import BaseScorer
from ...models.partner_data import PartnerData
from ...models.assessment_result import ParameterScore
from ...config import PARTNER_D_THRESHOLDS


class PartnerParameterDScorer(BaseScorer):
    """Scorer for Parameter D: Operational Capability."""

    parameter_id = "D"
    parameter_name = "Operational Capability"
    max_score = 15

    def score(self, data: PartnerData) -> ParameterScore:
        """Calculate score based on operational capability findings."""
        findings = data.parameter_d
        evidence: List[str] = []
        gaps: List[str] = []
        points = 0

        # Track record (3 pts)
        if findings.has_track_record:
            points += 3
            evidence.append("Proven track record in relevant field")
        else:
            gaps.append("Limited track record in relevant field")

        # Years of experience (2 pts)
        years = findings.years_of_experience
        if years:
            if years >= 10:
                points += 2
                evidence.append(f"Extensive experience ({years} years)")
            elif years >= 5:
                points += 1
                evidence.append(f"Moderate experience ({years} years)")
            else:
                gaps.append(f"Limited experience ({years} years)")

        # Expertise (2 pts)
        if findings.has_expertise:
            points += 2
            evidence.append("Has required expertise and skills")
        else:
            gaps.append("Required expertise not clearly demonstrated")

        # Management team (2 pts)
        if findings.management_team_qualified:
            points += 2
            evidence.append("Qualified management team")
        else:
            gaps.append("Management team qualifications unclear")

        # Resources (2 pts)
        if findings.has_adequate_resources:
            points += 2
            evidence.append("Adequate resources available")
        else:
            gaps.append("Resource adequacy concerns")

        # Processes (2 pts)
        if findings.operational_processes_documented:
            points += 2
            evidence.append("Operational processes documented")
        else:
            gaps.append("Operational processes not documented")

        # Quality certifications (2 pts)
        if findings.quality_certifications:
            points += 2
            evidence.append("Has relevant quality certifications")
        else:
            gaps.append("No relevant quality certifications")

        # Innovation capability (bonus check)
        if findings.innovation_capability:
            evidence.append("Demonstrates innovation capability")

        # Project management (bonus check)
        if findings.project_management_capability:
            evidence.append("Project management capability demonstrated")

        final_score = min(points, self.max_score)
        rating = self.get_rating(final_score, PARTNER_D_THRESHOLDS)

        return self.build_score(
            score=final_score,
            rating=rating,
            evidence=evidence,
            gaps=gaps,
            notes=findings.notes
        )
