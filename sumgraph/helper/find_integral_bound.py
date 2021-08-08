"""
This module finds the bounds of an integral given a positive, real-valued
function, target value, and lower bound
"""

import math
from typing import Callable, Optional, Tuple, TypedDict
from scipy import integrate  # type: ignore


IntegrableFn = Callable[[float], float]


NumericalOptions = TypedDict(
    "NumericalOptions",
    {
        "max_upper_bound": Optional[float],
        "tolerance": Optional[float],
        "max_iterations": Optional[int],
    },
    total=False,
)


def find_upper_and_lower_integral_upper_bound(
    get_integral_value: Callable[[float], Tuple[float, float]],
    target_value: float,
    min_upper_bound: float,
    max_upper_bound: float,
) -> Tuple[float, float]:
    """
    This function finds approximate lower and upper integral bounds for the
    upper limit of integration
    """

    lower_test_upper_bound: float = min_upper_bound
    upper_test_upper_bound: float = min_upper_bound

    upper_test_value: float = 0

    while upper_test_upper_bound < max_upper_bound:
        result: Tuple[float, float] = get_integral_value(upper_test_upper_bound)
        (upper_test_value, _) = result

        if upper_test_value >= target_value:
            break

        lower_test_upper_bound = upper_test_upper_bound

        upper_test_upper_bound = (upper_test_upper_bound + 1) * 2

    # If we hit the maximum upper bound, then we assume that the true upper
    # bound is infinite
    if upper_test_value < target_value:
        raise RuntimeWarning("max_upper bound reached")

    return (lower_test_upper_bound, upper_test_upper_bound)


def find_upper_bound_between_range(
    get_integral_value: Callable[[float], Tuple[float, float]],
    target_value: float,
    limits: Tuple[float, float],
    max_iterations: int,
    tolerance: float,
) -> float:
    """
    This function takes in two possible upper limits of integration and finds
    the correct limit of integration between those limits where the target value
    is acheived for the integral.
    """
    (lower_test_upper_bound, upper_test_upper_bound) = limits

    iterations = 0
    while iterations < max_iterations:
        test_upper_bound = (lower_test_upper_bound + upper_test_upper_bound) / 2

        result: Tuple[float, float] = get_integral_value(test_upper_bound)
        (test_value, _) = result

        diff = abs(test_value - target_value)

        if diff <= tolerance:
            return test_upper_bound

        if test_value < target_value:
            lower_test_upper_bound = test_upper_bound

        if test_value > target_value:
            upper_test_upper_bound = test_upper_bound

        iterations += 1

    raise RuntimeWarning("Max iterations reached but integral solution was not found")


def find_integral_bound(
    integrable_function: IntegrableFn,
    lower_bound: float,
    target_value: float,
    numerical_options: Optional[NumericalOptions] = None,
) -> float:
    """
    This function finds the upper bound of an integral given a positive,
    real-valued, integrable function, lower bound, and target value. Optionally,
    specify a maximum upper bound to look at; if we hit the max bound without
    reaching the target value, we return infiinity.
    """

    # Set parameters
    max_upper_bound: float = 1000
    tolerance: float = 0.0001
    max_iterations: int = 1000

    if numerical_options is not None:
        max_upper_bound = (
            numerical_options["max_upper_bound"] or max_upper_bound
            if "max_upper_bound" in numerical_options
            else max_upper_bound
        )
        tolerance = (
            numerical_options["tolerance"] or tolerance
            if "tolerance" in numerical_options
            else tolerance
        )
        max_iterations = (
            numerical_options["max_iterations"] or max_iterations
            if "max_iterations" in numerical_options
            else max_iterations
        )

    get_integral_value: Callable[
        [float], Tuple[float, float]
    ] = lambda x: integrate.quad(  # type: ignore
        func=integrable_function, a=lower_bound, b=x
    )

    # First: find potential bounds
    lower_test_upper_bound: float
    upper_test_upper_bound: float

    try:
        (
            lower_test_upper_bound,
            upper_test_upper_bound,
        ) = find_upper_and_lower_integral_upper_bound(
            get_integral_value=get_integral_value,
            target_value=target_value,
            min_upper_bound=lower_bound,
            max_upper_bound=max_upper_bound,
        )
    except RuntimeWarning:
        return math.inf

    # Second loop: binary search until we find the value
    return find_upper_bound_between_range(
        get_integral_value=get_integral_value,
        target_value=target_value,
        limits=(lower_test_upper_bound, upper_test_upper_bound),
        max_iterations=max_iterations,
        tolerance=tolerance,
    )
