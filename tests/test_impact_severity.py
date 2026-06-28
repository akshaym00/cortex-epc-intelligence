from backend.models.enums import ImpactSeverity


def test_impact_severity():

    assert ImpactSeverity.LOW == "low"

    assert ImpactSeverity.MEDIUM == "medium"

    assert ImpactSeverity.HIGH == "high"

    assert ImpactSeverity.CRITICAL == "critical"