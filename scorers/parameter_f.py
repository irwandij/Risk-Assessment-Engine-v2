"""Parameter F: Consumer Protection Readiness (10 pts)."""

from typing import List
from .base import BaseScorer
from ..models.research_data import ResearchData
from ..models.assessment_result import ParameterScore
from ..config import MerchantType, PARAMETER_F_THRESHOLDS


class ParameterFScorer(BaseScorer):
    """Scorer for Parameter F: Consumer Protection Readiness."""
    
    parameter_id = "F"
    parameter_name = "Consumer Protection Readiness"
    max_score_regular = 10
    max_score_pjp = 10
    
    def score(self, data: ResearchData) -> ParameterScore:
        """Calculate score based on consumer protection readiness."""
        findings = data.parameter_f
        evidence: List[str] = []
        gaps: List[str] = []
        points = 0
        
        support_channels = 0
        if findings.has_email_support:
            support_channels += 1
            evidence.append("Email support available")
        if findings.has_phone_support:
            support_channels += 1
            evidence.append("Phone support available")
        if findings.has_chat_support:
            support_channels += 1
            evidence.append("Chat support available")
        
        if support_channels == 0:
            gaps.append("No customer support channels found")
        elif support_channels == 1:
            points += 2
            gaps.append("Only one support channel available")
        elif support_channels >= 2:
            points += 4
            evidence.append("Multiple support channels available")
        
        if findings.has_faq:
            points += 1
            evidence.append("FAQ section available")
        
        if findings.has_escalation_path:
            points += 2
            evidence.append("Escalation path defined")
        else:
            gaps.append("No escalation path defined")
        
        if findings.has_sla:
            points += 2
            evidence.append("Support SLA defined")
        else:
            gaps.append("No support SLA defined")
        
        if findings.response_time_hours is not None:
            if findings.response_time_hours <= 24:
                points += 1
                evidence.append(f"Response time: {findings.response_time_hours}h (within 24h)")
            elif findings.response_time_hours <= 72:
                evidence.append(f"Response time: {findings.response_time_hours}h")
        
        final_score = min(points, self.max_score_for_type)
        rating = self.get_rating(final_score, PARAMETER_F_THRESHOLDS)
        
        return self.build_score(
            score=final_score,
            rating=rating,
            evidence=evidence,
            gaps=gaps,
            notes=findings.notes
        )
