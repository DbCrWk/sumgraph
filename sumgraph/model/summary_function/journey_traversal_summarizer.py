"""
This module converts a DynamicWeightedGraph into a SummaryGraph by computing
participation in shortest journeys.
"""

from __future__ import annotations
import math
from sumgraph.helper.source_shortest_paths_dynamic_graph import (
    source_shorest_paths_dynamic_graph,
)
from sumgraph.data_handler.data_accessor.distances_soap_accessor import (
    DistancesSoapAccessor,
)
from sumgraph.data_handler.data_adapter.distances_soap_to_dynamic_weighted_graph_adapter import (
    DistancesSoapToDynamicWeightedGraphAdapter,
)
from typing import Callable, Dict, List, Optional, Set
from sumgraph.model.dynamic_weighted_graph.convention_enum import ConventionEnum
from sumgraph.model.dynamic_weighted_graph.dynamic_weighted_graph import (
    DynamicWeightedGraph,
)
from sumgraph.model.summary_graph.summary_graph import SummaryGraph
from sumgraph.helper.find_integral_bound import find_integral_bound


class JourneyTraversalSummarizer:
    """
    This class implements the algorithm to compute participation in shortest
    journeys.
    """

    def __init__(self, dynamic_weighted_graph: DynamicWeightedGraph) -> None:
        if dynamic_weighted_graph.convention is not ConventionEnum.TRAVERSAL_TIME:
            raise ValueError(
                "journey traversal summarization only works with the traversal time convention"
            )

        self._dwg: DynamicWeightedGraph = dynamic_weighted_graph
        self._summary: SummaryGraph

    @property
    def summary(self) -> SummaryGraph:
        """
        The summary graph produced by summarization
        """
        return self._summary

    def summarize(self) -> JourneyTraversalSummarizer:
        """
        Perform summarization
        """

        self._summary = JourneyTraversalSummarizer.summarize_dynamic_weighted_graph(
            self._dwg
        )

        return self

    @staticmethod
    def summarize_dynamic_weighted_graph(
        dynamic_weighted_graph: DynamicWeightedGraph,
    ) -> SummaryGraph:
        """
        Perform summarization on the input graph
        """

        summary_graph = SummaryGraph(
            name="summary graph from journey traversal summarizer"
        )

        start_time = 0
        end_time = 86400
        iterations = 1000
        time_diff = (end_time - start_time) / iterations
        time_fraction = 1 / iterations

        for vertex in dynamic_weighted_graph.vertex_set:
            summary_graph.add_vertex(vertex=vertex)

        for time_step in range(iterations):
            current_time = (time_diff * time_step) + start_time

            print("starting iteration", time_step, current_time)

            for vertex in dynamic_weighted_graph.vertex_set:
                paths = source_shorest_paths_dynamic_graph(
                    dynamic_weighted_graph=dynamic_weighted_graph,
                    source_vertex=vertex,
                    start_time=current_time,
                )

                for _, path in paths.items():
                    for index, ver in enumerate(path):
                        is_last_index = index == len(path) - 1
                        if is_last_index:
                            break

                        source_vertex_in_edge = ver
                        target_vertex_in_edge = path[index + 1]

                        curr_weight = summary_graph.get_edge_weight(
                            source_vertex=source_vertex_in_edge,
                            target_vertex=target_vertex_in_edge,
                        )

                        summary_graph.set_edge_weight(
                            source_vertex=source_vertex_in_edge,
                            target_vertex=target_vertex_in_edge,
                            weight=curr_weight + time_fraction,
                        )

        return summary_graph


if __name__ == "__main__":
    accessor = DistancesSoapAccessor(
        filepath="/Users/dev.dabke/OneDrive - Princeton University/Documents/research/code/research/nasa-average-graphs/.data/Distances for 7_29_2021.csv"
    )
    adapter = DistancesSoapToDynamicWeightedGraphAdapter(accessor=accessor)
    dwg = adapter.adapt().dynamic_weighted_graph
    summarizer = JourneyTraversalSummarizer(dynamic_weighted_graph=dwg).summarize()

    print(summarizer.summary)
