"""
Tests for the EventParser.
"""

import json

import pytest

from backend.extraction.event_parser import EventParser


def test_parse_valid_events():
    """EventParser should parse valid JSON into EventExtractionResponse."""

    raw = json.dumps({
        "events": [
            {
                "title": "Generator delivery delayed",
                "event_type": "delay",
                "description": "Cummins notified a 14-day delay.",
                "affected_entity_name": "Generator G-12",
                "severity": "high",
            }
        ]
    })

    result = EventParser.parse(raw)

    assert len(result.events) == 1
    assert result.events[0].title == "Generator delivery delayed"
    assert result.events[0].event_type == "delay"
    assert result.events[0].severity == "high"


def test_parse_multiple_events():
    """EventParser should handle multiple events."""

    raw = json.dumps({
        "events": [
            {
                "title": "Event A",
                "event_type": "delay",
                "description": "Description A",
                "affected_entity_name": "Entity A",
                "severity": "low",
            },
            {
                "title": "Event B",
                "event_type": "risk",
                "description": "Description B",
                "affected_entity_name": "Entity B",
                "severity": "critical",
            },
        ]
    })

    result = EventParser.parse(raw)

    assert len(result.events) == 2
    assert result.events[0].title == "Event A"
    assert result.events[1].title == "Event B"


def test_parse_empty_events():
    """EventParser should handle an empty events list."""

    raw = json.dumps({"events": []})

    result = EventParser.parse(raw)

    assert len(result.events) == 0


def test_parse_invalid_json():
    """EventParser should raise an error for invalid JSON."""

    with pytest.raises(json.JSONDecodeError):
        EventParser.parse("not valid json")
