"""Parameter H: Security Indicators (5 pts)."""

from typing import List
from .base import BaseScorer
from ..models.research_data import ResearchData
from ..models.assessment_result import ParameterScore
from ..config import MerchantType, PARAMETER_H_THRESHOLDS


class ParameterHScorer(BaseScorer):
    """Scorer for Parameter H: Security Indicators."""
    
    parameter_id = "H"
    parameter_name = "Security Indicators"
    max_score_regular = 5
    max_score_pjp = 5
    
    def score(self, data: ResearchData) -> ParameterScore:
        """Calculate score based on security indicators."""
        findings = data.parameter_h
        evidence: List[str] = []
        gaps: List[str] = []
        points = 0
        
        if findings.phishing_indicators:
            gaps.append("CRITICAL: Phishing indicators detected")
            return self.build_score(
                score=1,
                rating="poor",
                evidence=evidence,
                gaps=gaps,
                notes="Phishing indicators detected - requires investigation"
            )
        
        if findings.malware_detected:
            gaps.append("CRITICAL: Malware detected")
            return self.build_score(
                score=0,
                rating="fail",
                evidence=evidence,
                gaps=gaps,
                notes="Malware detected - CRITICAL security issue"
            )
        
        if not findings.has_https:
            gaps.append("Website does not use HTTPS")
        else:
            points += 1
            evidence.append("Website uses HTTPS")
            
            if findings.ssl_valid:
                points += 1
                evidence.append("SSL certificate valid")
            else:
                gaps.append("SSL certificate issues")
        
        if findings.website_stable:
            points += 1
            evidence.append("Website stable and functional")
        else:
            gaps.append("Website stability issues")
        
        if findings.has_secure_login:
            points += 2
            evidence.append("Secure login mechanism present")
        else:
            gaps.append("No secure login mechanism detected")
        
        final_score = min(points, self.max_score_for_type)
        rating = self.get_rating(final_score, PARAMETER_H_THRESHOLDS)
        
        return self.build_score(
            score=final_score,
            rating=rating,
            evidence=evidence,
            gaps=gaps,
            notes=findings.notes
        )
