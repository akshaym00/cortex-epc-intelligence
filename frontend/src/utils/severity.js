const severityIcons = {
  low: "🟢",
  medium: "🟡",
  high: "🟠",
  critical: "🔴",
};

export function severityLabel(value = "low") {
  const normalized = String(value || "low").toLowerCase();
  return `${severityIcons[normalized] || "⚪"} ${normalized.toUpperCase()}`;
}

export function severityText(value = "low") {
  return String(value || "low").toUpperCase();
}
