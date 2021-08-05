"""
This module tests the DynamicWeightedGraph class for all operations
"""

from sumgraph.model.dynamic_weighted_graph.convention_enum import ConventionEnum
from sumgraph.model.dynamic_weighted_graph.dynamic_weighted_graph import (
    DynamicWeightedGraph,
)


def test_constructor():
    """
    Verify that the constructor works as intended
    """

    dwg = DynamicWeightedGraph(
        name="test", convention=ConventionEnum.CAPACITY, directed=True
    )
    assert dwg.name == "test"
    assert dwg.convention == ConventionEnum.CAPACITY
    assert dwg.directed is True
