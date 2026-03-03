"""Parameter E: T&C Completeness (15 pts Regular, 10 pts PJP)."""

from typing import List
from .base import BaseScorer
from ..models.research_data import ResearchData
from ..models.assessment_result import ParameterScore
from ..config import MerchantType, PARAMETER_E_THRESHOLDS


class ParameterEScorer(BaseScorer):
    """Scorer for Parameter E: T&C Completeness."""
    
    parameter_id = "E"
    parameter_name = "T&C Completeness"
    max_score_regular = 15
    max_score_pjp = 10
    
    def score(self, data: ResearchData) -> ParameterScore:
        """Calculate score based on T&C completeness.
        
        Scoring aligned with framework:
        - Regular (15): 13-15 excellent, 10-12 good, 7-9 fair (basic), 4-6 minimal, 1-3 poor, 0 fail
        - PJP (10): 9-10 excellent, 7-8 good, 5-6 fair, 3-4 minimal, 1-2 poor, 0 fail
        """
        findings = data.parameter_e
        evidence: List[str] = []
        gaps: List[str] = []
        points = 0
        
        merchant_key = "regular" if self.merchant_type == MerchantType.REGULAR else "pjp"
        thresholds = {
            k: v[merchant_key] for k, v in PARAMETER_E_THRESHOLDS.items()
        }
        
        has_any_terms = findings.has_terms_page or findings.tc_accessible
        
        if not findings.has_terms_page:
            gaps.append("No Terms & Conditions page found")
        else:
            points += 4
            evidence.append("Terms & Conditions page exists")
            
            if not findings.tc_accessible:
                gaps.append("T&C page not accessible")
                points -= 2
            else:
                points += 2
                evidence.append("T&C page accessible")
        
        if findings.has_cancellation_policy:
            points += 2
            evidence.append("Cancellation policy included")
        else:
            gaps.append("Cancellation policy missing")
        
        if findings.has_refund_policy:
            points += 2
            evidence.append("Refund policy included")
        else:
            gaps.append("Refund policy missing")
        
        if findings.has_dispute_clause:
            points += 2
            evidence.append("Dispute resolution clause included")
        else:
            gaps.append("Dispute resolution clause missing")
        
        if findings.has_jurisdiction_clause:
            points += 1
            evidence.append("Jurisdiction clause included")
        
        if findings.has_fee_schedule:
            points += 1
            evidence.append("Fee schedule included")
        
        if findings.tc_current:
            points += 1
            evidence.append("T&C appears current")
        else:
            gaps.append("T&C may be outdated")
        
        if self.merchant_type == MerchantType.REGULAR:
            complete_count = sum([
                findings.has_terms_page,
                findings.has_cancellation_policy,
                findings.has_refund_policy,
                findings.has_dispute_clause,
                findings.tc_accessible
            ])
            if complete_count == 5:
                points += 3
                evidence.append("Complete T&C documentation for subscription service")
        
        final_score = min(max(points, 0), self.max_score_for_type)
        rating = self.get_rating(final_score, thresholds)
        
        return self.build_score(
            score=min(max(points, 0), self.max_score_for_type),
            rating=rating,
            evidence=evidence,
            gaps=gaps,
            notes=findings.notes
        )
