"""Main assessment orchestrator."""

from typing import Dict, List, Optional, Any
from datetime import datetime
from ..models.research_data import ResearchData
from ..models.assessment_result import (
    AssessmentResult,
    ParameterScore,
    DecisionResult,
)
from ..config import MerchantType
from .classifier import MerchantClassifier
from .decision import DecisionEngine
from ..scorers import (
    ParameterAScorer,
    ParameterBScorer,
    ParameterCScorer,
    ParameterDScorer,
    ParameterEScorer,
    ParameterFScorer,
    ParameterGScorer,
    ParameterHScorer,
    ParameterIScorer,
)


class Assessor:
    """
    Main assessment orchestrator.
    
    Coordinates:
    1. Merchant type classification
    2. Parameter scoring
    3. Decision making
    4. Result generation
    """
    
    def __init__(self):
        self.classifier = MerchantClassifier()
        self._merchant_type: Optional[MerchantType] = None
        self._parameter_scores: Dict[str, ParameterScore] = {}
        self._regulatory_auto_reject = False
        self._regulatory_auto_reject_reason = ""
    
    def assess(self, data: ResearchData) -> AssessmentResult:
        """
        Conduct full assessment from research data.
        
        Args:
            data: Research data from Phase 1 (LLM research)
            
        Returns:
            AssessmentResult with all scores and decision
        """
        # Reset mutable state for each run to avoid cross-assessment contamination.
        self._parameter_scores = {}
        self._regulatory_auto_reject = False
        self._regulatory_auto_reject_reason = ""
        self._merchant_type = self.classifier.classify(data)
        
        self._score_all_parameters(data)
        
        total_score = self._calculate_total_score()
        
        decision_engine = DecisionEngine(self._merchant_type)
        decision_result = decision_engine.make_decision(
            total_score=total_score,
            parameter_scores=self._parameter_scores,
            data=data,
            regulatory_auto_reject=self._regulatory_auto_reject,
            regulatory_auto_reject_reason=self._regulatory_auto_reject_reason
        )
        
        strengths = self._identify_strengths()
        concerns = self._identify_concerns()
        recommendations = decision_engine.generate_recommendations(
            self._parameter_scores, data
        )
        
        classification = self.classifier.get_classification_details(data)
        
        regulatory_gate = None
        if self._merchant_type == MerchantType.PJP:
            regulatory_gate = self._build_regulatory_gate(data, decision_result)

        # Build reference URLs
        reference_urls = self._build_reference_urls(data)

        return AssessmentResult(
            merchant_name=data.merchant_info.name,
            merchant_type=self._merchant_type,
            classification=classification,
            parameter_scores=self._parameter_scores,
            total_score=total_score,
            decision_result=decision_result,
            strengths=strengths,
            concerns=concerns,
            recommendations=recommendations,
            regulatory_gate=regulatory_gate,
            reference_urls=reference_urls,
            assessment_date=datetime.now(),
            framework_version="2.1"
        )
    
    def _score_all_parameters(self, data: ResearchData) -> None:
        """Score all 9 parameters."""
        scorer_a = ParameterAScorer(self._merchant_type)
        self._parameter_scores["A"] = scorer_a.score(data)
        
        scorer_b = ParameterBScorer(self._merchant_type)
        self._parameter_scores["B"] = scorer_b.score(data)
        
        if scorer_b.auto_reject_triggered:
            self._regulatory_auto_reject = True
            self._regulatory_auto_reject_reason = scorer_b.auto_reject_reason
        
        scorer_c = ParameterCScorer(self._merchant_type)
        self._parameter_scores["C"] = scorer_c.score(data)
        
        scorer_d = ParameterDScorer(self._merchant_type)
        self._parameter_scores["D"] = scorer_d.score(data)
        
        scorer_e = ParameterEScorer(self._merchant_type)
        self._parameter_scores["E"] = scorer_e.score(data)
        
        scorer_f = ParameterFScorer(self._merchant_type)
        self._parameter_scores["F"] = scorer_f.score(data)
        
        scorer_g = ParameterGScorer(self._merchant_type)
        self._parameter_scores["G"] = scorer_g.score(data)
        
        scorer_h = ParameterHScorer(self._merchant_type)
        self._parameter_scores["H"] = scorer_h.score(data)
        
        scorer_i = ParameterIScorer(self._merchant_type)
        self._parameter_scores["I"] = scorer_i.score(data)
    
    def _calculate_total_score(self) -> int:
        """Calculate total score from parameter scores."""
        total = sum(score.score for score in self._parameter_scores.values())
        return min(max(total, 0), 100)
    
    def _identify_strengths(self) -> List[str]:
        """Identify strengths from high-scoring parameters."""
        strengths = []
        for param_id, score in self._parameter_scores.items():
            if score.rating == "excellent":
                strengths.append(f"{score.parameter_name}: {score.score}/{score.max_score}")
            elif score.rating == "good" and len(strengths) < 5:
                strengths.append(f"{score.parameter_name}: {score.score}/{score.max_score}")
        return strengths
    
    def _identify_concerns(self) -> List[str]:
        """Identify concerns from low-scoring parameters."""
        concerns = []
        for param_id, score in self._parameter_scores.items():
            if score.rating in ["fail", "poor", "weak"]:
                for gap in score.gaps[:2]:
                    concerns.append(gap)
        return concerns[:10]
    
    def _build_regulatory_gate(
        self,
        data: ResearchData,
        decision_result: DecisionResult
    ) -> Dict[str, Any]:
        """Build regulatory gate check details for PJP/Aggregators."""
        findings = data.parameter_b
        
        return {
            "regulated_activity": True,
            "required_license": "BI PJP License",
            "license_status": (
                "Verified" if findings.bi_license_verified
                else "Not Verified" if findings.bi_license_number
                else "Not Found"
            ),
            "license_number": findings.bi_license_number,
            "gate_override": decision_result.is_auto_rejected,
            "gate_override_reason": (
                "APPLICABLE - REJECT" if decision_result.is_auto_rejected
                else "NOT APPLICABLE"
            ),
        }

    def _build_reference_urls(self, data: ResearchData) -> Dict[str, str]:
        """Build reference URLs from input data."""
        urls = {}

        if data.merchant_info.website:
            urls["website"] = data.merchant_info.website

        if data.parameter_g.privacy_policy_url:
            urls["privacy_policy"] = data.parameter_g.privacy_policy_url

        if data.parameter_b.bi_registry_url:
            urls["bi_registry"] = data.parameter_b.bi_registry_url

        return urls
