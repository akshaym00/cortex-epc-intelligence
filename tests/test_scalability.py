from demo.scalability_benchmark import run_benchmark


def test_graph_core_handles_hackathon_scale():
    result = run_benchmark()

    assert result["entities"] == 15_200
    assert result["relationships"] >= 29_900
    assert result["downstream_entities"] == 14_999
