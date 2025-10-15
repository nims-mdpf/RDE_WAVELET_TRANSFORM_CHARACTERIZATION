from pathlib import Path

from rdetoolkit.errors import catch_exception_with_message
from rdetoolkit.models.rde2types import (
    MetaType,
    RdeInputDirPaths,
    RdeOutputResourcePath,
)
from rdetoolkit.rde2util import Meta

from modules.graph_handler import GraphPlotter
from modules.inputfile_handler import FileReader
from modules.invoice_handler import InvoiceWriter
from modules.meta_handler import MetaParser
from modules.structured_handler import StructuredDataProcessor


class CustomProcessingCoordinator:
    """Coordinator class for managing custom processing modules.

    This class serves as a coordinator for custom processing modules, facilitating the use of
    various components such as file reading, metadata parsing, graph plotting, structured
    data processing, and invoice overwriting. It is responsible for managing these components and
    providing an organized way to execute the required tasks.

    Args:
        file_reader (FileReader): An instance of the file reader component.
        meta_parser (MetaParser): An instance of the metadata parsing component.
        graph_plotter (GraphPlotter): An instance of the graph plotting component.
        structured_processer (StructuredDataProcessor): An instance of the structured data
                                                        processing component.
        invoice_writer (class): An instance of the invoice overwriting component.

    Attributes:
        file_reader (FileReader): The file reader component for reading input data.
        meta_parser (MetaParser): The metadata parsing component for processing metadata.
        graph_plotter (GraphPlotter): The graph plotting component for visualization.
        structured_processer (StructuredDataProcessor): The component for processing structured data.
        invoice_writer (class): The component for overwriting invoice.

    Example:
        custom_module = CustomProcessingCoordinator(FileReader(), MetaParser(), GraphPlotter(), StructuredDataProcessor(), InvoiceWriter())
        # Note: The method 'execute_processing' hasn't been defined in the provided code,
        #       so its usage is just an example here.
        custom_module.execute_processing(srcpaths, resource_paths)

    """

    def __init__(
        self,
        file_reader: FileReader,
        meta_parser: MetaParser,
        graph_plotter: GraphPlotter,
        structured_processer: StructuredDataProcessor,
        invoice_writer: InvoiceWriter,
    ):
        self.file_reader = file_reader
        self.meta_parser = meta_parser
        self.graph_plotter = graph_plotter
        self.structured_processer = structured_processer
        self.invoice_writer = invoice_writer


@catch_exception_with_message(error_message="ERROR: failed in data processing", error_code=50)
def dataset(srcpaths: RdeInputDirPaths, resource_paths: RdeOutputResourcePath) -> None:
    """Execute structured processing in Wavelet-transform.

    It handles structured text processing, metadata extraction, and visualization.
    Other processing required for structuring may be implemented as needed.

    Args:
        srcpaths (RdeInputDirPaths): Paths to input resources for processing.
        resource_paths (RdeOutputResourcePath): Paths to output resources for saving results.

    Returns:
        None

    Note:
        The actual function names and processing details may vary depending on the project.

    """
    module = CustomProcessingCoordinator(FileReader(), MetaParser(), GraphPlotter(), StructuredDataProcessor(), InvoiceWriter())

    # Check input File
    rawfile: Path = module.file_reader.validate(resource_paths.rawfiles)

    # Read the file, perform a wavelet transform, and extract the metadata
    meta: MetaType = module.file_reader.read(rawfile)

    # Save metadata as CSV format
    module.structured_processer.save_meta_to_csv(meta, rawfile.name, resource_paths.struct.joinpath(f"{rawfile.stem}.csv"))

    # Convert from input tif file to png file
    module.structured_processer.to_png(rawfile, resource_paths.main_image.joinpath(f"{rawfile.stem}.png"))
    # Parse and save meta
    module.meta_parser.parse(meta)
    module.meta_parser.save_meta(resource_paths.meta.joinpath("metadata.json"), Meta(srcpaths.tasksupport.joinpath("metadata-def.json")))

    # Overwrite invoice
    module.invoice_writer.overwrite_invoice_calculated_date(resource_paths)
