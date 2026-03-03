"""Parameter G: Privacy & PDP Readiness (10 pts)."""

from typing import List
from .base import BaseScorer
from ..models.research_data import ResearchData
from ..models.assessment_result import ParameterScore
from ..config import MerchantType, PARAMETER_G_THRESHOLDS


class ParameterGScorer(BaseScorer):
    """Scorer for Parameter G: Privacy & PDP Readiness."""
    
    parameter_id = "G"
    parameter_name = "Privacy & PDP Readiness"
    max_score_regular = 10
    max_score_pjp = 10
    
    def score(self, data: ResearchData) -> ParameterScore:
        """Calculate score based on privacy & PDP readiness."""
        findings = data.parameter_g
        evidence: List[str] = []
        gaps: List[str] = []
        points = 0
        
        if not findings.has_privacy_policy:
            gaps.append("No privacy policy found")
        else:
            points += 3
            evidence.append("Privacy policy exists")
            
            if findings.privacy_policy_url:
                evidence.append(f"Privacy policy URL: {findings.privacy_policy_url}")
        
        if findings.has_data_retention_policy:
            points += 2
            evidence.append("Data retention policy included")
        else:
            gaps.append("Data retention policy missing")
        
        if findings.has_user_rights_section:
            points += 2
            evidence.append("User rights section included (PDP compliance)")
        else:
            gaps.append("User rights section missing (PDP compliance gap)")
        
        if findings.has_dpo_contact:
            points += 1
            evidence.append("DPO/Privacy contact available")
        
        if findings.pdp_compliant:
            points += 2
            evidence.append("Appears PDP Law compliant")
        else:
            gaps.append("PDP compliance concerns")
        
        if findings.policy_date:
            evidence.append(f"Privacy policy last updated: {findings.policy_date}")
        
        final_score = min(points, self.max_score_for_type)
        rating = self.get_rating(final_score, PARAMETER_G_THRESHOLDS)
        
        return self.build_score(
            score=final_score,
            rating=rating,
            evidence=evidence,
            gaps=gaps,
            notes=findings.notes
        )
