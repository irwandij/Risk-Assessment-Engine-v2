"""Parameter A: Company Identity & Web Verification (15 pts)."""

from typing import List, Tuple
from .base import BaseScorer
from ..models.research_data import ResearchData
from ..models.assessment_result import ParameterScore
from ..config import MerchantType, PARAMETER_A_THRESHOLDS


class ParameterAScorer(BaseScorer):
    """Scorer for Parameter A: Company Identity & Web Verification."""
    
    parameter_id = "A"
    parameter_name = "Company Identity & Web Verification"
    max_score_regular = 15
    max_score_pjp = 15
    
    def score(self, data: ResearchData) -> ParameterScore:
        """Calculate score based on company identity verification."""
        findings = data.parameter_a
        evidence: List[str] = []
        gaps: List[str] = []
        points = 0
        
        if not findings.has_legal_entity:
            gaps.append("No legal entity (PT/CV) information found")
        else:
            points += 3
            entity_type = findings.legal_entity_type or "registered entity"
            evidence.append(f"Legal entity type: {entity_type}")
        
        if not findings.has_address:
            gaps.append("No business address found")
        else:
            points += 2
            evidence.append("Business address available")
            
            if findings.address_verified:
                points += 1
                evidence.append("Address verified (Google Maps/other)")
        
        if not findings.has_phone and not findings.has_email:
            gaps.append("No contact information found")
        else:
            points += 2
            contact_methods = []
            if findings.has_phone:
                contact_methods.append("phone")
            if findings.has_email:
                contact_methods.append("email")
            if findings.has_contact_form:
                contact_methods.append("contact form")
            evidence.append(f"Contact methods: {', '.join(contact_methods)}")
        
        if findings.linkedin_verified:
            points += 2
            evidence.append("LinkedIn profile verified")
        
        if findings.google_maps_verified:
            points += 2
            evidence.append("Google Maps listing verified")
        
        if findings.info_consistent:
            points += 3
            evidence.append("Information consistent across sources")
        elif findings.has_legal_entity:
            gaps.append("Information inconsistencies across sources")
            points += 1
        
        final_score = min(points, self.max_score_for_type)
        rating = self.get_rating(final_score, PARAMETER_A_THRESHOLDS)
        
        if findings.notes:
            notes = findings.notes
        else:
            notes = ""
        
        return self.build_score(
            score=final_score,
            rating=rating,
            evidence=evidence,
            gaps=gaps,
            notes=notes
        )
