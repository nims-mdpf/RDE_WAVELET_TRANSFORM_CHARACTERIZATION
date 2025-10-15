import os
import shutil
from typing import Union


def setup_inputdata_folder(inputdata_name: Union[str, list[str]]):
    """テスト用でdataフォルダ群の作成とrawファイルの準備

    Args:
        inputdata_name (Union[str, list[str]]): rawファイル名
    """
    destination_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    os.makedirs(destination_path, exist_ok=True)
    os.makedirs(os.path.join(destination_path, "inputdata"), exist_ok=True)
    os.makedirs(os.path.join(destination_path, "invoice"), exist_ok=True)
    inputdata_original_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "inputdata")

    tasksupport_original_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        "templates",
        "template",
        "tasksupport",
    )

    if isinstance(inputdata_name, list):
        for item in inputdata_name:
            shutil.copy(
                os.path.join(inputdata_original_path, item),
                os.path.join(destination_path, "inputdata"),
            )
    else:
        shutil.copy(
            os.path.join(inputdata_original_path, inputdata_name),
            os.path.join(destination_path, "inputdata"),
        )
    if not os.path.exists(os.path.join(destination_path, "tasksupport")):
        shutil.copytree(tasksupport_original_path, os.path.join(destination_path, "tasksupport"))


def setup_invoice_file(path: str):
    """テスト用でinvoiceファイルの準備

    Args:
        path (Union[str, list[str]]): rawファイル名
    """
    destination_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    os.makedirs(destination_path, exist_ok=True)
    os.makedirs(os.path.join(destination_path, "invoice"), exist_ok=True)
    inputdata_original_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "inputdata")

    shutil.copy(
        os.path.join(inputdata_original_path, path),
        os.path.join(destination_path, "invoice"),
    )


def setup_file(dirname: str, path: str):
    """Sets up the file structure and copies a specified file to a destination directory.
    This function creates a directory structure under a "data" directory located two levels up from the current file's directory.
    It then copies a file from an "inputdata" directory located three levels up from the current file's directory to the newly created directory.

    Args:
        dirname (str): The name of the subdirectory to create under the "data" directory.
        path (str): The relative path of the file to copy from the "inputdata" directory.

    Raises:
        OSError: If the file or directory operations fail.

    """

    destination_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    os.makedirs(destination_path, exist_ok=True)
    os.makedirs(os.path.join(destination_path, dirname), exist_ok=True)
    inputdata_original_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "inputdata")

    shutil.copy(
        os.path.join(inputdata_original_path, path),
        os.path.join(destination_path, dirname),
    )


class TestOutputCase1:
    """tifファイルの入力テスト:
       - "QPAF-C5.tif"
    """

    # inputdata: Union[str, list[str]] = "<テストで使用する入力ファイルパス: リポジトリ直下inputdataディィレクトリ以下>"
    # invoice: str = "<テストで使用するinvoice.jsonパス: リポジトリ直下inputdataディィレクトリ以下>"
    inputdata: Union[str, list[str]] = "test1/inputdata/QPAF-C5.tif"
    invoice: str = "test1/invoice/invoice.json"

    def test_setup(self):
        setup_inputdata_folder(self.inputdata)
        setup_invoice_file(self.invoice)
        # ...

    def test_raw_data(self, setup_main, data_path):
        assert os.path.exists(os.path.join(data_path, "nonshared_raw", "QPAF-C5.tif"))

    def test_main_image(self, data_path):
        assert os.path.exists(os.path.join(data_path, "main_image", "QPAF-C5.png"))

    def test_structured(self, data_path):
        assert os.path.exists(os.path.join(data_path, "structured", "QPAF-C5.csv"))

    def test_thumbnail(self, data_path):
        assert os.path.exists(os.path.join(data_path, "thumbnail", "QPAF-C5.png"))

    def test_metadata(self, data_path):
        assert os.path.exists(os.path.join(data_path, "meta", "metadata.json"))


class TestOutputCase2:
    """tiffファイルの入力テスト:
       - "QPAF-C5_test.tiff"
    """

    # inputdata: Union[str, list[str]] = "<テストで使用する入力ファイルパス: リポジトリ直下inputdataディィレクトリ以下>"
    # invoice: str = "<テストで使用するinvoice.jsonパス: リポジトリ直下inputdataディィレクトリ以下>"
    inputdata: Union[str, list[str]] = "test2/inputdata/QPAF-C5_test.tiff"
    invoice: str = "test2/invoice/invoice.json"

    def test_setup(self):
        setup_inputdata_folder(self.inputdata)
        setup_invoice_file(self.invoice)
        # ...

    def test_raw_data(self, setup_main, data_path):
        assert os.path.exists(os.path.join(data_path, "nonshared_raw", "QPAF-C5_test.tiff"))

    def test_main_image(self, data_path):
        assert os.path.exists(os.path.join(data_path, "main_image", "QPAF-C5_test.png"))

    def test_structured(self, data_path):
        assert os.path.exists(os.path.join(data_path, "structured", "QPAF-C5_test.csv"))

    def test_thumbnail(self, data_path):
        assert os.path.exists(os.path.join(data_path, "thumbnail", "QPAF-C5_test.png"))

    def test_metadata(self, data_path):
        assert os.path.exists(os.path.join(data_path, "meta", "metadata.json"))


class TestOutputCase3:
    """tif, tiffファイルのマルチファイルテスト:
       - "QPAF-C5.tif"
       - "QPAF-C5_test.tiff"
    """

    # inputdata: Union[str, list[str]] = "<テストで使用する入力ファイルパス: リポジトリ直下inputdataディィレクトリ以下>"
    # invoice: str = "<テストで使用するinvoice.jsonパス: リポジトリ直下inputdataディィレクトリ以下>"
    inputdata: Union[str, list[str]] = ["test3/inputdata/QPAF-C5.tif", "test3/inputdata/QPAF-C5_test.tiff"] 
    invoice: str = "test3/invoice/invoice.json"

    def test_setup(self):
        setup_inputdata_folder(self.inputdata)
        setup_invoice_file(self.invoice)
        # ...

    def test_raw_data(self, setup_main, data_path):
        assert os.path.exists(os.path.join(data_path, "nonshared_raw", "QPAF-C5.tif"))
        assert os.path.exists(os.path.join(data_path, "divided", "0001", "nonshared_raw", "QPAF-C5_test.tiff"))

    def test_main_image(self, data_path):
        assert os.path.exists(os.path.join(data_path, "main_image", "QPAF-C5.png"))
        assert os.path.exists(os.path.join(data_path, "divided", "0001", "main_image", "QPAF-C5_test.png"))

    def test_structured(self, data_path):
        assert os.path.exists(os.path.join(data_path, "structured", "QPAF-C5.csv"))
        assert os.path.exists(os.path.join(data_path, "divided", "0001", "structured", "QPAF-C5_test.csv"))

    def test_thumbnail(self, data_path):
        assert os.path.exists(os.path.join(data_path, "thumbnail", "QPAF-C5.png"))
        assert os.path.exists(os.path.join(data_path, "divided", "0001", "thumbnail", "QPAF-C5_test.png"))

    def test_metadata(self, data_path):
        assert os.path.exists(os.path.join(data_path, "meta", "metadata.json"))
        assert os.path.exists(os.path.join(data_path, "divided", "0001", "meta", "metadata.json"))
