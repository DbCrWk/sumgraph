"""
This module converts DistancesSoapData to a DynamicWeightedGraph.
"""

from sumgraph.data_handler.data_accessor.data_type import (
    DistancesSoapAccessorData,
    SatelliteName,
)
from sumgraph.data_handler.data_accessor.distances_soap_accessor import (
    DistancesSoapAccessor,
)
from sumgraph.model.dynamic_weighted_graph.dynamic_weighted_graph import (
    DynamicWeightedGraph,
)
from sumgraph.helper.closest_sorted_array_search import closest_sorted_array_search


class DistancesSoapToDynamicWeightedGraphAdapter:
    """
    This class converts DistancesSoapData to a DynamicWeightedGraph
    """

    def __init__(self, accessor: DistancesSoapAccessor):
        self._accessor = accessor
        self._accessor.run()

    def adapt(self) -> DynamicWeightedGraph:
        """
        Perform the conversion
        """
        data = self._accessor.data
        return DistancesSoapToDynamicWeightedGraphAdapter.adapt_data_to_model(data)

    @staticmethod
    def adapt_data_to_model(data: DistancesSoapAccessorData) -> DynamicWeightedGraph:
        """
        A method for performing the conversion of data to a dwg
        """
        satellites = data["satellites"]
        distances = data["distances"]
        distance_sample_times = data["distance_sample_timestamps"]

        dwg = DynamicWeightedGraph(name="distances_soap_graph")

        # 1. Add vertices
        for satellite in satellites:
            dwg.add_vertex(satellite)

        # 2. Add edge weights
        def get_weight_fn(source: SatelliteName, target: SatelliteName):
            def weight_fn(time: float) -> float:
                # 1. Find the closest time interval
                (index, _) = closest_sorted_array_search(
                    array=distance_sample_times, target=time
                )

                # 2. Use that index to return the correct value in the distances array
                return distances[source][target][index]

            return weight_fn

        for source in distances:
            for target in distances[source]:
                if dwg.has_edge_weight(source_vertex=source, target_vertex=target):
                    break

                weight_fn = get_weight_fn(source=source, target=target)
                dwg.define_edge_weight(
                    source_vertex=source,
                    target_vertex=target,
                    weight_function=weight_fn,
                )

        return dwg
