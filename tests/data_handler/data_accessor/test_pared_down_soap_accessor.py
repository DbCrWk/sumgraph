"""
This module tests the ParedDownSoapAccessor
"""
import pandas as pd

from sumgraph.data_handler.data_accessor.pared_down_soap_accessor import (
    DataFrameRow,
    ParedDownSoapAccessor,
)


def test_constructor():
    """
    Verify that the constructor works
    """
    accessor = ParedDownSoapAccessor(filepath="./test.csv")

    assert accessor is not None


def test_extract_satellite_names_from_analysis_label():
    """
    Verify that extract_satellite_names_from_analysis_label works
    """
    label = "A sees B"
    (
        source,
        target,
    ) = ParedDownSoapAccessor.extract_satellite_names_from_analysis_label(
        analysis_label=label
    )

    assert source == "A"
    assert target == "B"


def test_extract_visibility_from_analysis_row():
    """
    Verify that extract_visibility_from_analysis_row works
    """
    row: DataFrameRow = {"Analysis": "A sees B", "Percent True": "31.64%"}

    (
        source,
        target,
        percent_true,
    ) = ParedDownSoapAccessor.extract_visibility_from_analysis_row(row=row)

    assert source == "A"
    assert target == "B"
    assert percent_true == 31.64


def test_convert_dataframe_to_data():
    """
    Verify that convert_dataframe_to_data works
    """
    dataframe = pd.read_csv(  # type: ignore
        filepath_or_buffer="tests/data_handler/data_accessor/$.fixture/sample_soap_pared_down.csv"
    )

    (
        actual_satellites,
        actual_visibility,
    ) = ParedDownSoapAccessor.convert_dataframe_to_data(
        dataframe=dataframe  # type: ignore
    )

    expected_satellites = [
        "MRO",
        "Guam",
        "White Sands",
        "TDRS 10",
        "TDRS 12",
        "TDRS 13",
        "Canberra",
        "TDRS 8",
        "LRO",
        "Madrid",
        "Goldstone",
    ]
    assert len(actual_satellites) == len(expected_satellites)
    assert actual_satellites.sort() == expected_satellites.sort()

    expected_visibility = {
        "LRO": {
            "LRO": 0.0,
            "Madrid": 25.92,
            "White Sands": 0.0,
            "TDRS 10": 63.22,
            "Canberra": 30.64,
            "TDRS 13": 61.01,
            "Goldstone": 32.33,
            "Guam": 0.0,
            "MRO": 35.83,
            "TDRS 8": 63.2,
            "TDRS 12": 63.7,
        },
        "Madrid": {
            "LRO": 25.92,
            "Madrid": 0.0,
            "White Sands": 0.0,
            "TDRS 10": 0.0,
            "Canberra": 0.0,
            "TDRS 13": 100.0,
            "Goldstone": 0.0,
            "Guam": 0.0,
            "MRO": 0.0,
            "TDRS 8": 0.0,
            "TDRS 12": 100.0,
        },
        "White Sands": {
            "LRO": 0.0,
            "Madrid": 0.0,
            "White Sands": 0.0,
            "TDRS 10": 100.0,
            "Canberra": 0.0,
            "TDRS 13": 0.0,
            "Goldstone": 0.0,
            "Guam": 0.0,
            "MRO": 0.0,
            "TDRS 8": 0.0,
            "TDRS 12": 100.0,
        },
        "TDRS 10": {
            "LRO": 63.22,
            "Madrid": 0.0,
            "White Sands": 100.0,
            "TDRS 10": 0.0,
            "Canberra": 100.0,
            "TDRS 13": 100.0,
            "Goldstone": 100.0,
            "Guam": 100.0,
            "MRO": 0.0,
            "TDRS 8": 100.0,
            "TDRS 12": 100.0,
        },
        "Canberra": {
            "LRO": 30.64,
            "Madrid": 0.0,
            "White Sands": 0.0,
            "TDRS 10": 100.0,
            "Canberra": 0.0,
            "TDRS 13": 0.0,
            "Goldstone": 0.0,
            "Guam": 0.0,
            "MRO": 28.01,
            "TDRS 8": 100.0,
            "TDRS 12": 0.0,
        },
        "TDRS 13": {
            "LRO": 61.01,
            "Madrid": 100.0,
            "White Sands": 0.0,
            "TDRS 10": 100.0,
            "Canberra": 0.0,
            "TDRS 13": 0.0,
            "Goldstone": 0.0,
            "Guam": 0.0,
            "MRO": 0.0,
            "TDRS 8": 100.0,
            "TDRS 12": 100.0,
        },
        "Goldstone": {
            "LRO": 32.33,
            "Madrid": 0.0,
            "White Sands": 0.0,
            "TDRS 10": 100.0,
            "Canberra": 0.0,
            "TDRS 13": 0.0,
            "Goldstone": 0.0,
            "Guam": 0.0,
            "MRO": 0.0,
            "TDRS 8": 0.0,
            "TDRS 12": 100.0,
        },
        "Guam": {
            "LRO": 0.0,
            "Madrid": 0.0,
            "White Sands": 0.0,
            "TDRS 10": 100.0,
            "Canberra": 0.0,
            "TDRS 13": 0.0,
            "Goldstone": 0.0,
            "Guam": 0.0,
            "MRO": 0.0,
            "TDRS 8": 100.0,
            "TDRS 12": 0.0,
        },
        "MRO": {
            "LRO": 35.83,
            "Madrid": 0.0,
            "White Sands": 0.0,
            "TDRS 10": 0.0,
            "Canberra": 28.01,
            "TDRS 13": 0.0,
            "Goldstone": 0.0,
            "Guam": 0.0,
            "MRO": 0.0,
            "TDRS 8": 0.0,
            "TDRS 12": 0.0,
        },
        "TDRS 8": {
            "LRO": 63.2,
            "Madrid": 0.0,
            "White Sands": 0.0,
            "TDRS 10": 100.0,
            "Canberra": 100.0,
            "TDRS 13": 100.0,
            "Goldstone": 0.0,
            "Guam": 100.0,
            "MRO": 0.0,
            "TDRS 8": 0.0,
            "TDRS 12": 100.0,
        },
        "TDRS 12": {
            "LRO": 63.7,
            "Madrid": 100.0,
            "White Sands": 100.0,
            "TDRS 10": 100.0,
            "Canberra": 0.0,
            "TDRS 13": 100.0,
            "Goldstone": 100.0,
            "Guam": 0.0,
            "MRO": 0.0,
            "TDRS 8": 100.0,
            "TDRS 12": 0.0,
        },
    }
    assert actual_visibility == expected_visibility
