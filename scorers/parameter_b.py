"""Parameter B: Regulatory & Licensing (25 pts) - RULE-BASED.

This is the critical regulatory gate parameter.
For Regular Merchants: AUTO-PASS (25/25)
For PJP/Aggregators: Assessed, and NO LICENSE = AUTO-REJECT
"""

from typing import List
from .base import BaseScorer
from ..models.research_data import ResearchData
from ..models.assessment_result import ParameterScore
from ..config import MerchantType, PARAMETER_B_THRESHOLDS_PJP


class ParameterBScorer(BaseScorer):
    """Scorer for Parameter B: Regulatory & Licensing."""
    
    parameter_id = "B"
    parameter_name = "Regulatory & Licensing"
    max_score_regular = 25
    max_score_pjp = 25
    
    def __init__(self, merchant_type: MerchantType):
        super().__init__(merchant_type)
        self._auto_reject = False
        self._auto_reject_reason = ""
    
    @property
    def auto_reject_triggered(self) -> bool:
        """Check if auto-reject was triggered."""
        return self._auto_reject
    
    @property
    def auto_reject_reason(self) -> str:
        """Get auto-reject reason."""
        return self._auto_reject_reason
    
    def score(self, data: ResearchData) -> ParameterScore:
        """
        Calculate regulatory score.
        
        RULE-BASED LOGIC:
        - Regular Merchant: Always 25/25 (auto-pass)
        - PJP/Aggregator with verified BI license: 23-25
        - PJP/Aggregator with unverified license claim: 8-18
        - PJP/Aggregator with no license: 0 + AUTO-REJECT
        """
        evidence: List[str] = []
        gaps: List[str] = []
        notes = ""
        
        if self.merchant_type == MerchantType.REGULAR:
            return self._score_regular_merchant(data, evidence, gaps)
        else:
            return self._score_pjp_aggregator(data, evidence, gaps)
    
    def _score_regular_merchant(
        self,
        data: ResearchData,
        evidence: List[str],
        gaps: List[str]
    ) -> ParameterScore:
        """Score for Regular Merchant - AUTO-PASS."""
        evidence.append("Regular Merchant - No BI/OJK license required")
        evidence.append("Business model: receives payments for own products/services")
        
        if data.parameter_b.pse_registered:
            evidence.append("PSE registration found")
        else:
            gaps.append("PSE registration not verified (recommended but not required)")
        
        return self.build_score(
            score=25,
            rating="excellent",
            evidence=evidence,
            gaps=gaps,
            notes="AUTO-PASS: Regular Merchant does not require financial services license"
        )
    
    def _score_pjp_aggregator(
        self,
        data: ResearchData,
        evidence: List[str],
        gaps: List[str]
    ) -> ParameterScore:
        """Score for PJP/Aggregator - Assess BI License.
        
        Enhanced logic with BI Registry verification:
        - bi_registry_checked + bi_registry_found = VERIFIED (23-25 pts)
        - bi_registry_checked + NOT found = AUTO-REJECT
        - NOT checked + claimed = PARTIAL (8-18 pts)
        - NOT checked + no claim = AUTO-REJECT
        """
        findings = data.parameter_b
        
        evidence.append("PJP/Aggregator - BI PJP License REQUIRED")
        
        if findings.bi_registry_checked:
            if findings.bi_registry_found:
                return self._score_registry_verified_license(findings, evidence, gaps)
            else:
                return self._score_registry_not_found(findings, evidence, gaps)
        elif findings.bi_license_verified:
            return self._score_verified_license(findings, evidence, gaps)
        elif data.merchant_info.claimed_bi_license or findings.bi_license_number:
            return self._score_claimed_license(findings, data, evidence, gaps)
        else:
            return self._score_no_license(findings, evidence, gaps)
    
    def _score_registry_verified_license(
        self,
        findings,
        evidence: List[str],
        gaps: List[str]
    ) -> ParameterScore:
        """PJP with license VERIFIED in BI registry - highest score."""
        score = 25
        evidence.append(f"BI PJP License VERIFIED in official registry")
        
        if findings.bi_registry_category:
            evidence.append(f"Registry Category: {findings.bi_registry_category}")
        
        if findings.bi_registry_license_number:
            evidence.append(f"License Number: {findings.bi_registry_license_number}")
        
        if findings.bi_registry_decision_number:
            evidence.append(f"Decision Number: {findings.bi_registry_decision_number}")
        
        if findings.bi_registry_date:
            evidence.append(f"License Date: {findings.bi_registry_date}")
        
        if findings.bi_registry_status:
            evidence.append(f"Status: {findings.bi_registry_status}")
            
            if "Dicabut" in findings.bi_registry_status:
                score = 0
                gaps.append("CRITICAL: License has been REVOKED")
                self._auto_reject = True
                self._auto_reject_reason = "LICENSE_REVOKED"
            elif "Belum Operasional" in findings.bi_registry_status:
                score = 20
                gaps.append("License not yet operational")
        
        if findings.bi_registry_url:
            evidence.append(f"Registry URL: {findings.bi_registry_url}")
        
        if findings.license_scope_matches:
            evidence.append("License scope matches business activities")
        elif score > 0:
            score = min(score, 23)
            gaps.append("License scope may not fully match business activities")
        
        rating = self.get_rating(score, PARAMETER_B_THRESHOLDS_PJP)
        
        notes = findings.bi_verification_notes or findings.notes
        
        return self.build_score(
            score=score,
            rating=rating,
            evidence=evidence,
            gaps=gaps,
            notes=notes
        )
    
    def _score_registry_not_found(
        self,
        findings,
        evidence: List[str],
        gaps: List[str]
    ) -> ParameterScore:
        """BI Registry checked but license NOT found - AUTO-REJECT for PJP."""
        self._auto_reject = True
        self._auto_reject_reason = "NO_BI_LICENSE_REGISTRY"
        
        evidence.append("BI License Registry CHECKED - NO MATCH FOUND")
        
        if findings.bi_license_number:
            gaps.append(f"Claimed license {findings.bi_license_number} NOT FOUND in BI registry")
        
        gaps.append("CRITICAL: No valid BI PJP license found in official registry")
        gaps.append("PJP/Aggregator requires valid BI license to operate")
        
        if findings.bi_verification_notes:
            gaps.append(f"Verification notes: {findings.bi_verification_notes[:200]}")
        
        return self.build_score(
            score=0,
            rating="fail",
            evidence=evidence,
            gaps=gaps,
            notes=f"AUTO-REJECT: License not found in BI registry. {findings.bi_verification_notes}"
        )
    
    def _score_verified_license(
        self,
        findings,
        evidence: List[str],
        gaps: List[str]
    ) -> ParameterScore:
        """PJP with verified BI license - highest score."""
        score = 23
        evidence.append(f"BI PJP License VERIFIED: {findings.bi_license_number}")
        
        if findings.license_scope_matches:
            score = 25
            evidence.append("License scope matches business activities")
        else:
            score = 23
            gaps.append("License scope may not fully match business activities")
        
        if findings.ojk_registered:
            evidence.append("OJK registration verified")
        
        rating = self.get_rating(score, PARAMETER_B_THRESHOLDS_PJP)
        
        return self.build_score(
            score=score,
            rating=rating,
            evidence=evidence,
            gaps=gaps,
            notes=findings.notes
        )
    
    def _score_claimed_license(
        self,
        findings,
        data: ResearchData,
        evidence: List[str],
        gaps: List[str]
    ) -> ParameterScore:
        """PJP claims license but not verified - partial score."""
        score = 14
        
        if findings.bi_license_number:
            evidence.append(f"Claims BI License: {findings.bi_license_number}")
            gaps.append("License NOT VERIFIED in official registry")
            score = 14
        else:
            evidence.append("Merchant claims to have BI license")
            gaps.append("No license number provided")
            gaps.append("License NOT VERIFIED in official registry")
            score = 8
        
        rating = self.get_rating(score, PARAMETER_B_THRESHOLDS_PJP)
        
        return self.build_score(
            score=score,
            rating=rating,
            evidence=evidence,
            gaps=gaps,
            notes=findings.notes
        )
    
    def _score_no_license(
        self,
        findings,
        evidence: List[str],
        gaps: List[str]
    ) -> ParameterScore:
        """PJP with no license - AUTO-REJECT."""
        self._auto_reject = True
        self._auto_reject_reason = "NO_BI_LICENSE"
        
        gaps.append("CRITICAL: No BI PJP license found")
        gaps.append("PJP/Aggregator requires BI license to operate")
        
        evidence.append("BI License registry checked - NO MATCH FOUND")
        
        return self.build_score(
            score=0,
            rating="fail",
            evidence=evidence,
            gaps=gaps,
            notes=f"AUTO-REJECT TRIGGERED: {self._auto_reject_reason}"
        )
