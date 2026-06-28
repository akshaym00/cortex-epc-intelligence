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
class RelationshipType(str, Enum):
    """
    Defines how two entities are connected
    inside the Living Project Model.
    """

    DEPENDS_ON = "depends_on"

    REQUIRES = "requires"

    SUPPLIES = "supplies"

    INSTALLED_BY = "installed_by"

    OWNED_BY = "owned_by"

    MODIFIES = "modifies"

    REFERENCES = "references"

    GENERATES = "generates"

    MITIGATES = "mitigates"

    AFFECTS = "affects"

    LOCATED_IN = "located_in"

    APPROVED_BY = "approved_by"

    TRIGGERS = "triggers"

    PART_OF = "part_of"

    CAUSED_BY = "caused_by"