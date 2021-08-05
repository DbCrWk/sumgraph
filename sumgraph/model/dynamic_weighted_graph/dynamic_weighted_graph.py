"""
This module contains the DynamicWeightedGraph class, which is the main data
structure for a weighted graph that is dynamic.
"""

from typing import Dict, Set
from sumgraph.model.dynamic_weighted_graph.edge_weight_fn import (
    EdgeWeightFn,
    get_default_edge_weight_fn,
)
from sumgraph.model.dynamic_weighted_graph.convention_enum import ConventionEnum


class DynamicWeightedGraph:
    """
    The main DynamicWeightedGraph class
    """

    name: str
    directed: bool
    convention: ConventionEnum
    vertex_set: Set[str]
    edge_set: Dict[str, Dict[str, EdgeWeightFn]]

    def __init__(
        self,
        name: str,
        convention: ConventionEnum = ConventionEnum.TRAVERSAL_TIME,
        directed: bool = False,
    ) -> None:
        self.name = name
        self.directed = directed
        self.convention = convention
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

    def define_edge_weight(
        self, source_vertex: str, target_vertex: str, weight_function: EdgeWeightFn
    ) -> None:
        """
        This method places a function on an edge
        """
        if not self.has_vertex(vertex=source_vertex):
            raise ValueError("source vertex %s is not in graph" % source_vertex)

        if not self.has_vertex(vertex=target_vertex):
            raise ValueError("target vertex %s is not in graph" % target_vertex)

        if self.has_edge_weight(
            source_vertex=source_vertex, target_vertex=target_vertex
        ):
            raise ValueError(
                "edge weight already defined between %s and %s"
                % (source_vertex, target_vertex)
            )

        self.edge_set[source_vertex][target_vertex] = weight_function

        if not self.directed:
            self.edge_set[target_vertex][source_vertex] = weight_function

    def get_edge_weight_fn(
        self, source_vertex: str, target_vertex: str
    ) -> EdgeWeightFn:
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

        return get_default_edge_weight_fn(self.convention)
