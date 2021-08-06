"""
This module defines an Accessor that is backed by some type of datafile.
"""

from abc import abstractmethod
from sumgraph.data_handler.data_accessor.accessor import Accessor


class FileBasedAccessor(Accessor):
    """
    This class defines accessors that are based on a particular file
    """

    def __init__(self, filepath: str) -> None:
        super().__init__()
        self.filepath = filepath

    @property
    def filepath(self) -> str:
        """
        The filepath for the datafile that this accessor is based on
        """
        return self._filepath

    @filepath.setter
    def filepath(self, value: str) -> str:
        self._filepath = value

        return self._filepath

    @abstractmethod
    def run(self) -> Accessor:
        """
        The main run method of an Accessor
        """

    @abstractmethod
    def run_read_file(self) -> Accessor:
        """
        The main method to read the file
        """
