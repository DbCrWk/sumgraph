"""
This module tests the find_integral_bound function.
"""

from math import sqrt, inf
from typing import Callable
import pytest
from sumgraph.helper.find_integral_bound import find_integral_bound


def test_basic():
    """
    Perform a simple test
    """

    integrable_function: Callable[[float], float] = lambda x: x

    lower_bound = 0
    target_value = 1

    expected_upper_bound = sqrt(2)
    actual_upper_bound = find_integral_bound(
        integrable_function=integrable_function,
        lower_bound=lower_bound,
        target_value=target_value,
        numerical_options={"tolerance": 0.0000001},
    )

    assert pytest.approx(actual_upper_bound) == expected_upper_bound  # type: ignore


def test_indicator_fn():
    """
    Check an integrable indicator function
    """

    def integrable_function(input_x: float) -> float:
        """
        A basic indicator function
        """
        if 5 <= input_x <= 10:
            return 1

        return 0

    lower_bound = 0
    target_value = 1

    expected_upper_bound = 6
    actual_upper_bound = find_integral_bound(
        integrable_function=integrable_function,
        lower_bound=lower_bound,
        target_value=target_value,
        numerical_options={"tolerance": 0.0000001},
    )

    assert pytest.approx(actual_upper_bound) == expected_upper_bound  # type: ignore


def test_infinite_bound():
    """
    Ensure that infinity is returned when the bound would exceed the max bound
    """

    integrable_function: Callable[[float], float] = lambda x: x

    lower_bound = 0
    target_value = 100

    bound = find_integral_bound(
        integrable_function=integrable_function,
        lower_bound=lower_bound,
        target_value=target_value,
        numerical_options={"max_upper_bound": 5},
    )

    assert bound == inf


def test_max_iterations():
    """
    Ensure that a proper warning is raised when max iterations would be reached
    """

    integrable_function: Callable[[float], float] = lambda x: x

    lower_bound = 0
    target_value = 100

    with pytest.raises(RuntimeWarning):
        find_integral_bound(
            integrable_function=integrable_function,
            lower_bound=lower_bound,
            target_value=target_value,
            numerical_options={"max_iterations": 1},
        )
