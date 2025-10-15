from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Generic, TypeVar

import pandas as pd
from rdetoolkit.models.rde2types import MetaType, RepeatedMetaType
from rdetoolkit.rde2util import Meta

T = TypeVar("T")


class IInputFileParser(ABC):
    """Interface for input file parsers.

    Parsers read and parse files from given resource paths, and provide
    methods for column identification and invoice overwriting.

    Methods:
        read: Parse the input files.
        identify_columns: Identify relevant columns in data.
        overwrite_invoice: Overwrite invoice information.

    """

    @abstractmethod
    def read(self, path: Path) -> MetaType:
        """Read metadata from the specified path.

        This method must be implemented by subclasses. It is intended to read metadata
        from a given file path and return it as a `MetaType` object.

        Args:
            path (Path): The path to the metadata file.

        Returns:
            MetaType: The parsed metadata object.

        Raises:
            NotImplementedError: If the method is not implemented in a subclass.

        """
        raise NotImplementedError


class IStructuredDataProcessor(ABC):
    """Abstract base class (interface) for structured data parsers.

    This interface defines the contract that structured data parser
    implementations must follow. The parsers are expected to transform
    structured data, such as DataFrame, into various desired output formats.

    Methods:
        to_csv: A method that saves the given data to a CSV file.

    Implementers of this interface could transform data into various
    formats like CSV, Excel, JSON, etc.

    """

    @abstractmethod
    def to_csv(self, dataframe: pd.DataFrame, save_path: Path, *, header: list[str] | None = None, index: bool = False) -> None:
        """Save the given DataFrame as a CSV file."""
        raise NotImplementedError


class IMetaParser(ABC, Generic[T]):
    """Abstract base class (interface) for meta information parsers.

    This interface defines the contract that meta information parser
    implementations must follow. The parsers are expected to save the
    constant and repeated meta information to a specified path.

    Method:
        save_meta: Saves the constant and repeated meta information to a specified path.
        parse: This method returns two types of metadata: const_meta_info and repeated_meta_info.

    """

    @abstractmethod
    # def parse(self, meta: MetaType, characteristic_values: pd.DataFrame, invoice_obj: dict) -> tuple[MetaType, RepeatedMetaType]:
    def parse(self, data: MetaType) -> tuple[MetaType, RepeatedMetaType]:
        """Parse."""
        raise NotImplementedError

    @abstractmethod
    def save_meta(
        self,
        save_path: Path,
        meta_obj: Meta,
        *,
        const_meta_info: MetaType | None = None,
        repeated_meta_info: RepeatedMetaType | None = None,
    ) -> None:
        """Save meta."""
        raise NotImplementedError


class IGraphPlotter(ABC, Generic[T]):
    """Abstract base class (interface) for graph plotting implementations.

    This interface defines the contract that graph plotting
    implementations must follow. The implementations are expected
    to be capable of plotting a simple graph using a given pandas DataFrame.

    Methods:
        simple_plot: Plots a simple graph using the provided pandas DataFrame.

    """
