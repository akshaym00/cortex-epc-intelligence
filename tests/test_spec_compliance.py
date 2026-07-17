from backend.reasoning.spec_compliance import SpecComplianceAnalyzer


def test_flags_vendor_submittal_below_spec_with_citations():
    document = """
    Requirement [Spec 26 33 53 §2.4.1, page 47]: UPS efficiency >= 96.0 %
    Vendor submittal [VS-442, page 12]: UPS efficiency = 94.5 %
    """

    findings = SpecComplianceAnalyzer().analyze(document)

    assert len(findings) == 1
    assert findings[0].status == "deviation"
    assert findings[0].deviation == 1.5
    assert findings[0].requirement_citation == "Spec 26 33 53 §2.4.1, page 47"
    assert findings[0].submittal_citation == "VS-442, page 12"
