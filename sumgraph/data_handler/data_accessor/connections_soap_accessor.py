"""
This module handles SOAP data that tracks connections between satellites.
"""

import linecache
from typing import Dict, List, Tuple
import pandas as pd
from sumgraph.data_handler.data_accessor.data_type import (
    ConnectionsSoapAccessorData,
    SatelliteName,
)
from sumgraph.data_handler.data_accessor.file_based_accessor import FileBasedAccessor
from sumgraph.logger.logger import setup_logger


logger = setup_logger(__name__)

SEPARATOR_FOR_SATELLITE_NAMES = " sees "


class ConnectionsSoapAccessor(FileBasedAccessor):
    """
    This class is an accessor for SOAP connections data
    """

    def __init__(self, filepath: str) -> None:
        super().__init__(filepath)
        self._dataframe: pd.DataFrame
        self._data: ConnectionsSoapAccessorData = {
            "satellites": [],
            "connections": {},
        }

    @property
    def data(self) -> ConnectionsSoapAccessorData:
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

        # We only keep the first four columns, as we do not need the adjacency matrix
        dataframe: pd.DataFrame = pd.read_csv(  # type: ignore
            filepath_or_buffer=self._filepath, skiprows=skiprows
        ).iloc[:, 0:4]

        # This data also includes a matrix of seen values at the bottom that we need to get rid of
        indices_with_analysis: List[int] = dataframe.index[  # type: ignore
            dataframe["Analysis"] == "Analysis"
        ].tolist()
        if len(indices_with_analysis) != 1:
            raise ValueError(
                "datafile does not contain a unique secondary analysis block"
            )

        index_to_ignore_after = indices_with_analysis[0]
        self._dataframe = dataframe.iloc[0:index_to_ignore_after, :]

        return self

    def run_analyze_file(self):
        """
        This method converts the dataframe into data
        """

        self._data = ConnectionsSoapAccessor.convert_dataframe_to_data(self._dataframe)

        return self

    @staticmethod
    def convert_dataframe_to_data(
        dataframe: pd.DataFrame,
    ) -> ConnectionsSoapAccessorData:
        """
        This method converts a datafram into the data expcted from this class
        """

        satellites: List[str] = []
        connections: Dict[
            SatelliteName, Dict[SatelliteName, List[Tuple[float, float]]]
        ] = {}

        # Parse headers to get satellite names
        headers: List[str] = list(dataframe["Analysis"])
        for header in headers:
            (
                source,
                target,
            ) = ConnectionsSoapAccessor.extract_satellite_names_from_header(header)

            if source not in satellites:
                satellites.append(source)

            if target not in satellites:
                satellites.append(target)

            if source not in connections:
                connections[source] = {}

            if target not in connections:
                connections[target] = {}

        # Parse rows for rise/set times
        for _, row in dataframe.iterrows():
            (
                source,
                target,
            ) = ConnectionsSoapAccessor.extract_satellite_names_from_header(
                row["Analysis"]  # type: ignore
            )
            rise_time: float = float(row["Rise"])  # type: ignore
            set_time: float = float(row["Set"])  # type: ignore
            time_tuple: Tuple[float, float] = (rise_time, set_time)

            if target not in connections[source]:
                connections[source][target] = []

            if source not in connections[target]:
                connections[target][source] = []

            connections[source][target].append(time_tuple)
            connections[target][source].append(time_tuple)

        return {"satellites": satellites, "connections": connections}

    @staticmethod
    def extract_satellite_names_from_header(
        header: str,
    ) -> Tuple[SatelliteName, SatelliteName]:
        """
        This method extracts the two satellite names from the header of a column
        """
        satellite_names = header.split(SEPARATOR_FOR_SATELLITE_NAMES)

        if len(satellite_names) != 2:
            raise ValueError("could not parse header: %s" % header)

        source = satellite_names[0]
        target = satellite_names[1]

        return (source, target)
