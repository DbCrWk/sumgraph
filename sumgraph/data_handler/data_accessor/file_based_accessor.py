"""
This module defines an Accessor that is backed by some type of datafile.
"""

from __future__ import annotations
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

    def run(self):
        """
        The main run method of a file based accessor
        """
        self.run_read_file().run_analyze_file()

        return self

    @abstractmethod
    def run_read_file(self) -> FileBasedAccessor:
        """
        The main method to read the file
        """

    @abstractmethod
    def run_analyze_file(self) -> FileBasedAccessor:
        """
        The main method to analyze the file
        """
