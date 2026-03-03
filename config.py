"""
Configuration constants for Risk Assessment Engine.
Version: 2.0.0 - Enhanced with Partners, Vendor, and AI Project assessments
"""

from enum import Enum
from typing import Dict, List, Tuple


class AssessmentType(str, Enum):
    """Types of risk assessments supported."""
    MERCHANT = "merchant"
    PARTNER = "partner"
    VENDOR = "vendor"
    AI_PROJECT = "ai_project"


class MerchantType(str, Enum):
    REGULAR = "regular_merchant"
    PJP = "pjp_aggregator"


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    VERY_HIGH = "VERY HIGH"
    STOP = "STOP"  # For AI assessments with hard stops


class Decision(str, Enum):
    PROCEED = "PROCEED"
    PROCEED_WITH_CONDITIONS = "PROCEED WITH CONDITIONS"
    CONDITIONAL_REJECT = "CONDITIONAL REJECT"
    REJECT = "REJECT"
    # Partner/Vendor specific
    APPROVED = "APPROVED"
    CONDITIONAL = "CONDITIONAL"
    REVIEW = "REVIEW"
    ESCALATE = "ESCALATE"
    DECLINE = "DECLINE"
    # AI Project specific
    CONDITIONS = "CONDITIONS"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    STOP = "STOP"


# =============================================================================
# MERCHANT ASSESSMENT CONFIGURATION
# =============================================================================

DECISION_BANDS = {
    (80, 100): Decision.PROCEED,
    (60, 79): Decision.PROCEED_WITH_CONDITIONS,
    (40, 59): Decision.CONDITIONAL_REJECT,
    (0, 39): Decision.REJECT,
}

DECISION_RISK_LEVELS = {
    Decision.PROCEED: RiskLevel.LOW,
    Decision.PROCEED_WITH_CONDITIONS: RiskLevel.MEDIUM,
    Decision.CONDITIONAL_REJECT: RiskLevel.HIGH,
    Decision.REJECT: RiskLevel.VERY_HIGH,
}

MAX_SCORES = {
    "A": 15,
    "B": 25,
    "C": 10,
    "D": {"regular": 15, "pjp": 10},
    "E": {"regular": 15, "pjp": 10},
    "F": 10,
    "G": 10,
    "H": 5,
    "I": 5,
}

WEIGHTS_REGULAR: Dict[str, float] = {
    "A": 0.15,
    "B": 0.25,
    "C": 0.10,
    "D": 0.15,
    "E": 0.15,
    "F": 0.10,
    "G": 0.10,
    "H": 0.05,
    "I": 0.05,
}

WEIGHTS_PJP: Dict[str, float] = {
    "A": 0.15,
    "B": 0.25,
    "C": 0.10,
    "D": 0.10,
    "E": 0.10,
    "F": 0.10,
    "G": 0.10,
    "H": 0.05,
    "I": 0.05,
}

AUTO_REJECT_REASONS = {
    "NO_BI_LICENSE": "PJP/Aggregator without verifiable BI license",
    "NO_ONLINE_PRESENCE": "No functioning website and no social media presence",
    "CONFIRMED_FRAUD": "Confirmed fraud/scam evidence or regulatory enforcement",
    "LOW_APP_RATING": "App rating below 3.0 with serious negative news",
    "NON_SUBSCRIPTION_MODEL": "Non-subscription business model for autodebit application",
    "SCORE_TOO_LOW": "Total score below 40",
}

# Merchant Parameter Thresholds
PARAMETER_A_THRESHOLDS = {
    "excellent": (13, 15),
    "good": (10, 12),
    "fair": (7, 9),
    "weak": (4, 6),
    "poor": (1, 3),
    "fail": (0, 0),
}

PARAMETER_B_THRESHOLDS_PJP = {
    "excellent": (23, 25),
    "good": (19, 22),
    "partial": (14, 18),
    "unverified": (8, 13),
    "likely_none": (3, 7),
    "fail": (0, 0),
}

PARAMETER_C_THRESHOLDS = {
    "excellent": (9, 10),
    "good": (7, 8),
    "fair": (5, 6),
    "weak": (3, 4),
    "poor": (1, 2),
    "fail": (0, 0),
}

PARAMETER_D_THRESHOLDS = {
    "excellent": {"regular": (13, 15), "pjp": (9, 10)},
    "good": {"regular": (10, 12), "pjp": (7, 8)},
    "fair": {"regular": (7, 9), "pjp": (5, 6)},
    "weak": {"regular": (4, 6), "pjp": (3, 4)},
    "poor": {"regular": (1, 3), "pjp": (1, 2)},
    "fail": {"regular": (0, 0), "pjp": (0, 0)},
}

PARAMETER_E_THRESHOLDS = {
    "excellent": {"regular": (13, 15), "pjp": (9, 10)},
    "good": {"regular": (10, 12), "pjp": (7, 8)},
    "fair": {"regular": (7, 9), "pjp": (5, 6)},
    "weak": {"regular": (4, 6), "pjp": (3, 4)},
    "poor": {"regular": (1, 3), "pjp": (1, 2)},
    "fail": {"regular": (0, 0), "pjp": (0, 0)},
}

PARAMETER_F_THRESHOLDS = {
    "excellent": (9, 10),
    "good": (7, 8),
    "fair": (5, 6),
    "weak": (3, 4),
    "poor": (1, 2),
    "fail": (0, 0),
}

PARAMETER_G_THRESHOLDS = {
    "excellent": (9, 10),
    "good": (7, 8),
    "fair": (5, 6),
    "weak": (3, 4),
    "poor": (1, 2),
    "fail": (0, 0),
}

PARAMETER_H_THRESHOLDS = {
    "excellent": (5, 5),
    "good": (4, 4),
    "fair": (3, 3),
    "weak": (2, 2),
    "poor": (1, 1),
    "fail": (0, 0),
}

PARAMETER_I_THRESHOLDS = {
    "excellent": (5, 5),
    "good": (4, 4),
    "fair": (3, 3),
    "weak": (2, 2),
    "poor": (1, 1),
    "fail": (0, 0),
}


# =============================================================================
# PARTNER ASSESSMENT CONFIGURATION
# =============================================================================

PARTNER_DECISION_BANDS: Dict[Tuple[int, int], str] = {
    (80, 100): "PROCEED",
    (60, 79): "CONDITIONS",
    (40, 59): "REVIEW",
    (0, 39): "DECLINE",
}

PARTNER_RISK_LEVELS: Dict[str, RiskLevel] = {
    "PROCEED": RiskLevel.LOW,
    "CONDITIONS": RiskLevel.MEDIUM,
    "REVIEW": RiskLevel.HIGH,
    "DECLINE": RiskLevel.VERY_HIGH,
}

PARTNER_MAX_SCORES: Dict[str, int] = {
    "A": 15,  # Company Profile
    "B": 15,  # Financial Stability
    "C": 15,  # Strategic Alignment
    "D": 15,  # Operational Capability
    "E": 15,  # Regulatory Compliance
    "F": 10,  # Reputation & Track Record
    "G": 10,  # Data & Security
    "H": 5,   # Contract & Governance
}

PARTNER_AUTO_REJECT_REASONS: Dict[str, str] = {
    "SANCTIONED_ENTITY": "Partner is a sanctioned entity or legally prohibited",
    "CONFIRMED_FRAUD": "Confirmed fraud or criminal activity",
    "NO_REGISTRATION": "No valid business registration found",
    "SCORE_TOO_LOW": "Total score below 40",
}

# Partner Parameter Thresholds
PARTNER_A_THRESHOLDS = {
    "excellent": (13, 15),
    "good": (10, 12),
    "fair": (7, 9),
    "weak": (4, 6),
    "poor": (1, 3),
    "fail": (0, 0),
}

PARTNER_B_THRESHOLDS = {
    "excellent": (13, 15),
    "good": (10, 12),
    "fair": (7, 9),
    "weak": (4, 6),
    "poor": (1, 3),
    "fail": (0, 0),
}

PARTNER_C_THRESHOLDS = {
    "excellent": (13, 15),
    "good": (10, 12),
    "fair": (7, 9),
    "weak": (4, 6),
    "poor": (1, 3),
    "fail": (0, 0),
}

PARTNER_D_THRESHOLDS = {
    "excellent": (13, 15),
    "good": (10, 12),
    "fair": (7, 9),
    "weak": (4, 6),
    "poor": (1, 3),
    "fail": (0, 0),
}

PARTNER_E_THRESHOLDS = {
    "excellent": (13, 15),
    "good": (10, 12),
    "fair": (7, 9),
    "weak": (4, 6),
    "poor": (1, 3),
    "fail": (0, 0),
}

PARTNER_F_THRESHOLDS = {
    "excellent": (9, 10),
    "good": (7, 8),
    "fair": (5, 6),
    "weak": (3, 4),
    "poor": (1, 2),
    "fail": (0, 0),
}

PARTNER_G_THRESHOLDS = {
    "excellent": (9, 10),
    "good": (7, 8),
    "fair": (5, 6),
    "weak": (3, 4),
    "poor": (1, 2),
    "fail": (0, 0),
}

PARTNER_H_THRESHOLDS = {
    "excellent": (5, 5),
    "good": (4, 4),
    "fair": (3, 3),
    "weak": (2, 2),
    "poor": (1, 1),
    "fail": (0, 0),
}


# =============================================================================
# VENDOR ASSESSMENT CONFIGURATION
# =============================================================================

VENDOR_DECISION_BANDS: Dict[Tuple[int, int], str] = {
    (80, 100): "APPROVED",
    (60, 79): "CONDITIONAL",
    (40, 59): "ESCALATE",
    (0, 39): "REJECT",
}

VENDOR_RISK_LEVELS: Dict[str, RiskLevel] = {
    "APPROVED": RiskLevel.LOW,
    "CONDITIONAL": RiskLevel.MEDIUM,
    "ESCALATE": RiskLevel.HIGH,
    "REJECT": RiskLevel.VERY_HIGH,
}

VENDOR_MAX_SCORES: Dict[str, int] = {
    "A": 10,  # Vendor Profile
    "B": 10,  # Financial Health
    "C": 15,  # Security & Compliance
    "D": 15,  # Data Protection
    "E": 15,  # Operational Capability
    "F": 15,  # BCP/DRP Readiness
    "G": 10,  # IT Infrastructure
    "H": 5,   # Contract & SLA
    "I": 5,   # References & Reputation
}

VENDOR_AUTO_REJECT_REASONS: Dict[str, str] = {
    "NO_BCP_DRP": "No BCP/DRP documentation for critical services",
    "DATA_BREACH": "Data breach in past 12 months without remediation evidence",
    "NO_SECURITY_CERT": "No security certifications for data-handling services",
    "SANCTIONED_ENTITY": "Vendor is a sanctioned entity",
    "SCORE_TOO_LOW": "Total score below 40",
}

# Vendor Parameter Thresholds
VENDOR_A_THRESHOLDS = {
    "excellent": (9, 10),
    "good": (7, 8),
    "fair": (5, 6),
    "weak": (3, 4),
    "poor": (1, 2),
    "fail": (0, 0),
}

VENDOR_B_THRESHOLDS = {
    "excellent": (9, 10),
    "good": (7, 8),
    "fair": (5, 6),
    "weak": (3, 4),
    "poor": (1, 2),
    "fail": (0, 0),
}

VENDOR_C_THRESHOLDS = {
    "excellent": (13, 15),
    "good": (10, 12),
    "fair": (7, 9),
    "weak": (4, 6),
    "poor": (1, 3),
    "fail": (0, 0),
}

VENDOR_D_THRESHOLDS = {
    "excellent": (13, 15),
    "good": (10, 12),
    "fair": (7, 9),
    "weak": (4, 6),
    "poor": (1, 3),
    "fail": (0, 0),
}

VENDOR_E_THRESHOLDS = {
    "excellent": (13, 15),
    "good": (10, 12),
    "fair": (7, 9),
    "weak": (4, 6),
    "poor": (1, 3),
    "fail": (0, 0),
}

VENDOR_F_THRESHOLDS = {
    "excellent": (13, 15),
    "good": (10, 12),
    "fair": (7, 9),
    "weak": (4, 6),
    "poor": (1, 3),
    "fail": (0, 0),
}

VENDOR_G_THRESHOLDS = {
    "excellent": (9, 10),
    "good": (7, 8),
    "fair": (5, 6),
    "weak": (3, 4),
    "poor": (1, 2),
    "fail": (0, 0),
}

VENDOR_H_THRESHOLDS = {
    "excellent": (5, 5),
    "good": (4, 4),
    "fair": (3, 3),
    "weak": (2, 2),
    "poor": (1, 1),
    "fail": (0, 0),
}

VENDOR_I_THRESHOLDS = {
    "excellent": (5, 5),
    "good": (4, 4),
    "fair": (3, 3),
    "weak": (2, 2),
    "poor": (1, 1),
    "fail": (0, 0),
}


# =============================================================================
# AI PROJECT ASSESSMENT CONFIGURATION
# =============================================================================

AI_DECISION_BANDS: Dict[Tuple[int, int], str] = {
    (14, 16): "LOW",
    (10, 13): "MEDIUM",
    (0, 9): "HIGH",
}

AI_RISK_LEVELS: Dict[str, RiskLevel] = {
    "LOW": RiskLevel.LOW,
    "MEDIUM": RiskLevel.MEDIUM,
    "HIGH": RiskLevel.HIGH,
    "STOP": RiskLevel.STOP,
}

# AI Assessment max score is 16 (4 sections x 4 points each)
AI_MAX_SCORES: Dict[str, int] = {
    "A": 0,  # Hard stop section - no points
    "B": 0,  # Hard stop section - no points
    "C": 0,  # Hard stop section - no points
    "D": 4,  # Accountability
    "E": 4,  # Reliability
    "F": 4,  # Fairness
    "G": 4,  # Transparency
}

# AI Hard Stop Sections
AI_HARD_STOP_SECTIONS = ["A", "B", "C"]

AI_AUTO_REJECT_REASONS: Dict[str, str] = {
    "PRIVACY_HARD_STOP": "PDPWG approval required for personal data processing",
    "SECURITY_HARD_STOP": "IT Security review required for external-facing systems",
    "VALUE_HARD_STOP": "Clear business problem and measurable benefit required",
}


# =============================================================================
# ASSESSMENT TYPE METADATA
# =============================================================================

ASSESSMENT_TYPE_INFO: Dict[str, Dict[str, any]] = {
    "merchant": {
        "name": "Merchant Risk Assessment",
        "description": "Assessment for merchants accepting recurring payments",
        "max_total_score": 100,
        "parameters": {
            "A": "Company Identity & Web Verification",
            "B": "Regulatory & Licensing",
            "C": "Product/Service Clarity",
            "D": "Payment Transparency",
            "E": "T&C Completeness",
            "F": "Consumer Protection Readiness",
            "G": "Privacy & PDP Readiness",
            "H": "Security Indicators",
            "I": "Reputation & Public Footprint",
        }
    },
    "partner": {
        "name": "Partners Assessment",
        "description": "Assessment for business partners and strategic alliances",
        "max_total_score": 100,
        "parameters": {
            "A": "Company Profile",
            "B": "Financial Stability",
            "C": "Strategic Alignment",
            "D": "Operational Capability",
            "E": "Regulatory Compliance",
            "F": "Reputation & Track Record",
            "G": "Data & Security",
            "H": "Contract & Governance",
        }
    },
    "vendor": {
        "name": "Third-party Vendor Assessment",
        "description": "Assessment for vendors, suppliers, and service providers",
        "max_total_score": 100,
        "parameters": {
            "A": "Vendor Profile",
            "B": "Financial Health",
            "C": "Security & Compliance",
            "D": "Data Protection",
            "E": "Operational Capability",
            "F": "BCP/DRP Readiness",
            "G": "IT Infrastructure",
            "H": "Contract & SLA",
            "I": "References & Reputation",
        }
    },
    "ai_project": {
        "name": "AI Project Assessment",
        "description": "Assessment for AI/ML initiatives aligned with DANA AI Policy",
        "max_total_score": 16,
        "parameters": {
            "A": "Privacy & PDP Compliance",
            "B": "Security",
            "C": "Value",
            "D": "Accountability & Human Oversight",
            "E": "Reliability & Monitoring",
            "F": "Fairness",
            "G": "Transparency",
        }
    }
}


# =============================================================================
# DECISION BAND DESCRIPTIONS (for report generation)
# =============================================================================

DECISION_BAND_DESCRIPTIONS: Dict[str, Dict[str, Dict[str, str]]] = {
    "merchant": {
        "PROCEED": {
            "score_range": "80-100",
            "description": "The merchant demonstrates strong compliance and operational readiness. All key parameters meet or exceed requirements with minimal concerns.",
            "implications": "Standard onboarding with normal monitoring. No special conditions required."
        },
        "PROCEED WITH CONDITIONS": {
            "score_range": "60-79",
            "description": "The merchant shows acceptable compliance but has areas requiring attention. Some parameters show moderate gaps that should be addressed.",
            "implications": "Onboarding allowed with enhanced monitoring. Specific conditions must be fulfilled within defined timelines."
        },
        "CONDITIONAL REJECT": {
            "score_range": "40-59",
            "description": "Significant compliance gaps exist that present material risk. Multiple parameters show weak or poor ratings.",
            "implications": "Requires senior management review. Business justification and mitigation plan required before reconsideration."
        },
        "REJECT": {
            "score_range": "0-39",
            "description": "Severe compliance deficiencies or auto-reject triggers identified. The merchant poses unacceptable risk.",
            "implications": "Onboarding not recommended. Reassessment possible only after fundamental issues are resolved."
        }
    },
    "partner": {
        "PROCEED": {
            "score_range": "80-100",
            "description": "The partner demonstrates excellent alignment with partnership criteria. Strong financial, operational, and compliance standing.",
            "implications": "Partnership can proceed with standard governance and monitoring."
        },
        "CONDITIONS": {
            "score_range": "60-79",
            "description": "The partner is generally suitable but has areas requiring attention before or during partnership.",
            "implications": "Partnership allowed with specific conditions that must be addressed within agreed timelines."
        },
        "REVIEW": {
            "score_range": "40-59",
            "description": "Material concerns exist regarding strategic fit, financial stability, or compliance posture.",
            "implications": "Requires detailed senior review and business case before proceeding."
        },
        "DECLINE": {
            "score_range": "0-39",
            "description": "The partner does not meet minimum requirements or auto-reject triggers were activated.",
            "implications": "Partnership not recommended at this time."
        }
    },
    "vendor": {
        "APPROVED": {
            "score_range": "80-100",
            "description": "The vendor meets all security, operational, and compliance requirements. Strong track record and adequate controls.",
            "implications": "Vendor can be engaged with standard contract terms and normal oversight."
        },
        "CONDITIONAL": {
            "score_range": "60-79",
            "description": "The vendor is generally acceptable but has areas requiring enhanced controls or conditions.",
            "implications": "Vendor engagement allowed with specific conditions and enhanced monitoring."
        },
        "ESCALATE": {
            "score_range": "40-59",
            "description": "Significant concerns in security, data protection, or operational capability require senior review.",
            "implications": "Requires escalation to senior management for risk acceptance decision."
        },
        "REJECT": {
            "score_range": "0-39",
            "description": "The vendor fails to meet minimum security or compliance requirements. Critical risks identified.",
            "implications": "Vendor engagement not recommended."
        }
    },
    "ai_project": {
        "LOW": {
            "score_range": "14-16",
            "description": "The AI project demonstrates strong governance, clear value, and adequate risk controls across all ethical AI principles.",
            "implications": "Project can proceed to launch with standard monitoring."
        },
        "MEDIUM": {
            "score_range": "10-13",
            "description": "The AI project is generally sound but has areas requiring attention under AI governance principles.",
            "implications": "Department review required. Specific conditions must be addressed before or during deployment."
        },
        "HIGH": {
            "score_range": "0-9",
            "description": "Significant gaps in AI governance, ethical principles, or risk controls identified.",
            "implications": "AI Governance Committee approval required before launch."
        },
        "STOP": {
            "score_range": "N/A",
            "description": "Hard stop criteria triggered. Critical requirements for privacy, security, or value were not met.",
            "implications": "Project cannot proceed to launch. Hard stop issues must be resolved before reassessment."
        }
    }
}
