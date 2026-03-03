"""Vendor assessment scorers."""

from .vendor_profile import VendorParameterAScorer
from .financial_health import VendorParameterBScorer
from .security_compliance import VendorParameterCScorer
from .data_protection import VendorParameterDScorer
from .operational_capability import VendorParameterEScorer
from .bcp_drp import VendorParameterFScorer
from .it_infrastructure import VendorParameterGScorer
from .contract_sla import VendorParameterHScorer
from .references_reputation import VendorParameterIScorer

__all__ = [
    "VendorParameterAScorer",
    "VendorParameterBScorer",
    "VendorParameterCScorer",
    "VendorParameterDScorer",
    "VendorParameterEScorer",
    "VendorParameterFScorer",
    "VendorParameterGScorer",
    "VendorParameterHScorer",
    "VendorParameterIScorer",
]
