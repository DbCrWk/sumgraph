"""
This module contains the CentralityMap class, which is the main data
structure for a list of vertices with weights
"""


from typing import Dict, Set


DEFAULT_VERTEX_WEIGHT = 0


class CentralityMap:
    """
    The main CentralityMap class
    """

    name: str
    vertex_set: Set[str]
    vertex_weights: Dict[str, float]

    def __init__(
        self,
        name: str,
    ) -> None:
        self.name = name
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
        self.vertex_weights[vertex] = DEFAULT_VERTEX_WEIGHT

        return vertex

    def set_vertex_weight(self, vertex: str, weight: float) -> str:
        """
        This method sets a vertex weight
        """

        if not self.has_vertex(vertex=vertex):
            raise ValueError("vertex %s not in vertex_set" % vertex)

        self.vertex_weights[vertex] = weight

        return vertex

    def get_vertex_weight(self, vertex: str) -> float:
        """
        This method gets a vertex weight
        """

        if not self.has_vertex(vertex=vertex):
            raise ValueError("vertex %s not in vertex_set" % vertex)

        return self.vertex_weights[vertex]
