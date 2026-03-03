"""Parameter F: BCP/DRP Readiness (15 pts)."""

from typing import List
from ..base import BaseScorer
from ...models.vendor_data import VendorData
from ...models.assessment_result import ParameterScore
from ...config import VENDOR_F_THRESHOLDS


class VendorParameterFScorer(BaseScorer):
    """Scorer for Parameter F: BCP/DRP Readiness."""

    parameter_id = "F"
    parameter_name = "BCP/DRP Readiness"
    max_score = 15
    auto_reject_triggered: bool = False
    auto_reject_reason: str = ""

    def score(self, data: VendorData) -> ParameterScore:
        """Calculate score based on BCP/DRP readiness findings."""
        findings = data.parameter_f
        evidence: List[str] = []
        gaps: List[str] = []
        points = 0
        self.auto_reject_triggered = False
        self.auto_reject_reason = ""

        # BCP (3 pts)
        if findings.has_bcp:
            points += 1
            evidence.append("Has Business Continuity Plan")

            if findings.bcp_documented:
                points += 2
                evidence.append("BCP is documented")
            else:
                gaps.append("BCP not documented")
        else:
            gaps.append("No Business Continuity Plan")

        # DRP (3 pts)
        if findings.has_drp:
            points += 1
            evidence.append("Has Disaster Recovery Plan")

            if findings.drp_documented:
                points += 2
                evidence.append("DRP is documented")
            else:
                gaps.append("DRP not documented")
        else:
            gaps.append("No Disaster Recovery Plan")

        # RTO (2 pts)
        if findings.rto_defined:
            points += 2
            rto = findings.rto_value or "defined"
            evidence.append(f"RTO: {rto}")
        else:
            gaps.append("RTO not defined")

        # RPO (2 pts)
        if findings.rpo_defined:
            points += 2
            rpo = findings.rpo_value or "defined"
            evidence.append(f"RPO: {rpo}")
        else:
            gaps.append("RPO not defined")

        # BCP testing (3 pts)
        if findings.bcp_tested:
            points += 3
            last_test = findings.last_bcp_test or "tested"
            evidence.append(f"BCP tested (last: {last_test})")
        else:
            gaps.append("BCP not tested")

        # Backup site / geo redundancy (2 pts)
        if findings.has_backup_site:
            points += 1
            evidence.append("Has backup/recovery site")

            if findings.geo_redundancy:
                points += 1
                evidence.append("Has geographic redundancy")
            else:
                gaps.append("No geographic redundancy")
        else:
            gaps.append("No backup site")

        # Auto-reject check for critical services without BCP/DRP
        if data.vendor_info.service_criticality in ["critical", "high"]:
            if not findings.has_bcp and not findings.has_drp:
                self.auto_reject_triggered = True
                self.auto_reject_reason = "NO_BCP_DRP"
                gaps.append("CRITICAL: No BCP/DRP for critical/high criticality service")

        final_score = min(points, self.max_score)
        rating = self.get_rating(final_score, VENDOR_F_THRESHOLDS)

        return self.build_score(
            score=final_score,
            rating=rating,
            evidence=evidence,
            gaps=gaps,
            notes=findings.notes
        )
