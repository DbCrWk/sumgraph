"""
This module contains the ParedDownSoapAccessor.
"""

from typing import Dict, Iterable, List, Tuple, TypedDict
import pandas as pd
from sumgraph.data_handler.data_accessor.data_type import (
    ParedDownSoapAccessorData,
    SatelliteName,
    VisibilityPercentage,
)
from sumgraph.data_handler.data_accessor.file_based_accessor import FileBasedAccessor


DataFrameRow = TypedDict("DataFrameRow", {"Analysis": str, "Percent True": str})


class ParedDownSoapAccessor(FileBasedAccessor):
    """
    The ParedDownSoapAccessor accepts pared down soap data that is a csv file of
    satellite-to-satellite link uptime data.
    """

    def __init__(self, filepath: str) -> None:
        super().__init__(filepath)
        self._dataframe: pd.DataFrame
        self._data: ParedDownSoapAccessorData = {"satellites": [], "visibility": {}}

    @property
    def data(self) -> ParedDownSoapAccessorData:
        """
        The main data for this accessor
        """
        return self._data

    def run_read_file(self):
        """
        This method reads the passed datafile
        """
        self._dataframe = pd.read_csv(filepath_or_buffer=self.filepath)  # type: ignore

        return self

    def run_analyze_file(self):
        """
        This method converts the read file into usable data
        """
        self._data = ParedDownSoapAccessor.convert_dataframe_to_data(self._dataframe)

        return self

    @staticmethod
    def convert_dataframe_to_data(
        dataframe: pd.DataFrame,
    ) -> ParedDownSoapAccessorData:
        """
        This method converts a dataframe read from a file into the correct data
        format for this accessor
        """

        # First produce the name of the satellites
        satellite_name_column: List[str] = list(dataframe["Analysis"])
        satellites_nested_arrays = [
            ParedDownSoapAccessor.extract_satellite_names_from_analysis_label(x)
            for x in satellite_name_column
        ]
        satellite_names_with_duplicates = [
            item for sublist in satellites_nested_arrays for item in sublist
        ]
        satellites = list(set(satellite_names_with_duplicates))

        # Next, produce the visibility data
        visibility: Dict[SatelliteName, Dict[SatelliteName, VisibilityPercentage]] = {}
        for i in satellites:
            visibility[i] = {}

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
            visibility[target][source] = visibility_percent

        data: ParedDownSoapAccessorData = {
            "satellites": satellites,
            "visibility": visibility,
        }

        return data

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
        # The original format for the data is "xx.x%", so we need to remove the
        # % at the end and convert the remaining value to a float
        percent_true = float(row["Percent True"].rstrip("%"))

        return (source, target, percent_true)
