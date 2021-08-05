"""
This module defines the type for an edge weight function, as well as exporting
some default functions based on convention
"""

import math
from typing import Callable
from sumgraph.model.dynamic_weighted_graph.convention_enum import ConventionEnum


EdgeWeightFn = Callable[[float], float]


def traversal_time_default_edge_weight(_: float) -> float:
    """
    For a traversal time default, we assume the edge does not exist: this
    results in a traversal time of positive infinity.
    """
    return math.inf


def cost_default_edge_weight(_: float) -> float:
    """
    For a cost default, we assume the edge does not exist: this results in a
    cost of positive infinity.
    """
    return math.inf


def capacity_default_edge_weight(_: float) -> float:
    """
    For a capacity default, we assume the edge does not exist: this results in a
    capacity of 0.
    """
    return 0


def get_default_edge_weight_fn(convention: ConventionEnum) -> EdgeWeightFn:
    """
    This function accepts a convention and returns a default edge weight
    function.
    """

    if convention == ConventionEnum.TRAVERSAL_TIME:
        return traversal_time_default_edge_weight

    if convention == ConventionEnum.COST:
        return cost_default_edge_weight

    return capacity_default_edge_weight
