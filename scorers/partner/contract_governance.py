"""Parameter H: Contract & Governance (5 pts)."""

from typing import List
from ..base import BaseScorer
from ...models.partner_data import PartnerData
from ...models.assessment_result import ParameterScore
from ...config import PARTNER_H_THRESHOLDS


class PartnerParameterHScorer(BaseScorer):
    """Scorer for Parameter H: Contract & Governance."""

    parameter_id = "H"
    parameter_name = "Contract & Governance"
    max_score = 5

    def score(self, data: PartnerData) -> ParameterScore:
        """Calculate score based on contract and governance findings."""
        findings = data.parameter_h
        evidence: List[str] = []
        gaps: List[str] = []
        points = 0

        # Contract availability (1 pt)
        if findings.contract_draft_available:
            points += 1
            evidence.append("Contract draft available for review")
        else:
            gaps.append("Contract draft not available")

        # Clear terms (1 pt)
        if findings.terms_clear:
            points += 1
            evidence.append("Contract terms are clear and fair")
        else:
            gaps.append("Contract terms need clarification")

        # Liability clauses (1 pt)
        if findings.liability_clauses_defined:
            points += 1
            evidence.append("Liability clauses are well-defined")
        else:
            gaps.append("Liability clauses not defined")

        # Exit clauses (1 pt)
        if findings.exit_clauses_defined:
            points += 1
            evidence.append("Exit/termination clauses defined")
        else:
            gaps.append("Exit/termination clauses not defined")

        # Governance structure (1 pt)
        if findings.governance_structure_defined:
            points += 1
            evidence.append("Governance structure defined")
        else:
            gaps.append("Governance structure not defined")

        # IP rights (bonus check)
        if findings.ip_rights_clear:
            evidence.append("Intellectual property rights are clear")
        else:
            gaps.append("IP rights need clarification")

        # Escalation process (bonus check)
        if findings.escalation_process_defined:
            evidence.append("Escalation process defined")
        else:
            gaps.append("Escalation process not defined")

        final_score = min(points, self.max_score)
        rating = self.get_rating(final_score, PARTNER_H_THRESHOLDS)

        return self.build_score(
            score=final_score,
            rating=rating,
            evidence=evidence,
            gaps=gaps,
            notes=findings.notes
        )
