"""Parameter C: Product/Service Clarity (10 pts)."""

from typing import List
from .base import BaseScorer
from ..models.research_data import ResearchData
from ..models.assessment_result import ParameterScore
from ..config import MerchantType, PARAMETER_C_THRESHOLDS


class ParameterCScorer(BaseScorer):
    """Scorer for Parameter C: Product/Service Clarity."""
    
    parameter_id = "C"
    parameter_name = "Product/Service Clarity"
    max_score_regular = 10
    max_score_pjp = 10
    
    def score(self, data: ResearchData) -> ParameterScore:
        """Calculate score based on product/service clarity."""
        findings = data.parameter_c
        evidence: List[str] = []
        gaps: List[str] = []
        points = 0
        
        if not findings.services_clearly_described:
            gaps.append("Services/products not clearly described")
        else:
            points += 3
            evidence.append("Services/products clearly described")
        
        if findings.has_scope_documentation:
            points += 2
            evidence.append("Scope of services documented")
        else:
            gaps.append("Scope documentation missing or unclear")
        
        if findings.has_deliverables:
            points += 2
            evidence.append("Deliverables clearly defined")
        else:
            gaps.append("Deliverables not clearly defined")
        
        if findings.has_limitations:
            points += 1
            evidence.append("Limitations/exceptions stated")
        
        if not findings.no_misleading_claims:
            gaps.append("Potential misleading claims detected")
            points = max(0, points - 3)
        else:
            evidence.append("No misleading claims identified")
        
        final_score = min(points, self.max_score_for_type)
        rating = self.get_rating(final_score, PARAMETER_C_THRESHOLDS)
        
        return self.build_score(
            score=final_score,
            rating=rating,
            evidence=evidence,
            gaps=gaps,
            notes=findings.notes
        )
