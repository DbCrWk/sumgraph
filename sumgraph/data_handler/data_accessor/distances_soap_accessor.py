"""
This module handles distances data from SOAP.
"""

import linecache
from typing import Dict, List, Tuple
import pandas as pd
from sumgraph.data_handler.data_accessor.data_type import (
    DistancesSoapAccessorData,
    SatelliteName,
)
from sumgraph.data_handler.data_accessor.file_based_accessor import FileBasedAccessor
from sumgraph.logger.logger import setup_logger


logger = setup_logger(__name__)

HEADER_PREFIX_FOR_SATELLITE_NAME = "Dist:"
SEPARATOR_FOR_SATELLITE_NAMES = "_"


class DistancesSoapAccessor(FileBasedAccessor):
    """
    The DistancesSoapAccessor accepts distances data from SOAP that is an
    augmented csv file of sampled satellite-to-satellite link distance data.
    """

    def __init__(self, filepath: str) -> None:
        super().__init__(filepath)
        self._dataframe: pd.DataFrame
        self._data: DistancesSoapAccessorData = {
            "satellites": [],
            "distances": {},
            "distance_sample_timestamps": [],
        }

    @property
    def data(self) -> DistancesSoapAccessorData:
        """
        The main data for this accessor
        """
        return self._data

    def run_read_file(self):
        """
        This method reads in the datafile
        """

        # Certain lines of the original file cannot be parsed, so we handle them
        # specifically and skip them when importing through pandas:
        #   0: the header row that defines the file
        #   1: the row that gives the timestamp of when the data is for
        #   2: a blank line
        #   3: the row that gives the timestamp of when the data was generated
        #   4: the start and stop time of the simulation
        #   6: the line that defines what units the data is in
        skiprows = [0, 1, 2, 3, 4, 6]

        header_row = linecache.getline(
            filename=self.filepath, lineno=0 + 1
        )  # lineno indexing begins at 1, not 0
        logger.info("parsing distances SOAP file: %s", header_row)

        # We have to drop the last column of data, as it is not valid data
        self._dataframe = pd.read_csv(  # type: ignore
            filepath_or_buffer=self._filepath, skiprows=skiprows
        ).iloc[:, :-1]

        return self

    def run_analyze_file(self):
        """
        This method converts the dataframe into data
        """

        self._data = DistancesSoapAccessor.convert_dataframe_to_data(self._dataframe)

        return self

    @staticmethod
    def convert_dataframe_to_data(dataframe: pd.DataFrame) -> DistancesSoapAccessorData:
        """
        This method converts a datafram into the data expcted from this class
        """

        # Skip the first column, as this corresponds to samples
        columns_with_satellite_distances: List[str] = list(dataframe.columns[1:])

        # 1. Get the names of satellites
        satellites_nested_arrays = [
            DistancesSoapAccessor.extract_satellite_names_from_header(x)
            for x in columns_with_satellite_distances
        ]
        satellite_names_with_duplicates = [
            item for sublist in satellites_nested_arrays for item in sublist
        ]
        satellites: List[SatelliteName] = list(set(satellite_names_with_duplicates))

        # 2. Extract pairwise distance data
        distances: Dict[SatelliteName, Dict[SatelliteName, List[float]]] = {}
        for column_header in columns_with_satellite_distances:
            (
                source,
                target,
            ) = DistancesSoapAccessor.extract_satellite_names_from_header(column_header)
            distance_list: List[float] = list(dataframe[column_header])

            if source not in distances:
                distances[source] = {}

            if target not in distances:
                distances[target] = {}

            distances[source][target] = distance_list
            distances[target][source] = distance_list

        # 3. Get the sample timestamps
        distance_sample_timestamps: List[float] = list(dataframe["TIME_UNITS"])

        data: DistancesSoapAccessorData = {
            "satellites": satellites,
            "distances": distances,
            "distance_sample_timestamps": distance_sample_timestamps,
        }

        return data

    @staticmethod
    def extract_satellite_names_from_header(
        header: str,
    ) -> Tuple[SatelliteName, SatelliteName]:
        """
        This method extracts the two satellite names from the header of a column
        """
        stripped_header = header[len(HEADER_PREFIX_FOR_SATELLITE_NAME) :]
        satellite_names = stripped_header.split(SEPARATOR_FOR_SATELLITE_NAMES)

        if len(satellite_names) != 2:
            raise ValueError("could not parse header: %s" % header)

        source = satellite_names[0]
        target = satellite_names[1]

        return (source, target)
