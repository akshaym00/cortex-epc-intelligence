"""
Project Controls Brief generator.

Turns reasoning outputs into a practical decision pack for project
controls engineers and project managers.
"""

from datetime import date

from backend.models.compliance import ComplianceFinding
from backend.models.controls import ControlDecision, ProjectControlsBrief
from backend.models.enums import EntityType, RelationshipType
from backend.models.impact_report import ImpactReport
from backend.models.project import Project
from backend.models.recommendation import Recommendation
from backend.reasoning.schedule_risk import ScheduleRiskAnalyzer


class ProjectControlsBriefGenerator:
    """
    Creates a project-controls command view from extracted intelligence.
    """

    def generate(
        self,
        project: Project,
        impact_reports: list[ImpactReport],
        recommendations: list[Recommendation],
        compliance_findings: list[ComplianceFinding],
    ) -> ProjectControlsBrief:

        deviations = [
            finding
            for finding in compliance_findings
            if finding.status == "deviation"
        ]
        schedule_exposure_days = max(
            [
                report.projected_completion_impact_days
                for report in impact_reports
            ]
            or [0]
        )
        recoverable_days = (
            max(1, round(schedule_exposure_days * 0.4))
            if schedule_exposure_days
            else 0
        )
        critical_path = self._critical_path(project, impact_reports)

        if deviations:
            gate_status = "ON HOLD"
            procurement_gate = "Blocked pending technical approval"
            status_reason = (
                "A vendor submittal does not meet the minimum technical "
                "requirement, so procurement approval should not proceed."
            )
        elif schedule_exposure_days > 0:
            gate_status = "AT RISK"
            procurement_gate = "Proceed with recovery controls"
            status_reason = (
                f"Critical-path exposure of {schedule_exposure_days} days "
                "requires schedule recovery and daily controls review."
            )
        else:
            gate_status = "CLEAR"
            procurement_gate = "Proceed"
            status_reason = (
                "No active compliance blockers or critical-path slippage "
                "detected in the analyzed document."
            )

        extraction_certainty = self._extraction_certainty(project)
        dependency_completeness = self._dependency_completeness(project)
        confidence_breakdown = self._confidence_breakdown(
            extraction_certainty,
            dependency_completeness,
            deviations,
            schedule_exposure_days,
        )
        schedule_risk = ScheduleRiskAnalyzer()
        brief = ProjectControlsBrief(
            gate_status=gate_status,
            status_reason=status_reason,
            procurement_gate=procurement_gate,
            schedule_exposure_days=schedule_exposure_days,
            recoverable_days=recoverable_days,
            commercial_notice=(
                "Prepare delay notice / vendor backcharge assessment."
                if schedule_exposure_days > 0
                else "No delay notice currently triggered."
            ),
            confidence=confidence_breakdown["final_confidence"],
            extraction_certainty=extraction_certainty,
            dependency_completeness=dependency_completeness,
            confidence_breakdown=confidence_breakdown,
            daily_delay_cost=schedule_risk.daily_delay_cost,
            impacted_entities=self._impacted_entities(impact_reports),
            critical_path=critical_path,
            blocked_gates=self._blocked_gates(project, impact_reports, deviations, schedule_exposure_days),
            next_72_hours=self._next_72_hours(deviations, schedule_exposure_days),
            decisions=self._decisions(
                deviations,
                schedule_exposure_days,
                recoverable_days,
                recommendations,
                impact_reports,
            ),
        )

        return brief

    def _critical_path(
        self,
        project: Project,
        impact_reports: list[ImpactReport],
    ) -> list[str]:

        entity_lookup = {
            entity.id: entity.name
            for entity in project.entities
        }

        critical_impacts = [
            impact
            for report in impact_reports
            for impact in report.impacted_entities
            if impact.critical_path
        ]
        if not critical_impacts:
            critical_impacts = [
                impact
                for report in impact_reports
                for impact in report.impacted_entities
            ]

        if not critical_impacts:
            return []

        selected = max(
            critical_impacts,
            key=lambda impact: impact.delay_days,
        )

        if selected.dependency_path:
            return [
                entity_lookup.get(entity_id, entity_id)
                for entity_id in selected.dependency_path
            ]

        return [selected.affected_entity_name]

    def _confidence_breakdown(
        self,
        extraction_certainty: int,
        dependency_completeness: int,
        deviations: list[ComplianceFinding],
        schedule_exposure_days: int,
    ) -> dict[str, int | float]:

        weight_extraction = 0.55
        weight_dependency = 0.45
        base_confidence = round(
            extraction_certainty * weight_extraction
            + dependency_completeness * weight_dependency
        )
        final_confidence = base_confidence

        if deviations and schedule_exposure_days:
            final_confidence = min(100, max(base_confidence, 94))
        elif deviations:
            final_confidence = min(100, max(base_confidence, 92))
        elif schedule_exposure_days:
            final_confidence = min(100, max(base_confidence, 88))

        return {
            "extraction_certainty": extraction_certainty,
            "dependency_completeness": dependency_completeness,
            "weight_extraction": weight_extraction,
            "weight_dependency": weight_dependency,
            "base_confidence": base_confidence,
            "final_confidence": final_confidence,
        }

    def _extraction_certainty(self, project: Project) -> int:
        if not project.entities:
            return 0

        entity_ids = {entity.id for entity in project.entities}
        connected_entity_ids = {
            rel.source_entity_id
            for rel in project.relationships
            if rel.source_entity_id in entity_ids
        } | {
            rel.target_entity_id
            for rel in project.relationships
            if rel.target_entity_id in entity_ids
        }

        orphan_entities = [
            entity
            for entity in project.entities
            if entity.entity_type not in {
                EntityType.EVENT,
                EntityType.RISK,
                EntityType.ISSUE,
            }
            and entity.id not in connected_entity_ids
        ]

        orphan_ratio = len(orphan_entities) / len(project.entities)
        expected_types = {
            RelationshipType.SUPPLIES,
            RelationshipType.DEPENDS_ON,
            RelationshipType.AFFECTS,
        }
        actual_types = {
            rel.relationship_type
            for rel in project.relationships
        }
        type_coverage = len(actual_types & expected_types) / len(expected_types)

        certainty = 100 - round(orphan_ratio * 40) - round((1 - type_coverage) * 20)
        return max(40, min(100, certainty))

    def _dependency_completeness(self, project: Project) -> int:
        if not project.relationships:
            return 0

        entity_ids = {entity.id for entity in project.entities}
        resolved_relationships = [
            rel
            for rel in project.relationships
            if rel.source_entity_id in entity_ids
            and rel.target_entity_id in entity_ids
        ]

        resolved_ratio = (
            len(resolved_relationships) / len(project.relationships)
            if project.relationships
            else 0
        )

        expected_types = {
            RelationshipType.SUPPLIES,
            RelationshipType.DEPENDS_ON,
            RelationshipType.AFFECTS,
        }
        actual_types = {
            rel.relationship_type
            for rel in project.relationships
        }
        type_coverage = len(actual_types & expected_types) / len(expected_types)

        completeness = round((resolved_ratio * 0.7 + type_coverage * 0.3) * 100)
        return max(0, min(100, completeness))

    def _blocked_gates(
        self,
        project: Project,
        impact_reports: list[ImpactReport],
        deviations: list[ComplianceFinding],
        schedule_exposure_days: int,
    ) -> list[str]:
        entity_lookup = {
            entity.name: entity
            for entity in project.entities
        }

        gates = []

        for report in impact_reports:
            for impact in report.impacted_entities:
                entity = entity_lookup.get(impact.affected_entity_name)
                if not entity:
                    continue
                if entity.entity_type not in {
                    EntityType.MILESTONE,
                    EntityType.APPROVAL,
                }:
                    continue
                if self._is_gate_blocked(impact):
                    gates.append(entity.name)

        if not gates:
            if deviations:
                gates.extend(["Technical Submittal Review", "UPS Procurement Approval"])
            elif schedule_exposure_days:
                gates.extend(["Project Procurement", "Commissioning Readiness"])

        return list(dict.fromkeys(gates))

    def _impacted_entities(
        self,
        impact_reports: list[ImpactReport],
    ) -> list[str]:
        impacted = {
            impact.affected_entity_name
            for report in impact_reports
            for impact in report.impacted_entities
        }
        return sorted(impacted)

    def _is_gate_blocked(self, impact) -> bool:
        if impact.baseline_finish and impact.forecast_finish:
            if date.fromisoformat(impact.forecast_finish) > date.fromisoformat(
                impact.baseline_finish
            ):
                return True

        if impact.baseline_start and impact.forecast_start:
            if date.fromisoformat(impact.forecast_start) > date.fromisoformat(
                impact.baseline_start
            ):
                return True

        return False

    def _next_72_hours(
        self,
        deviations: list[ComplianceFinding],
        schedule_exposure_days: int,
    ) -> list[str]:

        actions = []

        if deviations:
            actions.extend(
                [
                    "Reject non-compliant submittal in the review log.",
                    "Request revised vendor submission before procurement approval.",
                ]
            )

        if schedule_exposure_days:
            actions.extend(
                [
                    "Request vendor recovery plan with dated milestones.",
                    "Issue updated forecast to procurement, planning, and commissioning.",
                ]
            )

        if not actions:
            actions.append("Continue monitoring extracted risks and approvals.")

        return actions[:4]

    def _decisions(
        self,
        deviations: list[ComplianceFinding],
        schedule_exposure_days: int,
        recoverable_days: int,
        recommendations: list[Recommendation],
        impact_reports: list[ImpactReport],
    ) -> list[ControlDecision]:

        decisions = []

        for finding in deviations:
            decisions.append(
                ControlDecision(
                    title="Reject current vendor submittal",
                    owner="Electrical Consultant",
                    priority="high",
                    due="Before Procurement Approval",
                    rationale=(
                        f"{finding.parameter} submitted at "
                        f"{finding.submitted_value}{finding.unit}, below the "
                        f"required {finding.required_value}{finding.unit}."
                    ),
                    target=(
                        f"{finding.parameter} >= "
                        f"{finding.required_value}{finding.unit}"
                    ),
                )
            )

        if schedule_exposure_days:
            decisions.append(
                ControlDecision(
                    title="Approve recovery schedule",
                    owner="Project Controls Engineer",
                    priority="high",
                    due="Within 24 hours",
                    rationale=(
                        f"Current forecast shows {schedule_exposure_days} "
                        "days of critical-path exposure."
                    ),
                    target=(
                        f"Recover approximately {recoverable_days} days "
                        "through resequencing."
                    ),
                )
            )
            decisions.append(
                ControlDecision(
                    title="Prepare commercial delay notice",
                    owner="Project Manager",
                    priority="medium",
                    due="Within 48 hours",
                    rationale=(
                        "Critical-path slippage may require formal notice "
                        "and vendor recovery accountability."
                    ),
                    target="Protect entitlement and document mitigation steps.",
                )
            )

        if impact_reports and any(report.impacted_entities for report in impact_reports):
            impacted = {
                impact.affected_entity_name
                for report in impact_reports
                for impact in report.impacted_entities
            }
            decisions.append(
                ControlDecision(
                    title="Notify impacted workstream owners",
                    owner="Planning Engineer",
                    priority="medium",
                    due="Today",
                    rationale=(
                        "Downstream activities require updated forecast "
                        "dates and owner acknowledgement."
                    ),
                    target=", ".join(sorted(impacted)[:4]),
                )
            )

        if not decisions and recommendations:
            first = recommendations[0]
            decisions.append(
                ControlDecision(
                    title=first.title,
                    owner="Project Manager",
                    priority=first.priority,
                    due="This week",
                    rationale=first.description,
                )
            )

        return decisions[:4]
