import json
import re
from datetime import date, timedelta
from pathlib import Path


class ScheduleRiskAnalyzer:
    """Quantifies delay propagation against the demo baseline schedule."""

    def __init__(self, schedule_path: Path | None = None):
        path = schedule_path or (
            Path(__file__).resolve().parents[2]
            / "demo_data"
            / "project_schedule.json"
        )
        self.schedule = json.loads(path.read_text(encoding="utf-8"))
        self.daily_delay_cost = self.schedule.get("daily_delay_cost", 0)

    @staticmethod
    def extract_delay_days(*texts: str) -> int:
        for text in texts:
            match = re.search(r"(\d+)\s*(?:calendar\s+|working\s+)?days?", text, re.I)
            if match:
                return int(match.group(1))
        return 0

    def forecast(self, entity_name: str, delay_days: int) -> dict | None:
        query = entity_name.strip().casefold()

        for activity in self.schedule["activities"]:
            names = [activity["name"], *activity.get("aliases", [])]
            if any(name.casefold() in query or query in name.casefold() for name in names):
                baseline_start = date.fromisoformat(activity["baseline_start"])
                baseline_finish = date.fromisoformat(activity["baseline_finish"])
                return {
                    "baseline_start": baseline_start.isoformat(),
                    "baseline_finish": baseline_finish.isoformat(),
                    "forecast_start": (baseline_start + timedelta(days=delay_days)).isoformat(),
                    "forecast_finish": (baseline_finish + timedelta(days=delay_days)).isoformat(),
                    "critical": activity.get("critical", False),
                }

        return None
