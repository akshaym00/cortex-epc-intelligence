from backend.models.base import CortexBaseModel


class ComplianceFinding(CortexBaseModel):
    parameter: str
    required_value: float
    submitted_value: float
    unit: str
    deviation: float
    status: str
    requirement_citation: str
    submittal_citation: str
    recommendation: str
