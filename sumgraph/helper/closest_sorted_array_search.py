"""
This module searches through a sorted array and returns the index and value of
the closest entry in the array.
"""


from typing import List, Tuple


def closest_sorted_array_search(array: List[float], target: float) -> Tuple[int, float]:
    """
    Find the closest value in a sorted array of a specified target. Returns the index and value
    """

    array_length = len(array)

    if array_length == 0:
        raise ValueError("array is empty")

    if array_length == 1:
        return (0, array[0])

    middle_index = int(array_length / 2)
    middle_value = array[middle_index]

    if target > middle_value:
        (right_index, right_value) = closest_sorted_array_search(
            array=array[middle_index:], target=target
        )

        middle_diff = abs(middle_value - target)
        right_diff = abs(right_value - target)

        if middle_diff > right_diff:
            return (right_index + middle_index, right_value)

    if target < middle_value:
        (left_index, left_value) = closest_sorted_array_search(
            array=array[0:middle_index], target=target
        )

        middle_diff = abs(middle_value - target)
        left_diff = abs(left_value - target)

        if middle_diff > left_diff:
            return (left_index, left_value)

    return (middle_index, middle_value)
