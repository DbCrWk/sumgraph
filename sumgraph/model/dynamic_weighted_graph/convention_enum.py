"""
This module defines the various conventions on what an edge weight represents
"""


from enum import Enum


class ConventionEnum(Enum):
    """
    This enum provides a convention on what edge weight represents
    """

    TRAVERSAL_TIME = 1
    CAPACITY = 2
    COST = 3
