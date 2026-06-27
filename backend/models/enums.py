from enum import Enum


class EntityType(str, Enum):
    """
    Represents every type of object that can exist
    inside a project.
    """

    PROJECT = "project"

    EQUIPMENT = "equipment"

    SYSTEM = "system"

    TASK = "task"

    MILESTONE = "milestone"

    VENDOR = "vendor"

    CONTRACTOR = "contractor"

    TEAM = "team"

    PERSON = "person"

    DOCUMENT = "document"

    RISK = "risk"

    EVENT = "event"

    ISSUE = "issue"

    APPROVAL = "approval"

    LOCATION = "location"