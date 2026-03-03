"""Merchant type classification logic."""

from typing import Dict, Any
from ..models.research_data import ResearchData
from ..config import MerchantType


class MerchantClassifier:
    """
    Classifies merchant type based on research data.
    
    Classification Logic:
    - IF processes payments for OTHER merchants → PJP/Aggregator
    - IF receives payments for OWN products/services → Regular Merchant
    """
    
    def classify(self, data: ResearchData) -> MerchantType:
        """
        Classify the merchant type from research data.
        
        Args:
            data: Research data containing merchant information
            
        Returns:
            MerchantType enum value
        """
        if self._is_pjp_or_aggregator(data):
            return MerchantType.PJP
        return MerchantType.REGULAR
    
    def _is_pjp_or_aggregator(self, data: ResearchData) -> bool:
        """
        Determine if merchant is PJP/Aggregator.
        
        PJP/Aggregator indicators:
        - Explicitly processes payments for others
        - Is a payment gateway, QRIS acquirer, e-wallet, etc.
        - Claims to be a PJP (Penyedia Jasa Pembayaran)
        """
        if data.merchant_info.processes_payments_for_others:
            return True
        
        if data.parameter_b.is_pjp_or_aggregator:
            return True
        
        business_type_lower = data.merchant_info.business_type.lower()
        pjp_keywords = [
            "payment gateway",
            "payment aggregator",
            "pjp",
            "penyedia jasa pembayaran",
            "qris acquirer",
            "e-wallet",
            "digital wallet",
            "money transfer",
            "remittance",
            "disbursement",
            "payout service",
            "payment processor",
        ]
        
        for keyword in pjp_keywords:
            if keyword in business_type_lower:
                return True
        
        return False
    
    def get_classification_details(self, data: ResearchData) -> Dict[str, Any]:
        """
        Get detailed classification information.
        
        Returns dict with:
        - merchant_type: The classified type
        - business_model: Description of business
        - payment_processing: "Own products" or "On behalf of others"
        - regulatory_requirement: "N/A" or "BI PJP License Required"
        """
        merchant_type = self.classify(data)
        is_pjp = merchant_type == MerchantType.PJP
        
        payment_processing = (
            "On behalf of others" if is_pjp else "Own products/services"
        )
        
        regulatory_requirement = (
            "BI PJP License Required" if is_pjp else "N/A"
        )
        
        return {
            "merchant_type": merchant_type,
            "merchant_type_display": "PJP / Aggregator" if is_pjp else "Regular Merchant",
            "business_model": data.merchant_info.business_type,
            "payment_processing": payment_processing,
            "regulatory_requirement": regulatory_requirement,
            "is_subscription_model": data.merchant_info.subscription_model,
        }
