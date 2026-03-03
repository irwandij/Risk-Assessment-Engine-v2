"""Parameter G: IT Infrastructure (10 pts)."""

from typing import List
from ..base import BaseScorer
from ...models.vendor_data import VendorData
from ...models.assessment_result import ParameterScore
from ...config import VENDOR_G_THRESHOLDS


class VendorParameterGScorer(BaseScorer):
    """Scorer for Parameter G: IT Infrastructure."""

    parameter_id = "G"
    parameter_name = "IT Infrastructure"
    max_score = 10

    def score(self, data: VendorData) -> ParameterScore:
        """Calculate score based on IT infrastructure findings."""
        findings = data.parameter_g
        evidence: List[str] = []
        gaps: List[str] = []
        points = 0

        # Infrastructure reliability (2 pts)
        if findings.infrastructure_reliable:
            points += 2
            evidence.append("Infrastructure is reliable")
        else:
            gaps.append("Infrastructure reliability concerns")

        # Uptime track record (2 pts)
        if findings.uptime_track_record:
            points += 2
            evidence.append(f"Historical uptime: {findings.uptime_track_record}")
        else:
            gaps.append("Uptime track record not available")

        # Scalability (1 pt)
        if findings.has_scalability:
            points += 1
            evidence.append("Has scalability capability")
        else:
            gaps.append("Scalability capability unclear")

        # Monitoring (2 pts)
        if findings.monitoring_capability:
            points += 1
            evidence.append("Has monitoring capability")

            if findings.has_status_page:
                points += 1
                evidence.append("Has public status page")
            else:
                gaps.append("No public status page")
        else:
            gaps.append("No monitoring capability")

        # Infrastructure providers (2 pts)
        if findings.uses_reputable_providers:
            points += 2
            providers = findings.infrastructure_providers or "reputable providers"
            evidence.append(f"Uses {providers}")
        else:
            gaps.append("Infrastructure providers unclear")

        # Capacity planning (1 pt)
        if findings.has_capacity_planning:
            points += 1
            evidence.append("Has capacity planning process")
        else:
            gaps.append("No capacity planning process")

        final_score = min(points, self.max_score)
        rating = self.get_rating(final_score, VENDOR_G_THRESHOLDS)

        return self.build_score(
            score=final_score,
            rating=rating,
            evidence=evidence,
            gaps=gaps,
            notes=findings.notes
        )
