"""Parameter E: Operational Capability (15 pts)."""

from typing import List
from ..base import BaseScorer
from ...models.vendor_data import VendorData
from ...models.assessment_result import ParameterScore
from ...config import VENDOR_E_THRESHOLDS


class VendorParameterEScorer(BaseScorer):
    """Scorer for Parameter E: Operational Capability."""

    parameter_id = "E"
    parameter_name = "Operational Capability"
    max_score = 15

    def score(self, data: VendorData) -> ParameterScore:
        """Calculate score based on operational capability findings."""
        findings = data.parameter_e
        evidence: List[str] = []
        gaps: List[str] = []
        points = 0

        # SLA (4 pts)
        if findings.has_sla:
            points += 2
            uptime = findings.sla_uptime or "defined"
            evidence.append(f"Has SLA with {uptime} uptime")

            if findings.sla_history_good:
                points += 2
                evidence.append("SLA compliance history is good")
            else:
                gaps.append("SLA compliance history concerns")
        else:
            gaps.append("No Service Level Agreement")

        # Support team (3 pts)
        if findings.has_support_team:
            points += 1
            support_hours = findings.support_hours or "defined hours"
            evidence.append(f"Has support team ({support_hours})")

            if findings.support_response_time:
                points += 1
                evidence.append(f"Support response time: {findings.support_response_time}")

            if findings.has_escalation_process:
                points += 1
                evidence.append("Has escalation process")
            else:
                gaps.append("No escalation process")
        else:
            gaps.append("No dedicated support team")

        # Account management (2 pts)
        if findings.has_account_manager:
            points += 2
            evidence.append("Has dedicated account manager")
        else:
            gaps.append("No dedicated account manager")

        # Change management (2 pts)
        if findings.change_management:
            points += 2
            evidence.append("Has change management process")
        else:
            gaps.append("No change management process")

        # Incident management (2 pts)
        if findings.incident_management:
            points += 2
            evidence.append("Has incident management process")
        else:
            gaps.append("No incident management process")

        # Critical service check
        if data.vendor_info.service_criticality == "critical":
            if not findings.support_hours or "24/7" not in findings.support_hours.lower():
                gaps.append("Critical service without 24/7 support recommended")

        final_score = min(points, self.max_score)
        rating = self.get_rating(final_score, VENDOR_E_THRESHOLDS)

        return self.build_score(
            score=final_score,
            rating=rating,
            evidence=evidence,
            gaps=gaps,
            notes=findings.notes
        )
