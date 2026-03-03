"""Parameter H: Contract & SLA (5 pts)."""

from typing import List
from ..base import BaseScorer
from ...models.vendor_data import VendorData
from ...models.assessment_result import ParameterScore
from ...config import VENDOR_H_THRESHOLDS


class VendorParameterHScorer(BaseScorer):
    """Scorer for Parameter H: Contract & SLA."""

    parameter_id = "H"
    parameter_name = "Contract & SLA"
    max_score = 5

    def score(self, data: VendorData) -> ParameterScore:
        """Calculate score based on contract and SLA findings."""
        findings = data.parameter_h
        evidence: List[str] = []
        gaps: List[str] = []
        points = 0

        # Contract terms (1 pt)
        if findings.contract_terms_clear:
            points += 1
            evidence.append("Contract terms are clear")
        else:
            gaps.append("Contract terms need clarification")

        # Liability caps (1 pt)
        if findings.liability_caps_defined:
            points += 1
            evidence.append("Liability caps are defined")
        else:
            gaps.append("Liability caps not defined")

        # Indemnification (1 pt)
        if findings.indemnification_clause:
            points += 1
            evidence.append("Indemnification clause exists")
        else:
            gaps.append("No indemnification clause")

        # Exit clauses (1 pt)
        if findings.exit_clauses_defined:
            points += 1
            evidence.append("Exit/termination clauses defined")
        else:
            gaps.append("Exit/termination clauses not defined")

        # Data return (1 pt)
        if findings.data_return_clause:
            points += 1
            evidence.append("Data return/deletion clause exists")
        else:
            gaps.append("No data return/deletion clause")

        # Audit rights (bonus check)
        if findings.audit_rights:
            evidence.append("Audit rights included")
        else:
            gaps.append("No audit rights")

        # IP ownership (bonus check)
        if findings.ip_ownership_clear:
            evidence.append("IP ownership is clear")
        else:
            gaps.append("IP ownership unclear")

        final_score = min(points, self.max_score)
        rating = self.get_rating(final_score, VENDOR_H_THRESHOLDS)

        return self.build_score(
            score=final_score,
            rating=rating,
            evidence=evidence,
            gaps=gaps,
            notes=findings.notes
        )
