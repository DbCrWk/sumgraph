from typing import Set


class DynamicWeightedGraphh:
    name: str
    vertex_set: Set[str]

    def __init__(self, name: str) -> None:
        self.name = name

    def add_vertex(self, vertex: str) -> str:
        if vertex in self.vertex_set:
            raise ValueError("vertex %s is already in vertex_set" % vertex)

        self.vertex_set.add(vertex)

        return vertex

    def has_vertex(self, vertex: str) -> bool:
        return vertex in self.vertex_set
