"""
This module accepts ConnectionsSoapData and return zigzag persistence
"""


from typing import Iterable, List, Tuple
import dionysus  # type: ignore
from sumgraph.data_handler.data_accessor.data_type import ConnectionsSoapAccessorData
from sumgraph.data_handler.data_accessor.connections_soap_accessor import (
    ConnectionsSoapAccessor,
)


ZigzagType = Iterable[str]

PointType = Tuple[float, float]
DiagramType = List[PointType]
DiagramsType = Iterable[DiagramType]


class ConnectionsSoapToZigzagAdapter:
    """
    This class converts ConnectionsSoapData to zigzag persistence
    """

    def __init__(self, accessor: ConnectionsSoapAccessor) -> None:
        self._accessor = accessor
        self._accessor.run()

    def adapt(self) -> Tuple[ZigzagType, DiagramsType]:
        """
        Perform the adaptation
        """
        data = self._accessor.data

        return ConnectionsSoapToZigzagAdapter.adapt_data_to_model(data=data)

    @staticmethod
    def adapt_data_to_model(
        data: ConnectionsSoapAccessorData,
    ) -> Tuple[ZigzagType, DiagramsType]:
        """
        Mehtod for adapting data
        """
        simplex: List[List[int]] = []
        times: List[List[float]] = []

        # First, we need to add all of the vertices as 0-dimensional simplices
        for index, _ in enumerate(data["satellites"]):
            simplex.append([index])
            times.append([0])

        for source in data["connections"]:
            for target in data["connections"][source]:
                source_to_target_connections = data["connections"][source][target]

                source_index = data["satellites"].index(source)
                target_index = data["satellites"].index(target)

                # If we have already added [target, source], we cannot add it
                # again, or dionysus will throw a segmentation fault
                if [target_index, source_index] in simplex:
                    continue

                simplex.append([source_index, target_index])

                simplex_times: List[float] = []

                for (rise_time, set_time) in source_to_target_connections:
                    simplex_times.append(rise_time)
                    simplex_times.append(set_time)

                times.append(simplex_times)

        filtration = dionysus.Filtration(  # type: ignore # pylint: disable=no-member
            simplex
        )
        return dionysus.zigzag_homology_persistence(filtration, times)  # type: ignore # pylint: disable=no-member
