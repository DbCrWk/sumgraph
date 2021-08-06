"""
This module contains the ParedDownSoapAccessor.
"""

from enum import Enum
from typing import Dict, Iterable, List, Tuple, TypedDict
import pandas as pd
from sumgraph.data_handler.data_accessor.data_type import (
    ParedDownSoapAccessorData,
    SatelliteName,
)


class DataFrameColumn(Enum):
    """
    This enum captures the important columns of the dataframe parsed in a data
    file.
    """

    ANALYSIS = "Analysis"
    PERCENT_TRUE = "Percent True"


DataFrameRow = TypedDict("DataFrameRow", {"Analysis": str, "Percent True": float})


class ParedDownSoapAccessor:
    """
    The ParedDownSoapAccessor accepts pared down soap data that is a csv file of
    satellite-to-satellite link uptime data.
    """

    _filepath: str
    _dataframe: pd.DataFrame
    data: ParedDownSoapAccessorData

    def __init__(self, filepath: str):
        self._filepath = filepath
        self.data = {"satellites": [], "visibility": {}}

    def run(self):
        """
        The main method to run data extraction and analysis
        """
        self.run_read_file().run_analyze_file()

        return self

    def run_read_file(self):
        """
        This method reads the passed datafile
        """
        self._dataframe = pd.read_csv(filepath_or_buffer=self._filepath)  # type: ignore

        return self

    def run_analyze_file(self):
        """
        This method converts the read file into usable data
        """
        (satellites, visibility) = ParedDownSoapAccessor.convert_dataframe_to_data(
            self._dataframe
        )

        self.data["satellites"] = satellites
        self.data["visibility"] = visibility

        return self

    @staticmethod
    def convert_dataframe_to_data(
        dataframe: pd.DataFrame,
    ) -> Tuple[List[str], Dict[SatelliteName, Dict[SatelliteName, float]]]:
        """
        This method converts a dataframe read from a file into the correct data
        format for this accessor
        """

        # First produce the name of the satellites
        satellite_name_column: List[str] = list(dataframe[DataFrameColumn.ANALYSIS])
        satellites_nested_arrays = [
            ParedDownSoapAccessor.extract_satellite_names_from_analysis_label(x)
            for x in satellite_name_column
        ]
        satellite_names_with_duplicates = [
            item for sublist in satellites_nested_arrays for item in sublist
        ]
        satellites = list(set(satellite_names_with_duplicates))

        # Next, produce the visibility data
        visibility: Dict[SatelliteName, Dict[SatelliteName, float]] = {}
        for i in satellites:
            for j in satellites:
                visibility[i][j] = 0.0
                visibility[j][i] = 0.0

        dataframe_iter: Iterable[Tuple[int, DataFrameRow]] = dataframe.iterrows()  # type: ignore
        for _, row in dataframe_iter:
            (
                source,
                target,
                visibility_percent,
            ) = ParedDownSoapAccessor.extract_visibility_from_analysis_row(row)
            visibility[source][target] = visibility_percent

        # Return the data
        return (satellites, visibility)

    @staticmethod
    def extract_satellite_names_from_analysis_label(analysis_label: str) -> List[str]:
        """
        This method accepts a label from the "Analysis" column of the data and
        returns a tuple of the underlying satellite names
        """
        return analysis_label.split(" sees ")

    @staticmethod
    def extract_visibility_from_analysis_row(
        row: DataFrameRow,
    ) -> Tuple[SatelliteName, SatelliteName, float]:
        """
        This method extracts visibility data from a row
        """
        (
            source,
            target,
        ) = ParedDownSoapAccessor.extract_satellite_names_from_analysis_label(
            row["Analysis"]
        )
        percent_true = row["Percent True"]

        return (source, target, percent_true)
