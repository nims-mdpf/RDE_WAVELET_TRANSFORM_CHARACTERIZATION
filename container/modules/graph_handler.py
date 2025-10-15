from __future__ import annotations

from pathlib import Path

import pandas as pd

from modules.interfaces import IGraphPlotter


class GraphPlotter(IGraphPlotter[pd.DataFrame]):
    """Template class for creating graphs and visualizations.

    This class serves as a template for the development team to create graphs and visualizations.
    It implements the IGraphPlotter interface. Developers can use this template class as a
    foundation for adding specific graphing logic and customizations based on the project's
    requirements.

    Args:
        df (pd.DataFrame): The DataFrame containing data to be plotted.
        save_path (Path): The path where the generated graph will be saved.

    Keyword Args:
        header (Optional[list[str]], optional): A list of column names to use as headers in the graph.
            Defaults to None.

    Example:
        graph_plotter = GraphPlotter()
        data = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
        graph_plotter.plot(data, 'graph.png', header=['X Axis', 'Y Axis'])

    """

    def plot(self, data: pd.DataFrame, save_path: Path, *, title: str | None = None, xlabel: str | None = None, ylabel: str | None = None) -> bool:
        """Draw graph."""
        raise NotImplementedError
