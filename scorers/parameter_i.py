"""Parameter I: Reputation & Public Footprint (5 pts)."""

from typing import List
from .base import BaseScorer
from ..models.research_data import ResearchData
from ..models.assessment_result import ParameterScore
from ..config import MerchantType, PARAMETER_I_THRESHOLDS


class ParameterIScorer(BaseScorer):
    """Scorer for Parameter I: Reputation & Public Footprint."""
    
    parameter_id = "I"
    parameter_name = "Reputation & Public Footprint"
    max_score_regular = 5
    max_score_pjp = 5
    
    def score(self, data: ResearchData) -> ParameterScore:
        """Calculate score based on reputation and public footprint."""
        findings = data.parameter_i
        evidence: List[str] = []
        gaps: List[str] = []
        points = 0
        
        if findings.regulatory_enforcement:
            gaps.append("CRITICAL: Regulatory enforcement action found")
            return self.build_score(
                score=0,
                rating="fail",
                evidence=["Regulatory enforcement action detected"],
                gaps=gaps,
                notes="Regulatory enforcement - AUTO-REJECT trigger"
            )
        
        if findings.scam_allegations:
            gaps.append("CRITICAL: Scam allegations found")
            points = max(0, points - 3)
        
        footprint_score = sum([
            findings.has_social_media,
            findings.has_linkedin,
            findings.has_google_maps,
            findings.has_press_coverage
        ])
        
        if footprint_score == 0:
            gaps.append("Very limited online footprint")
        elif footprint_score == 1:
            points += 1
            evidence.append("Limited online footprint")
        elif footprint_score == 2:
            points += 2
            evidence.append("Moderate online footprint")
        elif footprint_score >= 3:
            points += 3
            evidence.append("Strong online footprint")
        
        if findings.app_store_rating is not None:
            rating = findings.app_store_rating
            review_count = findings.review_count or 0
            
            if rating >= 4.5:
                points += 2
                evidence.append(f"Excellent app rating: {rating}/5 ({review_count} reviews)")
            elif rating >= 4.0:
                points += 1
                evidence.append(f"Good app rating: {rating}/5 ({review_count} reviews)")
            elif rating < 3.0:
                gaps.append(f"Low app rating: {rating}/5")
                if findings.negative_news:
                    gaps.append("Low rating combined with negative news")
            else:
                evidence.append(f"App rating: {rating}/5")
        
        if findings.positive_news:
            evidence.append(f"Positive coverage: {len(findings.positive_news)} articles")
        
        if findings.negative_news:
            gaps.append(f"Negative news found: {len(findings.negative_news)} articles")
            points = max(0, points - 1)
        
        final_score = min(points, self.max_score_for_type)
        rating = self.get_rating(final_score, PARAMETER_I_THRESHOLDS)
        
        return self.build_score(
            score=final_score,
            rating=rating,
            evidence=evidence,
            gaps=gaps,
            notes=findings.notes
        )
