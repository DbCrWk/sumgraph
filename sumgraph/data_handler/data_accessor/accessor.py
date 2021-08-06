"""
This module defines the basic structure of an accessor
"""

from __future__ import annotations
from abc import ABC, abstractmethod


class Accessor(ABC):  # pylint: disable=too-few-public-methods
    """
    This class defines the basic Accessor pattern
    """

    @abstractmethod
    def run(self) -> Accessor:
        """
        This is the main method of an accessor that actually invokes it
        """
