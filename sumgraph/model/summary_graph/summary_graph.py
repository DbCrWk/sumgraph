"""
This module contains the SummaryGraph class, which is the main data
structure for a weighted, directed summary graph.
"""


from __future__ import annotations
from typing import Dict, Set


DEFAULT_EDGE_WEIGHT = 0


class SummaryGraph:
    """
    The main SummaryGraph class
    """

    name: str
    vertex_set: Set[str]
    edge_set: Dict[str, Dict[str, float]]

    def __init__(
        self,
        name: str,
    ) -> None:
        self.name = name
        self.edge_set = {}
        self.vertex_set = set()

    def has_vertex(self, vertex: str) -> bool:
        """
        This method verifies if a vertex exists on the vertex set
        """

        return vertex in self.vertex_set

    def add_vertex(self, vertex: str) -> str:
        """
        This method adds a vertex to the vertex set
        """

        if self.has_vertex(vertex=vertex):
            raise ValueError("vertex %s is already in vertex_set" % vertex)

        self.vertex_set.add(vertex)
        self.edge_set[vertex] = {}

        return vertex

    def has_edge_weight(self, source_vertex: str, target_vertex: str) -> bool:
        """
        This method checks if an edge weight function has been defined
        """

        if not self.has_vertex(vertex=source_vertex):
            return False

        if not self.has_vertex(vertex=target_vertex):
            return False

        return target_vertex in self.edge_set[source_vertex]

    def set_edge_weight(
        self, source_vertex: str, target_vertex: str, weight: float
    ) -> None:
        """
        This method places a function on an edge
        """
        if not self.has_vertex(vertex=source_vertex):
            raise ValueError("source vertex %s is not in graph" % source_vertex)

        if not self.has_vertex(vertex=target_vertex):
            raise ValueError("target vertex %s is not in graph" % target_vertex)

        self.edge_set[source_vertex][target_vertex] = weight

    def get_edge_weight(self, source_vertex: str, target_vertex: str) -> float:
        """
        This method gets the right edge weight function for a particular edge.
        If none has been defined, it will default to a reasonable function given
        the convention.
        """
        if not self.has_vertex(vertex=source_vertex):
            raise ValueError("source vertex %s is not in graph" % source_vertex)

        if not self.has_vertex(vertex=target_vertex):
            raise ValueError("target vertex %s is not in graph" % target_vertex)

        if self.has_edge_weight(
            source_vertex=source_vertex, target_vertex=target_vertex
        ):
            return self.edge_set[source_vertex][target_vertex]

        return DEFAULT_EDGE_WEIGHT

    def __add__(self, b_graph: SummaryGraph):
        """
        This method adds two summary graphs together
        """
        if self.vertex_set.difference(b_graph.vertex_set):
            raise ValueError("sets do not have same vertex sets and cannot be added")

        if b_graph.vertex_set.difference(self.vertex_set):
            raise ValueError("sets do not have same vertex sets and cannot be added")

        sum_graph = SummaryGraph(
            name="sum graph of two graphs %s + %s" % (self.name, b_graph.name)
        )

        for vertex in self.vertex_set:
            sum_graph.add_vertex(vertex=vertex)

        for source in self.vertex_set:
            for target in self.vertex_set:
                self_weight = self.get_edge_weight(
                    source_vertex=source,
                    target_vertex=target,
                )
                b_weight = b_graph.get_edge_weight(
                    source_vertex=source,
                    target_vertex=target,
                )

                sum_graph.set_edge_weight(
                    source_vertex=source,
                    target_vertex=target,
                    weight=self_weight + b_weight,
                )

        return sum_graph
