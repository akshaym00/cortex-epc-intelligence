from backend.models.compliance import ComplianceFinding
from backend.models.entity import Entity
from backend.models.enums import EntityType, ImpactSeverity
from backend.models.impact import Impact
from backend.models.impact_report import ImpactReport
from backend.models.project import Project
from backend.reasoning.project_controls_brief import ProjectControlsBriefGenerator


def test_controls_brief_blocks_procurement_for_spec_deviation():
    project = Project(name="Demo")
    finding = ComplianceFinding(
        parameter="UPS efficiency",
        required_value=96.0,
        submitted_value=94.5,
        unit="%",
        deviation=1.5,
        status="deviation",
        requirement_citation="Electrical Specification 26 33 53 §2.4.1",
        submittal_citation="VoltSafe VS-442 Page 12",
        recommendation="Reject submittal",
    )

    brief = ProjectControlsBriefGenerator().generate(
        project=project,
        impact_reports=[],
        recommendations=[],
        compliance_findings=[finding],
    )

    assert brief.gate_status == "ON HOLD"
    assert "UPS Procurement Approval" in brief.blocked_gates
    assert brief.decisions[0].owner == "Electrical Consultant"
    assert brief.decisions[0].target == "UPS efficiency >= 96.0%"


def test_controls_brief_quantifies_schedule_exposure():
    source = Entity(
        name="Chiller CH-02",
        entity_type=EntityType.EQUIPMENT,
        description="Delayed chiller",
    )
    target = Entity(
        name="Commissioning",
        entity_type=EntityType.TASK,
        description="Commissioning task",
    )
    project = Project(
        name="Demo",
        entities=[source, target],
    )
    report = ImpactReport(
        event_title="Chiller CH-02 delayed by 5 days",
        overall_severity="medium",
        delay_days=5,
        projected_completion_impact_days=5,
        impacted_entities=[
            Impact(
                affected_entity_id=target.id,
                affected_entity_name=target.name,
                severity=ImpactSeverity.MEDIUM,
                reason="Chiller CH-02 → Commissioning",
                dependency_path=[source.id, target.id],
                delay_days=5,
                critical_path=True,
            )
        ],
    )

    brief = ProjectControlsBriefGenerator().generate(
        project=project,
        impact_reports=[report],
        recommendations=[],
        compliance_findings=[],
    )

    assert brief.gate_status == "AT RISK"
    assert brief.schedule_exposure_days == 5
    assert brief.recoverable_days == 2
    assert brief.critical_path == ["Chiller CH-02", "Commissioning"]
    assert brief.daily_delay_cost == 1800000  # INR 18,00,000/day (illustrative assumption)
    assert brief.impacted_entities == ["Commissioning"]
    assert brief.confidence_breakdown["extraction_certainty"] >= 40
    assert brief.confidence_breakdown["dependency_completeness"] >= 0
    assert brief.confidence_breakdown["base_confidence"] == round(
        brief.confidence_breakdown["extraction_certainty"] * 0.55
        + brief.confidence_breakdown["dependency_completeness"] * 0.45
    )
    assert brief.confidence == brief.confidence_breakdown["final_confidence"]
