import argparse
from collections.abc import Hashable
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import pyrtools as pt  # type: ignore[import-untyped]
from PIL import Image
from scipy import stats


def wavelet_process(input_file_path: Path) -> dict[str, float]:
    """Extract steerable pyramid features from an image and save them as CSV.

    This function loads an image from ``input_file_path``, crops it to a
    2048 x 2048 region, computes steerable pyramid features with a fixed
    decomposition height and order, aggregates selected statistics, and
    writes the resulting feature vector to ``steerable_pyramid_feature.csv``
    inside ``output_file_path``. The first (and only) record of the feature
    vector is also returned as a dictionary.

    Args:
        input_file_path (Path): Path to the image file to be processed.
        output_file_path (Path): Directory where the CSV file will be saved.

    Returns:
        dict: A dictionary mapping feature names to their computed values
        for the input image. The dictionary corresponds to the first row of
        the generated CSV.

    Raises:
        FileNotFoundError: If ``input_file_path`` does not exist.
        IOError: If the image cannot be opened or the CSV file cannot be
        written.
        ValueError: If any of the intermediate processing steps fail
        (e.g., unexpected image shape).

    """
    height: int = 5
    order: int = 3
    df = pd.DataFrame()
    image = np.array(Image.open(input_file_path))
    image_array = np.array(image)[:2048, :2048]
    feature = get_steerable_pyramid_feature(image_array, height, order)
    df = pd.DataFrame(list(feature.values()), index=list(feature.keys())).T
    feature_labels = df.columns
    for h in range(height):
        df[f"s_{h}"] = df[[f"ss_({h}, 0)" for k in range(order)]].mean(axis=1)
    df_mini = df[
        [
            "ms_mean",
            "ms_std",
            "ms_kurtosis",
            "ms_skewness",
            "ss_residual_highpass",
            "ss_residual_lowpass",
            "s_0",
            "s_1",
            "s_2",
            "s_3",
            "s_4",
        ]
    ]
    feature_labels = df_mini.columns

    output_df = df[feature_labels]
    original_dict: dict[Hashable, Any] = output_df.to_dict(orient="records")[0]
    # Convert to dictionary of str type
    result: dict[str, Any] = {str(key): value for key, value in original_dict.items()}
    return result


def get_steerable_pyramid_feature(image: Any, height: int, order: int) -> dict:
    """Extract statistical features from a steerable pyramid decomposition.

    The function builds a :class:`~pyrtools.pyramids.SteerablePyramidSpace`
    using the given ``height`` and ``order`` parameters, then computes a set
    of global statistics on the original image and the mean absolute
    coefficients for each sub?band of the pyramid.

    Args:
        image (Any): 2?D array?like image data (e.g., ``numpy.ndarray``).
        height (int): Height of the pyramid (number of decomposition scales).
        order (int): Order of the pyramid (number of orientation bands).

    Returns:
        dict: Mapping from feature names to their numeric values. The dictionary
        contains the following keys:

        - ``ms_mean``: Mean of all pixel values.
        - ``ms_std``: Sample standard deviation of pixel values.
        - ``ms_kurtosis``: Kurtosis of pixel values.
        - ``ms_skewness``: Skewness of pixel values.
        - ``ss_<key>``: Mean absolute coefficient of each sub?band ``key`` in the
          pyramid (e.g., ``ss_(0, 0)``).

    Raises:
        ValueError: If ``image`` cannot be reshaped to a 1?D array or if the
        ``height``/``order`` arguments are invalid for the pyramid constructor.

    """
    pyr = pt.pyramids.SteerablePyramidSpace(image, height=height, order=order)
    array = image.reshape(-1)
    feature_dict = {
        "ms_mean": np.mean(array),
        "ms_std": np.std(array, ddof=1),
        "ms_kurtosis": stats.kurtosis(array),
        "ms_skewness": stats.skew(array),
    }
    for key in pyr.pyr_coeffs:
        name = "ss_" + str(key)
        feature_dict[name] = np.mean(abs(pyr.pyr_coeffs[key]))

    return feature_dict


def main(input_file_path: Path, output_file_path: Path) -> None:
    """Execute unit tests."""
    dict_result = wavelet_process(Path(input_file_path))
    output_df = pd.DataFrame(dict_result, index=[0])
    output_df = output_df.rename(index={0: input_file_path.name})
    output_df.to_csv(output_file_path.joinpath("steerable_pyramid_feature.csv"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file_path")
    parser.add_argument("output_file_path")
    options = parser.parse_args()
    input_file_path = options.input_file_path
    output_file_path = options.output_file_path

    # wavelet_process(Path(input_file_path), Path(output_file_path))
    main(Path(input_file_path), Path(output_file_path))
    """
    fig, ax = plt.subplots()
    plt.title("name1")
    df_org = pd.read_csv(readfile1)
    df1_org = df_org.dropna().reset_index(drop=True)
    df1_org = df1_org.rename(columns = {"波長 (nm)": "wavelength (nm)", "量子効率": "EQE (%)"})
    df1_org = df1_org.sort_values(by=["wavelength (nm)"], ascending=True)
    eqe_inflection_row = df1_org.query('`wavelength (nm)` == @inflection_nm')
    eqe_inflection_percent = eqe_inflection_row.iloc[0,1]
    eqe_inflection_percent2 = eqe_inflection_row.iloc[0,1] * 1e-3
    df1_org = df1_org.query("`wavelength (nm)` >= @inflection_nm & @eqe_inflection_percent2 < `EQE (%)`").reset_index(drop=True)
    print(df1_org)
    print(inflection_nm)
    analyze_plot(df1_org, name1, eqe_inflection_row)
    plt.savefig(name1 + ".png", bbox_inches='tight')
    """
