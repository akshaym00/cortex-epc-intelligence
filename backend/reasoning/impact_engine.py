"""
Impact Engine.
"""

from networkx import DiGraph

from backend.models.event import ProjectEvent
from backend.models.impact import Impact
from backend.models.impact_report import ImpactReport
from backend.models.enums import ImpactSeverity
from backend.models.enums import EntityType
from backend.project_state.entity_resolver import EntityResolver
from backend.project_state.living_project_model import LivingProjectModel
from backend.reasoning.dependency_reasoner import DependencyReasoner
from backend.reasoning.explanation_engine import ExplanationEngine
from backend.reasoning.schedule_risk import ScheduleRiskAnalyzer


class ImpactEngine:

    def __init__(self):

        self.reasoner = DependencyReasoner()
        self.explainer = ExplanationEngine()
        self.schedule_risk = ScheduleRiskAnalyzer()

    def analyze(
        self,
        living_model: LivingProjectModel,
        graph: DiGraph,
        event: ProjectEvent,
    ) -> ImpactReport:

        entity = EntityResolver.by_name(
            living_model.project,
            event.affected_entity_name,
        )

        if entity is None:
            return ImpactReport(
                event_title=event.title,
            )

        impacts = []
        delay_days = self.schedule_risk.extract_delay_days(
            event.title,
            event.description,
        )

        downstream = self.reasoner.get_downstream_entities(
            graph,
            entity.id,
        )

        for downstream_id in downstream:

            path = self.reasoner.get_dependency_path(
                graph,
                entity.id,
                downstream_id,
            )

            affected = EntityResolver.by_id(
                living_model.project,
                downstream_id,
            )

            if affected is None:
                continue

            # Events and risks describe causes or inferred conditions; they
            # are not downstream project activities shown to the user.
            if affected.entity_type in {
                EntityType.EVENT,
                EntityType.RISK,
            }:
                continue

            forecast = self.schedule_risk.forecast(
                affected.name,
                delay_days,
            )

            impacts.append(
                Impact(
                    affected_entity_id=affected.id,
                    affected_entity_name=affected.name,
                    severity=ImpactSeverity.MEDIUM,
                    dependency_path=path,
                    reason=self.explainer.explain_path(
                        living_model.project,
                        path,
                    ),
                    delay_days=delay_days,
                    baseline_start=forecast["baseline_start"] if forecast else None,
                    baseline_finish=forecast["baseline_finish"] if forecast else None,
                    forecast_start=forecast["forecast_start"] if forecast else None,
                    forecast_finish=forecast["forecast_finish"] if forecast else None,
                    critical_path=forecast["critical"] if forecast else False,
                )
            )

        if delay_days >= 15:
            severity = "critical"
        elif delay_days >= 8:
            severity = "high"
        elif delay_days >= 3:
            severity = "medium"
        else:
            severity = "low" if not impacts else "medium"

        critical_delay = delay_days if any(i.critical_path for i in impacts) else 0

        report = ImpactReport(
            event_title=event.title,
            impacted_entities=impacts,
            summary=(
                f"{len(impacts)} downstream entities affected; "
                f"forecast critical-path slippage is {critical_delay} days."
                if delay_days
                else f"{len(impacts)} downstream entities affected."
            ),
            overall_severity=severity,
            delay_days=delay_days,
            projected_completion_impact_days=critical_delay,
            methodology=(
                "Delay extracted from the event and propagated through "
                "dependency paths against the project baseline schedule."
            ),
        )

        return report
