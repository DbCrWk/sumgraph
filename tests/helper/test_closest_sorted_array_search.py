"""
This module tests the closest_sorted_array_search
"""

from sumgraph.helper.closest_sorted_array_search import closest_sorted_array_search


def test_basic():
    """
    A basic test
    """
    array = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
    target = 3.3

    expected_index = 2
    expected_value = 3.0

    (actual_index, actual_value) = closest_sorted_array_search(
        array=array, target=target
    )

    assert actual_index == expected_index
    assert actual_value == expected_value


def test_one_element_array():
    """
    A one-element array
    """
    array = [1.0]
    target = 5.0

    expected_index = 0
    expected_value = 1.0

    (actual_index, actual_value) = closest_sorted_array_search(
        array=array, target=target
    )

    assert actual_index == expected_index
    assert actual_value == expected_value
