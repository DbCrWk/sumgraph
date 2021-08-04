"""
This module tests the DynamicWeightedGraphh class for all operations
"""

from sumgraph.model.dynamic_weighted_graph import DynamicWeightedGraphh


def test_constructor():
    """
    Verify that the constructor works as intended
    """

    dwg = DynamicWeightedGraphh(name="test")
    assert dwg.name == "test"
