"""
This module contains the algorithm for finding shortest paths for a source
vertex in a dynamic weighted graph
"""

import math
from typing import Callable, Dict, List, Optional, Set, Tuple
from sumgraph.model.dynamic_weighted_graph.dynamic_weighted_graph import (
    DynamicWeightedGraph,
)
from sumgraph.helper.find_integral_bound import find_integral_bound


def get_integrable_fn(
    dynamic_weighted_graph: DynamicWeightedGraph, source: str, target: str
) -> Callable[[float], float]:
    edge_weight_fn = dynamic_weighted_graph.get_edge_weight_fn(
        source_vertex=source,
        target_vertex=target,
    )

    def integrable_fn(input_x: float) -> float:
        val = edge_weight_fn(input_x)
        if math.isinf(val):
            return 0

        return val

    return integrable_fn


def initialize(
    dynamic_weighted_graph: DynamicWeightedGraph,
    source_vertex: str,
    start_time: float,
) -> Tuple[Dict[str, float], Dict[str, Optional[str]]]:
    lengths: Dict[str, float] = {}
    predecessor: Dict[str, Optional[str]] = {}

    for vertex in dynamic_weighted_graph.vertex_set:
        if vertex == source_vertex:
            lengths[vertex] = start_time
        else:
            lengths[vertex] = math.inf

        predecessor[vertex] = None

    return (lengths, predecessor)


def populate_lengths_and_predecessor(
    dynamic_weighted_graph: DynamicWeightedGraph,
    source_vertex: str,
    lengths: Dict[str, float],
    predecessor: Dict[str, Optional[str]],
) -> None:
    finalized: Set[str] = set()

    # Run algorithm
    while len(finalized) < len(dynamic_weighted_graph.vertex_set):
        unfinalized = dynamic_weighted_graph.vertex_set.difference(finalized)
        current_vertex = min(unfinalized, key=(lambda k: lengths[k]))

        current_length = lengths[current_vertex]
        finalized.add(current_vertex)

        for target in dynamic_weighted_graph.vertex_set:
            traversal_time = find_integral_bound(
                integrable_function=get_integrable_fn(
                    dynamic_weighted_graph=dynamic_weighted_graph,
                    source=source_vertex,
                    target=target,
                ),
                lower_bound=current_length,
                target_value=1,
            )

            if current_length + traversal_time < lengths[target]:
                lengths[target] = current_length + traversal_time
                predecessor[target] = source_vertex


def get_paths(
    dynamic_weighted_graph: DynamicWeightedGraph,
    source_vertex: str,
    predecessor: Dict[str, Optional[str]],
):
    paths: Dict[str, List[str]] = {}

    for vertex in dynamic_weighted_graph.vertex_set:
        paths[vertex] = []

        curr_pred = predecessor[vertex]
        if curr_pred is None:
            continue

        paths[vertex].append(vertex)
        curr_vertex = vertex
        while curr_pred != source_vertex:
            paths[vertex].append(curr_pred)
            curr_vertex = curr_pred
            test_pred = predecessor[curr_vertex]

            if test_pred is None:
                raise ValueError(
                    "somehow, a predecessor is None for %s with curr %s and pred %s"
                    % (vertex, curr_vertex, curr_pred)
                )

            curr_pred = test_pred

        paths[vertex].append(source_vertex)

        paths[vertex].reverse()

    return paths


def source_shorest_paths_dynamic_graph(
    dynamic_weighted_graph: DynamicWeightedGraph,
    source_vertex: str,
    start_time: float,
) -> Dict[str, List[str]]:
    """
    This method provides the shortest path from a source vertex to every other
    vertex. It returns the list of vertices in the shortest path for each target
    vertex.
    """
    if not dynamic_weighted_graph.has_vertex(vertex=source_vertex):
        raise ValueError("vertex %s not found in graph" % source_vertex)

    (lengths, predecessor) = initialize(
        dynamic_weighted_graph=dynamic_weighted_graph,
        source_vertex=source_vertex,
        start_time=start_time,
    )

    populate_lengths_and_predecessor(
        dynamic_weighted_graph=dynamic_weighted_graph,
        source_vertex=source_vertex,
        lengths=lengths,
        predecessor=predecessor,
    )

    paths = get_paths(
        dynamic_weighted_graph=dynamic_weighted_graph,
        source_vertex=source_vertex,
        predecessor=predecessor,
    )

    return paths
