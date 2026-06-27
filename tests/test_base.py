from backend.models.base import CortexBaseModel


def test_base_model_creation():
    obj = CortexBaseModel()

    assert obj.id is not None
    assert obj.created_at is not None
    assert obj.updated_at is not None
    assert obj.metadata == {}