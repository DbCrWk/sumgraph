from sumgraph.model.dynamic_weighted_graph import DynamicWeightedGraphh


def test_constructor():
    dwg = DynamicWeightedGraphh(name="test")
    assert dwg.name == "test"
