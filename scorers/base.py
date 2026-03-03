"""Base scorer class for all parameter scorers."""

from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Optional, Any
from ..config import MerchantType, AssessmentType


class BaseScorer(ABC):
    """Abstract base class for parameter scorers."""

    parameter_id: str = ""
    parameter_name: str = ""
    max_score: int = 0
    max_score_regular: int = 0  # For merchant assessments
    max_score_pjp: int = 0      # For merchant assessments

    def __init__(self, merchant_type: Optional[MerchantType] = None):
        self.merchant_type = merchant_type

    @property
    def max_score_for_type(self) -> int:
        """Get max score based on merchant type (for merchant assessments)."""
        if self.merchant_type == MerchantType.REGULAR:
            return self.max_score_regular or self.max_score
        return self.max_score_pjp or self.max_score

    def get_rating(self, score: int, thresholds: Dict[str, Tuple[int, int]]) -> str:
        """Determine rating based on score and thresholds."""
        for rating, (min_val, max_val) in thresholds.items():
            if min_val <= score <= max_val:
                return rating
        return "fail"

    @abstractmethod
    def score(self, data: Any) -> Any:
        """Calculate score for this parameter. Must be implemented by subclasses."""
        pass

    def build_score(
        self,
        score: int,
        rating: str,
        evidence: List[str],
        gaps: List[str],
        notes: str = ""
    ) -> Any:
        """Build a ParameterScore object."""
        from ..models.assessment_result import ParameterScore

        max_score = self.max_score_for_type if self.max_score_regular else self.max_score

        return ParameterScore(
            parameter_id=self.parameter_id,
            parameter_name=self.parameter_name,
            score=score,
            max_score=max_score,
            rating=rating,
            evidence=evidence,
            gaps=gaps,
            notes=notes
        )
