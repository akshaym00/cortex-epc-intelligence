import re

from backend.models.compliance import ComplianceFinding


class SpecComplianceAnalyzer:
    """Compares explicit numeric requirements with vendor-submitted values."""

    REQUIREMENT = re.compile(
        r"Requirement\s*\[(?P<citation>[^\]]+)\]\s*:\s*"
        r"(?P<parameter>.+?)\s*>=\s*(?P<value>[\d.]+)\s*(?P<unit>%|[A-Za-z]+)",
        re.IGNORECASE,
    )
    SUBMITTAL = re.compile(
        r"Vendor submittal\s*\[(?P<citation>[^\]]+)\]\s*:\s*"
        r"(?P<parameter>.+?)\s*=\s*(?P<value>[\d.]+)\s*(?P<unit>%|[A-Za-z]+)",
        re.IGNORECASE,
    )

    def analyze(self, document: str) -> list[ComplianceFinding]:
        requirements = list(self.REQUIREMENT.finditer(document))
        submittals = list(self.SUBMITTAL.finditer(document))
        findings = []

        for requirement in requirements:
            parameter = requirement.group("parameter").strip()
            matching_submittal = next(
                (
                    item for item in submittals
                    if item.group("parameter").strip().casefold()
                    == parameter.casefold()
                ),
                None,
            )
            if matching_submittal is None:
                continue

            required = float(requirement.group("value"))
            submitted = float(matching_submittal.group("value"))
            deviation = round(required - submitted, 2)
            compliant = submitted >= required

            findings.append(
                ComplianceFinding(
                    parameter=parameter,
                    required_value=required,
                    submitted_value=submitted,
                    unit=requirement.group("unit"),
                    deviation=max(0, deviation),
                    status="compliant" if compliant else "deviation",
                    requirement_citation=requirement.group("citation").strip(),
                    submittal_citation=matching_submittal.group("citation").strip(),
                    recommendation=(
                        "Accept the submitted value."
                        if compliant
                        else "Reject or request a revised submittal that meets "
                        f"the minimum {required:g}{requirement.group('unit')} requirement."
                    ),
                )
            )

        return findings
