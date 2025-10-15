from pathlib import Path

from rdetoolkit.exceptions import StructuredError
from rdetoolkit.models.rde2types import MetaType

from modules import wavelet
from modules.interfaces import IInputFileParser


class FileReader(IInputFileParser):
    """Template class for reading and parsing input data.

    This class serves as a template for the development team to read and parse input data.
    It implements the IInputFileParser interface. Developers can use this template class
    as a foundation for adding specific file reading and parsing logic based on the project's
    requirements.

    Args:
        srcpaths (tuple[Path, ...]): Paths to input source files.

    Returns:
        Any: The loaded data from the input file(s).
    tto
    Example:
        file_reader = FileReader()
        loaded_data = file_reader.read(('file1.txt', 'file2.txt'))
        file_reader.to_csv('output.csv')

    """

    def read(self, path: Path) -> MetaType:
        """Read and convert wavelet-processed data from the input file into a MetaType object.

        This method processes the given input file using the `wavelet.wavelet_process`
        function and wraps the resulting dictionary into a `MetaType` instance.

        Args:
            path (Path): The path to the input file to be processed.

        Returns:
            MetaType: An instance containing the processed metadata.

        """
        dict_result = wavelet.wavelet_process(path)
        return MetaType(dict_result)

    def validate(self, rawfiles: tuple[Path, ...]) -> Path:
        """Validate input files for TIFF processing.

        This function ensures that exactly one TIFF file is provided for processing.
        It checks for file existence, quantity, and format validity.

        Args:
            rawfiles (tuple[Path, ...]): A tuple containing paths to input files.

        Returns:
            Path: The validated TIFF file path.

        Raises:
            StructuredError: If no input files are provided.
            StructuredError: If more than one file is provided.
            StructuredError: If the file is not in TIFF format (.tif or .tiff).

        Note:
            Only TIFF files with .tif or .tiff extensions are accepted.

        """
        if not rawfiles:
            msg = "No input files provided"
            raise StructuredError(msg)
        if len(rawfiles) > 1:
            msg = "Multiple files detected, only one file allowed"
            raise StructuredError(msg)
        input_file = rawfiles[0]
        if not (input_file.suffix.lower() == ".tif" or input_file.suffix.lower() == ".tiff"):
            raise StructuredError("An unexpected file was registered: " + input_file.name)
        return input_file

    def wavelet_process(self, input_file: Path) -> dict:
        """Apply wavelet-based processing to the input file.

        This method calls an external `wavelet.wavelet_process` function to perform
        wavelet transformation or analysis on the given file. The result is returned
        as a dictionary, with its structure depending on the implementation of the
        wavelet module.

        Args:
            input_file (Path): The path to the input file to be processed.

        Returns:
            dict: A dictionary containing the results of the wavelet processing.
                The exact structure and contents depend on `wavelet.wavelet_process`.

        """
        return wavelet.wavelet_process(input_file)
