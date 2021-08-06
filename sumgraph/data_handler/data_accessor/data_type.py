"""
The modules provides type information on the data provided by data accessors.
"""

from typing import Dict, List, TypedDict


SatelliteName = str
VisibilityPercentage = float


class ParedDownSoapAccessorData(TypedDict):
    """
    This class is a type declaration for the data provided by ParedDownSoapAccessor
    """

    satellites: List[SatelliteName]
    visibility: Dict[SatelliteName, Dict[SatelliteName, VisibilityPercentage]]
