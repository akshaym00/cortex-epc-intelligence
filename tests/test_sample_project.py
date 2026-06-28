from demo_data.sample_project import build_sample_project


def test_sample_project():

    project = build_sample_project()

    assert project.name == "Demo Data Center Project"

    assert len(project.entities) == 5

    assert len(project.relationships) == 4