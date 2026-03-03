"""Parameter D: Payment Transparency (15 pts Regular, 10 pts PJP)."""

from typing import List
from .base import BaseScorer
from ..models.research_data import ResearchData
from ..models.assessment_result import ParameterScore
from ..config import MerchantType, PARAMETER_D_THRESHOLDS


class ParameterDScorer(BaseScorer):
    """Scorer for Parameter D: Payment Transparency."""
    
    parameter_id = "D"
    parameter_name = "Payment Transparency"
    max_score_regular = 15
    max_score_pjp = 10
    
    def score(self, data: ResearchData) -> ParameterScore:
        """Calculate score based on payment transparency.
        
        Scoring aligned with framework:
        - Regular (15): 13-15 excellent, 10-12 good, 7-9 fair, 4-6 minimal, 1-3 poor, 0 fail
        - PJP (10): 9-10 excellent, 7-8 good, 5-6 fair, 3-4 minimal, 1-2 poor, 0 fail
        """
        findings = data.parameter_d
        evidence: List[str] = []
        gaps: List[str] = []
        points = 0
        
        merchant_key = "regular" if self.merchant_type == MerchantType.REGULAR else "pjp"
        thresholds = {
            k: v[merchant_key] for k, v in PARAMETER_D_THRESHOLDS.items()
        }
        
        has_any_info = any([
            findings.has_fee_disclosure,
            findings.has_billing_cycle,
            findings.has_settlement_info,
            findings.pricing_clear
        ])
        
        if has_any_info:
            points += 4
            evidence.append("Some payment/billing information available")
        else:
            points += 4
            gaps.append("Minimal payment transparency - no fees or billing info visible")
        
        if not findings.has_fee_disclosure:
            gaps.append("No fee disclosure found")
        else:
            points += 2
            evidence.append("Fees disclosed")
        
        if findings.has_billing_cycle:
            points += 1
            evidence.append("Billing cycle explained")
        else:
            gaps.append("Billing cycle not explained")
        
        if findings.has_settlement_info:
            points += 1
            evidence.append("Settlement information provided")
        else:
            gaps.append("Settlement information missing")
        
        if not findings.has_refund_policy:
            gaps.append("No refund policy found")
        else:
            points += 2
            evidence.append("Refund policy available")
        
        if findings.has_dispute_process:
            points += 2
            evidence.append("Dispute process defined")
        else:
            gaps.append("Dispute process not defined")
        
        if findings.has_sla:
            points += 1
            evidence.append("Payment SLA provided")
        
        if findings.pricing_clear:
            points += 2
            evidence.append("Pricing is clear and transparent")
        
        if self.merchant_type == MerchantType.REGULAR:
            if findings.has_fee_disclosure and findings.has_refund_policy and findings.pricing_clear:
                points += 2
                evidence.append("Complete payment transparency for subscription model")
        
        final_score = min(points, self.max_score_for_type)
        rating = self.get_rating(final_score, thresholds)
        
        return self.build_score(
            score=min(points, self.max_score_for_type),
            rating=rating,
            evidence=evidence,
            gaps=gaps,
            notes=findings.notes
        )
