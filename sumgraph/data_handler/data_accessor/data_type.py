"""
The modules provides type information on the data provided by data accessors.
"""

from typing import Dict, List, TypedDict, Union


SatelliteName = str
VisibilityPercentage = float


class ParedDownSoapAccessorData(TypedDict):
    """
    This class is a type declaration for the data provided by ParedDownSoapAccessor
    """

    satellites: List[SatelliteName]
    visibility: Dict[SatelliteName, Dict[SatelliteName, VisibilityPercentage]]


class DistancesSoapAccessorData(TypedDict):
    """
    This class is a type declaration for the data provided by DistancesSoapAccessor
    """

    satellites: List[SatelliteName]
    distances: Dict[SatelliteName, Dict[SatelliteName, List[float]]]
    distance_sample_timestamps: List[float]


AccessorData = Union[
    ParedDownSoapAccessorData,
    DistancesSoapAccessorData,
]
