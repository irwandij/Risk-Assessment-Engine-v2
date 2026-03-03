"""Markdown report generator for assessment results.

Supports all assessment types:
- Merchant Assessment
- Partners Assessment
- Vendor Assessment
- AI Project Assessment
"""

from typing import Optional, Dict, Any, List
from datetime import datetime
from ..models.assessment_result import (
    AssessmentResult,
    ParameterScore,
    DecisionResult,
    Condition,
    Recommendation,
    AutoRejectTrigger,
)
from ..config import (
    MerchantType,
    Decision,
    AssessmentType,
    ASSESSMENT_TYPE_INFO,
    DECISION_BAND_DESCRIPTIONS,
    DECISION_BANDS,
    PARTNER_DECISION_BANDS,
    VENDOR_DECISION_BANDS,
    AI_DECISION_BANDS,
)


class ReportGenerator:
    """Generates markdown assessment reports from AssessmentResult."""

    def generate(self, result: AssessmentResult) -> str:
        """
        Generate full markdown assessment report.

        Args:
            result: AssessmentResult from Assessor

        Returns:
            Markdown formatted report string
        """
        # Determine assessment type
        assessment_type = self._get_assessment_type(result)

        sections = [
            self._generate_header(result, assessment_type),
            self._generate_executive_summary(result, assessment_type),
            self._generate_classification(result, assessment_type),
            self._generate_regulatory_gate(result),
            self._generate_decision_rationale(result, assessment_type),
            self._generate_parameter_scores(result, assessment_type),
            self._generate_evidence_references(result, assessment_type),
            self._generate_detailed_findings(result),
            self._generate_risk_treatment(result),
            self._generate_conditions(result),
            self._generate_conclusion(result, assessment_type),
            self._generate_footer(result),
        ]

        return "\n\n".join(filter(None, sections))

    def _get_assessment_type(self, result: AssessmentResult) -> str:
        """Get assessment type string from result."""
        merchant_type = result.merchant_type
        if isinstance(merchant_type, AssessmentType):
            return merchant_type.value
        elif isinstance(merchant_type, MerchantType):
            return "merchant"
        elif isinstance(merchant_type, str):
            return merchant_type
        return "merchant"

    def _generate_header(self, result: AssessmentResult, assessment_type: str) -> str:
        """Generate report header."""
        type_info = ASSESSMENT_TYPE_INFO.get(assessment_type, {})
        type_name = type_info.get("name", "Risk Assessment")
        return f"# {type_name}: {result.merchant_name}"

    def _generate_executive_summary(self, result: AssessmentResult, assessment_type: str) -> str:
        """Generate executive summary section."""
        lines = [
            "## Executive Summary",
            "",
            f"- **Assessment Type**: {self._format_assessment_type(assessment_type)}",
            f"- **Overall Risk Rating**: {result.risk_level.value}",
            f"- **Total Score**: {result.total_score}/{self._get_max_score(assessment_type)}",
            f"- **Decision**: **{result.decision.value}**",
            f"- **Assessment Date**: {result.assessment_date.strftime('%Y-%m-%d %H:%M')}",
        ]

        if result.decision_result.is_auto_rejected:
            lines.append("")
            lines.append("### Auto-Reject Triggers")
            lines.append("")
            for trigger in result.decision_result.auto_reject_triggers:
                lines.append(f"- **{trigger.code}**: {trigger.reason}")
                if trigger.details:
                    lines.append(f"  - {trigger.details}")

        return "\n".join(lines)

    def _generate_classification(self, result: AssessmentResult, assessment_type: str) -> str:
        """Generate classification section based on assessment type."""
        classification = result.classification

        if assessment_type == "merchant":
            return self._generate_merchant_classification(classification)
        elif assessment_type == "partner":
            return self._generate_partner_classification(classification)
        elif assessment_type == "vendor":
            return self._generate_vendor_classification(classification)
        elif assessment_type == "ai_project":
            return self._generate_ai_classification(classification)

        return ""

    def _generate_merchant_classification(self, classification: Dict[str, Any]) -> str:
        """Generate merchant classification section."""
        lines = [
            "## Merchant Classification",
            "",
            f"- **Business Model**: {classification.get('business_model', 'N/A')}",
            f"- **Payment Processing**: {classification.get('payment_processing', 'N/A')}",
            f"- **Merchant Type**: {classification.get('merchant_type_display', 'N/A')}",
            f"- **Regulatory Requirement**: {classification.get('regulatory_requirement', 'N/A')}",
            f"- **Subscription Model**: {'Yes' if classification.get('is_subscription_model') else 'No'}",
        ]
        return "\n".join(lines)

    def _generate_partner_classification(self, classification: Dict[str, Any]) -> str:
        """Generate partner classification section."""
        lines = [
            "## Partner Classification",
            "",
            f"- **Partnership Type**: {classification.get('partnership_type', 'N/A')}",
            f"- **Industry Sector**: {classification.get('industry_sector', 'N/A')}",
            f"- **Country**: {classification.get('country', 'N/A')}",
        ]
        return "\n".join(lines)

    def _generate_vendor_classification(self, classification: Dict[str, Any]) -> str:
        """Generate vendor classification section."""
        lines = [
            "## Vendor Classification",
            "",
            f"- **Vendor Type**: {classification.get('vendor_type', 'N/A')}",
            f"- **Service Criticality**: {classification.get('service_criticality', 'N/A')}",
            f"- **Country**: {classification.get('country', 'N/A')}",
        ]
        return "\n".join(lines)

    def _generate_ai_classification(self, classification: Dict[str, Any]) -> str:
        """Generate AI project classification section."""
        lines = [
            "## AI Project Classification",
            "",
            f"- **Project Owner**: {classification.get('project_owner', 'N/A')}",
            f"- **Department**: {classification.get('department', 'N/A')}",
            f"- **AI Type**: {classification.get('ai_type', 'N/A')}",
            f"- **External Facing**: {'Yes' if classification.get('is_external_facing') else 'No'}",
            f"- **Processes Personal Data**: {'Yes' if classification.get('processes_personal_data') else 'No'}",
        ]
        return "\n".join(lines)

    def _generate_regulatory_gate(self, result: AssessmentResult) -> Optional[str]:
        """Generate regulatory gate section (for PJP/Aggregators only)."""
        if result.merchant_type != MerchantType.PJP:
            return None

        gate = result.regulatory_gate
        if not gate:
            return None

        lines = [
            "## Regulatory Gate Check (PJP/Aggregator)",
            "",
            f"- **Regulated Activity**: {'Yes' if gate.get('regulated_activity') else 'No'}",
            f"- **Required License**: {gate.get('required_license', 'N/A')}",
            f"- **License Status**: {gate.get('license_status', 'N/A')}",
        ]

        if gate.get("license_number"):
            lines.append(f"- **License Number**: {gate.get('license_number')}")

        lines.append(f"- **Gate Override**: {gate.get('gate_override_reason', 'N/A')}")

        return "\n".join(lines)

    def _generate_decision_rationale(self, result: AssessmentResult, assessment_type: str) -> str:
        """Generate decision rationale section explaining why the decision was made."""
        lines = [
            "## Decision Rationale",
            "",
        ]

        # Get decision description
        decision_value = result.decision.value if hasattr(result.decision, 'value') else str(result.decision)
        band_descriptions = DECISION_BAND_DESCRIPTIONS.get(assessment_type, {})
        decision_info = band_descriptions.get(decision_value, {})

        # Decision explanation
        if decision_info:
            lines.append("### Why This Decision?")
            lines.append("")
            score_range = decision_info.get("score_range", "N/A")
            if score_range != "N/A":
                lines.append(f"The total score of **{result.total_score}** falls within the **{score_range}** range, which maps to **{decision_value}**.")
            lines.append("")
            lines.append(decision_info.get("description", "No description available."))
            lines.append("")
            lines.append(f"**Implications:** {decision_info.get('implications', 'N/A')}")
            lines.append("")

        # Decision thresholds table
        lines.append("### Decision Thresholds")
        lines.append("")
        lines.append("| Score Range | Decision | Risk Level | Active |")
        lines.append("|-------------|----------|------------|--------|")

        # Get decision bands for this assessment type
        bands = self._get_decision_bands_for_type(assessment_type)
        for (min_score, max_score), decision in bands.items():
            is_active = min_score <= result.total_score <= max_score
            active_marker = " **CURRENT**" if is_active else ""
            risk_level = self._get_risk_level_for_decision(decision, assessment_type)
            decision_label = decision.value if hasattr(decision, "value") else str(decision)
            lines.append(
                f"| {min_score}-{max_score} | {decision_label} | {risk_level} |{'Yes' if is_active else ''}{active_marker} |"
            )

        lines.append("")

        # Key supporting factors
        supporting_factors = self._get_supporting_factors(result)
        if supporting_factors:
            lines.append("### Key Supporting Factors")
            lines.append("")
            for factor in supporting_factors:
                lines.append(f"- {factor}")
            lines.append("")

        # Areas of concern
        areas_of_concern = self._get_areas_of_concern(result)
        if areas_of_concern:
            lines.append("### Areas of Concern")
            lines.append("")
            for concern in areas_of_concern:
                lines.append(f"- {concern}")
            lines.append("")

        # Auto-reject triggers if applicable
        if result.decision_result.is_auto_rejected and result.decision_result.auto_reject_triggers:
            lines.append("### Auto-Reject Triggers Activated")
            lines.append("")
            for trigger in result.decision_result.auto_reject_triggers:
                lines.append(f"- **{trigger.code}**: {trigger.reason}")
                if trigger.details:
                    lines.append(f"  - Details: {trigger.details}")
            lines.append("")

        return "\n".join(lines)

    def _generate_evidence_references(self, result: AssessmentResult, assessment_type: str) -> str:
        """Generate evidence and references section with per-parameter details."""
        lines = [
            "## Evidence & References",
            "",
        ]

        # Reference URLs
        if result.reference_urls:
            lines.append("### Reference Links")
            lines.append("")
            lines.append("| Source | URL |")
            lines.append("|--------|-----|")
            for source, url in result.reference_urls.items():
                # Format source name
                source_display = source.replace("_", " ").title()
                if url:
                    lines.append(f"| {source_display} | {url} |")
                else:
                    lines.append(f"| {source_display} | Not provided |")
            lines.append("")

        # Per-parameter evidence and gaps
        lines.append("### Parameter Evidence & Gaps")
        lines.append("")

        type_info = ASSESSMENT_TYPE_INFO.get(assessment_type, {})
        param_names = type_info.get("parameters", {})

        for param_id in sorted(result.parameter_scores.keys()):
            score = result.parameter_scores.get(param_id)
            if score:
                param_name = param_names.get(param_id, score.parameter_name)
                lines.append(f"#### {param_id}. {param_name}")
                lines.append("")
                lines.append(f"**Score:** {score.score}/{score.max_score} ({score.rating})")
                lines.append("")

                if score.evidence:
                    lines.append("**Evidence:**")
                    lines.append("")
                    for evidence in score.evidence:
                        lines.append(f"- {evidence}")
                    lines.append("")

                if score.gaps:
                    lines.append("**Gaps/Concerns:**")
                    lines.append("")
                    for gap in score.gaps:
                        lines.append(f"- {gap}")
                    lines.append("")

                if score.notes:
                    lines.append(f"**Notes:** {score.notes}")
                    lines.append("")

        return "\n".join(lines)

    def _get_decision_bands_for_type(self, assessment_type: str) -> Dict:
        """Get decision bands for the assessment type."""
        if assessment_type == "merchant":
            return DECISION_BANDS
        elif assessment_type == "partner":
            return PARTNER_DECISION_BANDS
        elif assessment_type == "vendor":
            return VENDOR_DECISION_BANDS
        elif assessment_type == "ai_project":
            return AI_DECISION_BANDS
        return DECISION_BANDS

    def _get_risk_level_for_decision(self, decision: str, assessment_type: str) -> str:
        """Get risk level for a decision."""
        from ..config import DECISION_RISK_LEVELS, PARTNER_RISK_LEVELS, VENDOR_RISK_LEVELS, AI_RISK_LEVELS

        risk_levels_map = {
            "merchant": DECISION_RISK_LEVELS,
            "partner": PARTNER_RISK_LEVELS,
            "vendor": VENDOR_RISK_LEVELS,
            "ai_project": AI_RISK_LEVELS,
        }

        risk_levels = risk_levels_map.get(assessment_type, {})
        risk_level = risk_levels.get(decision)
        if risk_level:
            return risk_level.value if hasattr(risk_level, 'value') else str(risk_level)
        return "N/A"

    def _get_supporting_factors(self, result: AssessmentResult) -> List[str]:
        """Extract key supporting factors from high-scoring parameters."""
        factors = []
        for param_id, score in result.parameter_scores.items():
            if score.rating in ["excellent", "good"]:
                factor = f"**{score.parameter_name}**: Scored {score.score}/{score.max_score} ({score.rating})"
                if score.evidence:
                    factor += f" - {score.evidence[0][:60]}..." if len(score.evidence[0]) > 60 else f" - {score.evidence[0]}"
                factors.append(factor)
        return factors[:5]  # Limit to top 5

    def _get_areas_of_concern(self, result: AssessmentResult) -> List[str]:
        """Extract areas of concern from weak/poor/fail parameters."""
        concerns = []
        for param_id, score in result.parameter_scores.items():
            if score.rating in ["weak", "poor", "fail"]:
                concern = f"**{score.parameter_name}**: Scored {score.score}/{score.max_score} ({score.rating})"
                if score.gaps:
                    concern += f" - {score.gaps[0][:60]}..." if len(score.gaps[0]) > 60 else f" - {score.gaps[0]}"
                concerns.append(concern)
        return concerns[:5]  # Limit to top 5

    def _generate_parameter_scores(self, result: AssessmentResult, assessment_type: str) -> str:
        """Generate parameter scores table."""
        type_info = ASSESSMENT_TYPE_INFO.get(assessment_type, {})
        param_names = type_info.get("parameters", {})
        max_total = type_info.get("max_total_score", 100)

        lines = [
            "## Parameter Scores",
            "",
            "| # | Parameter | Score | Max | Rating | Notes |",
            "|---|-----------|-------|-----|--------|-------|",
        ]

        for param_id in sorted(result.parameter_scores.keys()):
            score = result.parameter_scores.get(param_id)
            if score:
                param_name = param_names.get(param_id, score.parameter_name)
                notes = score.notes[:40] + "..." if len(score.notes) > 40 else score.notes
                lines.append(
                    f"| {param_id} | {param_name} | "
                    f"{score.score} | {score.max_score} | {score.rating} | {notes or '-'} |"
                )

        lines.append(f"| **TOTAL** | | **{result.total_score}** | **{max_total}** | | |")

        return "\n".join(lines)

    def _generate_detailed_findings(self, result: AssessmentResult) -> str:
        """Generate detailed findings section."""
        lines = ["## Detailed Findings", ""]

        if result.strengths:
            lines.append("### Strengths")
            lines.append("")
            for i, strength in enumerate(result.strengths, 1):
                lines.append(f"{i}. {strength}")
            lines.append("")

        if result.concerns:
            lines.append("### Concerns and Gaps")
            lines.append("")
            for i, concern in enumerate(result.concerns, 1):
                lines.append(f"{i}. {concern}")

        return "\n".join(lines)

    def _generate_risk_treatment(self, result: AssessmentResult) -> Optional[str]:
        """Generate risk treatment recommendations section."""
        if not result.recommendations:
            return None

        lines = [
            "## Risk Treatment Recommendations",
            "",
        ]

        for i, rec in enumerate(result.recommendations, 1):
            priority_marker = (
                "HIGH" if rec.priority == "high"
                else "MEDIUM" if rec.priority == "medium"
                else "LOW"
            )
            lines.append(f"{i}. {rec.recommendation} - Priority: **{priority_marker}**")

        return "\n".join(lines)

    def _generate_conditions(self, result: AssessmentResult) -> Optional[str]:
        """Generate conditions section for conditional decisions."""
        # Check for various conditional decisions
        conditional_decisions = [
            Decision.PROCEED_WITH_CONDITIONS,
            "CONDITIONS",
            "CONDITIONAL",
        ]

        if result.decision not in conditional_decisions:
            return None

        conditions = result.decision_result.conditions
        if not conditions:
            return None

        lines = [
            "## Conditions",
            "",
            "The following conditions must be addressed:",
            "",
        ]

        for i, cond in enumerate(conditions, 1):
            timeline = f" (Due: {cond.timeline_days} days)" if cond.timeline_days else ""
            lines.append(f"{i}. {cond.condition}{timeline}")

        return "\n".join(lines)

    def _generate_conclusion(self, result: AssessmentResult, assessment_type: str) -> str:
        """Generate conclusion section."""
        lines = [
            "## Conclusion",
            "",
        ]

        decision = result.decision.value if hasattr(result.decision, 'value') else str(result.decision)
        max_score = self._get_max_score(assessment_type)

        if decision in ["PROCEED", "APPROVED", "LOW"]:
            lines.append(
                f"Based on the assessment, **{result.merchant_name}** has achieved a score of "
                f"**{result.total_score}/{max_score}** with a **{result.risk_level.value}** risk rating. "
                f"The {'project' if assessment_type == 'ai_project' else 'entity'} is approved for standard operations with normal monitoring."
            )
        elif decision in ["PROCEED WITH CONDITIONS", "CONDITIONS", "CONDITIONAL", "MEDIUM"]:
            lines.append(
                f"Based on the assessment, **{result.merchant_name}** has achieved a score of "
                f"**{result.total_score}/{max_score}** with a **{result.risk_level.value}** risk rating. "
                f"{'The project' if assessment_type == 'ai_project' else 'The entity'} may proceed with enhanced monitoring and must address the identified conditions."
            )
        elif decision in ["CONDITIONAL REJECT", "REVIEW", "ESCALATE", "HIGH"]:
            lines.append(
                f"Based on the assessment, **{result.merchant_name}** has achieved a score of "
                f"**{result.total_score}/{max_score}** with a **{result.risk_level.value}** risk rating. "
                f"This decision requires **senior review** before final determination. "
                f"A business justification and mitigation plan must be submitted."
            )
        else:  # REJECT, DECLINE, STOP
            if decision == "STOP":
                lines.append(
                    f"Based on the assessment, **{result.merchant_name}** has been rated as "
                    f"**STOP** with a score of **{result.total_score}/{max_score}**. "
                    f"The project **cannot proceed to launch**."
                )
            else:
                lines.append(
                    f"Based on the assessment, **{result.merchant_name}** has been rated as "
                    f"**{result.risk_level.value}** risk with a score of **{result.total_score}/{max_score}**. "
                    f"The {'project' if assessment_type == 'ai_project' else 'entity'} is **not suitable for approval**."
                )

            if result.decision_result.is_auto_rejected:
                lines.append("")
                lines.append("**Auto-Reject Reason(s):**")
                for trigger in result.decision_result.auto_reject_triggers:
                    lines.append(f"- {trigger.reason}")

        return "\n".join(lines)

    def _generate_footer(self, result: AssessmentResult) -> str:
        """Generate report footer."""
        return (
            "---\n\n"
            f"*Assessment conducted using Risk Assessment Framework v{result.framework_version}*\n"
            f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"
        )

    def _format_assessment_type(self, assessment_type: str) -> str:
        """Format assessment type for display."""
        type_names = {
            "merchant": "Merchant Risk Assessment",
            "partner": "Partners Assessment",
            "vendor": "Third-party Vendor Assessment",
            "ai_project": "AI Project Assessment",
        }
        return type_names.get(assessment_type, assessment_type.title())

    def _format_merchant_type(self, merchant_type: MerchantType) -> str:
        """Format merchant type for display."""
        if merchant_type == MerchantType.PJP:
            return "PJP / Aggregator"
        return "Regular Merchant"

    def _get_max_score(self, assessment_type: str) -> int:
        """Get max total score for assessment type."""
        type_info = ASSESSMENT_TYPE_INFO.get(assessment_type, {})
        return type_info.get("max_total_score", 100)
