from backend.reasoning.schedule_risk import ScheduleRiskAnalyzer


def test_delay_days_and_forecast_are_quantified():
    analyzer = ScheduleRiskAnalyzer()

    delay_days = analyzer.extract_delay_days(
        "Generator G-12 will be delayed by 9 days."
    )
    forecast = analyzer.forecast("Electrical Testing", delay_days)

    assert delay_days == 9
    assert forecast["baseline_start"] == "2026-07-16"
    assert forecast["forecast_start"] == "2026-07-25"
    assert forecast["critical"] is True
