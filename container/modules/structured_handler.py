from __future__ import annotations

from pathlib import Path

import pandas as pd
from PIL import Image
from rdetoolkit.exceptions import StructuredError
from rdetoolkit.models.rde2types import MetaType

from modules.interfaces import IStructuredDataProcessor


class StructuredDataProcessor(IStructuredDataProcessor):
    """Template class for parsing structured data.

    This class serves as a template for the development team to read and parse structured data.
    It implements the IStructuredDataProcessor interface. Developers can use this template class
    as a foundation for adding specific file reading and parsing logic based on the project's
    requirements.

    Example:
        csv_handler = StructuredDataProcessor()
        df = pd.DataFrame([[1,2,3],[4,5,6]])
        loaded_data = csv_handler.to_csv(df, 'file2.txt')

    """

    def to_csv(self, dataframe: pd.DataFrame, save_path: Path, *, header: list[str] | None = None, index: bool = False) -> None:
        """Save a pandas DataFrame to a CSV file.

        If a header list is provided, it will be used as the column headers in the CSV file.
        Otherwise, the DataFrame's existing column names will be used.

        Args:
            dataframe (pd.DataFrame): The DataFrame to save.
            save_path (Path): The path where the CSV file will be saved.
            header (list[str] | None, optional): A list of column names to use as the header.
                If None, uses the DataFrame's existing headers. Defaults to None.
            index (bool, optional): Whether to write the row indices to the CSV file. Defaults to False.

        Returns:
            None

        """
        if header is not None:
            dataframe.to_csv(save_path, header=header, index=index)
        else:
            dataframe.to_csv(save_path, index=index)

    def save_meta_to_csv(self, meta: MetaType, input_file_name: str, output_path: Path) -> None:
        """Save a metadata to csv file.

        Args:
            meta (MetaType): metadata.
            input_file_name (str): Input file name. Used for the index of the dataframe
            output_path (Path): Path for the CSV file to be saved

        """
        df = pd.DataFrame(meta, index=[0])
        df = df.rename(index={0: input_file_name})
        self.to_csv(df, output_path, header=df.columns.to_list(), index=True)

    def to_png(self, tif_path: Path, png_path: Path) -> None:
        """Convert a TIFF image to PNG.

        Args:
            tif_path (Path): Path to the source TIFF file.
            png_path (Path): Path where the converted PNG file will be saved

        """
        try:
            with Image.open(tif_path) as img:
                img.save(png_path, format="PNG")
        except FileNotFoundError as e:
            err_msg = f"Error: File not found: {tif_path}"
            raise StructuredError(err_msg) from e
        except Exception as e:
            err_msg = f"Error: An error occurred during conversion: {e}"
            raise StructuredError(err_msg) from e
