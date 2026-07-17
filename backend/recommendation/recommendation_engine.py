"""
Recommendation Engine.

Generates actionable recommendations from detected
project events and impact reports.
"""

from backend.models.event import ProjectEvent
from backend.models.impact_report import ImpactReport
from backend.models.recommendation import Recommendation


class RecommendationEngine:
    """
    Generates project recommendations.
    """

    def generate(
        self,
        events: list[ProjectEvent],
        impact_reports: list[ImpactReport],
    ) -> list[Recommendation]:

        recommendations = []
        reports_by_event = {
            report.event_title: report
            for report in impact_reports
        }

        for event in events:

            title = event.title.lower()

            # -----------------------------
            # Delay
            # -----------------------------
            if "delay" in title:

                report = reports_by_event.get(event.title)
                delay_days = report.delay_days if report else 0
                impact_days = (
                    report.projected_completion_impact_days
                    if report else 0
                )

                recommendations.append(
                    Recommendation(
                        title="Expedite delayed activity",
                        description=(
                            f"Request a vendor recovery plan within 24 hours. "
                            f"The reported {delay_days}-day delay currently "
                            f"creates {impact_days} days of critical-path "
                            f"exposure. Track recovery milestones daily."
                            if delay_days
                            else "Request a vendor recovery plan within 24 "
                            "hours and track recovery milestones daily."
                        ),
                        priority="high",
                        related_event=event.title,
                    )
                )

                recommendations.append(
                    Recommendation(
                        title="Review project schedule",
                        description=(
                            f"Rebaseline {len(report.impacted_entities)} "
                            f"downstream activities and issue the {impact_days}-day "
                            f"completion forecast to planning and commissioning."
                            if report and report.impacted_entities
                            else "Rebaseline dependent activities and issue an "
                            "updated completion forecast."
                        ),
                        priority="high",
                        related_event=event.title,
                    )
                )

            # -----------------------------
            # Risk
            # -----------------------------
            if "risk" in title:

                recommendations.append(
                    Recommendation(
                        title="Mitigate identified risk",
                        description=(
                            "Develop contingency plans for the "
                            "affected activities."
                        ),
                        priority="medium",
                        related_event=event.title,
                    )
                )

        # -----------------------------
        # Impact Reports
        # -----------------------------

        for report in impact_reports:

            if len(report.impacted_entities) > 0:

                recommendations.append(
                    Recommendation(
                        title="Notify impacted teams",
                        description=(
                            f"Issue schedule revisions to owners of: "
                            f"{', '.join(impact.affected_entity_name for impact in report.impacted_entities)}. "
                            f"Complete notification before the earliest forecast "
                            f"start date."
                        ),
                        priority=report.overall_severity,
                        related_event=report.event_title,
                    )
                )

            if report.projected_completion_impact_days > 0:
                recoverable_days = max(
                    1,
                    round(report.projected_completion_impact_days * 0.4),
                )
                recommendations.append(
                    Recommendation(
                        title="Resequence critical-path work",
                        description=(
                            f"The current forecast shows "
                            f"{report.projected_completion_impact_days} days of "
                            f"critical-path slippage. Parallel testing preparation "
                            f"and commissioning readiness could recover approximately "
                            f"{recoverable_days} days; validate this scenario with the "
                            f"project scheduler."
                        ),
                        priority="high",
                        related_event=report.event_title,
                    )
                )

        # Multiple events can produce the same action. Keep the first
        # occurrence so the dashboard remains concise and actionable.
        unique_recommendations = {}

        for recommendation in recommendations:
            key = recommendation.title.strip().casefold()
            unique_recommendations.setdefault(key, recommendation)

        return list(unique_recommendations.values())
