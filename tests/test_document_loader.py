from backend.ingestion.loader_factory import LoaderFactory


def test_text_loader():

    loader = LoaderFactory.create(
        "demo_data/sample_document.txt"
    )

    text = loader.load(
        "demo_data/sample_document.txt"
    )

    assert "Generator G-12" in text

    assert "Cummins" in text