"""
This module contains the DynamicWeightedGraphh class, which is the main data
structure for a weighted graph that is dynamic.
"""

from typing import Set


class DynamicWeightedGraphh:
    """
    The main DynamicWeightedGraphh class
    """

    name: str
    vertex_set: Set[str]

    def __init__(self, name: str) -> None:
        self.name = name

    def add_vertex(self, vertex: str) -> str:
        """
        This method adds a vertex to the vertex set
        """

        if vertex in self.vertex_set:
            raise ValueError("vertex %s is already in vertex_set" % vertex)

        self.vertex_set.add(vertex)

        return vertex

    def has_vertex(self, vertex: str) -> bool:
        """
        This method verifies if a vertex exists on the vertex set
        """

        return vertex in self.vertex_set
