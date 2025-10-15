import json
import os
import shutil
from typing import List, Union


def setup_inputdata_folder(inputdata_name: Union[str, List[str]], format_name: str):
    """テスト用でdataフォルダ群の作成とrawファイルの準備

    Args:
        inputdata_name (Union[str, List[str]]): rawファイル名
        format_name (str): 使用するフォーマット名（mpms, LakeShoreなど）
    """

    destination_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    if os.path.exists(destination_path):
        shutil.rmtree(destination_path)

    destination_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    os.makedirs(destination_path, exist_ok=True)
    os.makedirs(os.path.join(destination_path, "inputdata"), exist_ok=True)
    os.makedirs(os.path.join(destination_path, "invoice"), exist_ok=True)

    inputdata_original_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "inputdata", format_name
    )

    if isinstance(inputdata_name, list):
        for item in inputdata_name:
            shutil.copy(
                os.path.join(inputdata_original_path, "inputdata", item),
                os.path.join(destination_path, "inputdata"),
            )
    else:
        shutil.copy(
            os.path.join(inputdata_original_path, format_name, inputdata_name),
            os.path.join(destination_path, "inputdata"),
        )

    shutil.copy(
        os.path.join(inputdata_original_path, "invoice", "invoice.json"),
        os.path.join(destination_path, "invoice"),
    )

    # tasksupport
    tasksupport_original_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "templates", "template", "tasksupport"
    )
    tasksupport_dest_path = os.path.join(destination_path, "tasksupport")
    os.makedirs(tasksupport_dest_path, exist_ok=True)

    for fname in ["invoice.schema.json", "metadata-def.json", "rdeconfig.yaml"]:
        shutil.copy(
            os.path.join(tasksupport_original_path, fname),
            os.path.join(tasksupport_dest_path, fname),
        )


class TestMeta1:
    """tiff形式のテスト:
       - "QPAF-C5.tif"
    """

    inputdata: Union[str, List[str]] = [
        "QPAF-C5.tif"
    ]

    def test_setup(self):
        setup_inputdata_folder(self.inputdata, format_name="test1")

    def test_metadata_constant(self, setup_main, setup_metadatadef_json):
        metadata = "metadata.json"
        result_metadata_filepath = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "data", "meta", metadata
        )

        with open(result_metadata_filepath, mode="r", encoding="utf-8") as f:
            contents = json.load(f)

        for k in contents["constant"].keys():
            constant_meta_key = setup_metadatadef_json.get(k)
            assert constant_meta_key

    def test_metadata_variable(self, setup_metadatadef_json):
        metadata = "metadata.json"
        result_metadata_filepath = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "data", "meta", metadata
        )

        with open(result_metadata_filepath, mode="r", encoding="utf-8") as f:
            contents = json.load(f)

        result_variable_keys = [k for item in contents["variable"] for k in item.keys()]
        for k in result_variable_keys:
            # metadata.json: variable
            variable_meta_key = setup_metadatadef_json.get(k)
            # check defined variable = 1
            except_variable_flag = setup_metadatadef_json[k].get("variable")

            assert (all(variable_meta_key)) and (except_variable_flag is not None)

class TestMeta2:
    """tiff形式のテスト:
       - "QPAF-C5_test.tiff"
    """

    inputdata: Union[str, List[str]] = [
        "QPAF-C5_test.tiff"
    ]

    def test_setup(self):
        setup_inputdata_folder(self.inputdata, format_name="test2")

    def test_metadata_constant(self, setup_main, setup_metadatadef_json):
        metadata = "metadata.json"
        result_metadata_filepath = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "data", "meta", metadata
        )

        with open(result_metadata_filepath, mode="r", encoding="utf-8") as f:
            contents = json.load(f)

        for k in contents["constant"].keys():
            constant_meta_key = setup_metadatadef_json.get(k)
            assert constant_meta_key

    def test_metadata_variable(self, setup_metadatadef_json):
        metadata = "metadata.json"
        result_metadata_filepath = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "data", "meta", metadata
        )

        with open(result_metadata_filepath, mode="r", encoding="utf-8") as f:
            contents = json.load(f)

        result_variable_keys = [k for item in contents["variable"] for k in item.keys()]
        for k in result_variable_keys:
            # metadata.json: variable
            variable_meta_key = setup_metadatadef_json.get(k)
            # check defined variable = 1
            except_variable_flag = setup_metadatadef_json[k].get("variable")

            assert (all(variable_meta_key)) and (except_variable_flag is not None)


class TestMeta3:
    """case3
    マルチファイルのテスト:
       - "QPAF-C5.tif"
       - "QPAF-C5_test.tiff"

    """

    inputdata: Union[str, List[str]] = [
       "QPAF-C5.tif",
       "QPAF-C5_test.tiff"
    ]

    def test_setup(self):
        setup_inputdata_folder(self.inputdata, format_name="test3")

    def test_metadata_constant(self, setup_main, setup_metadatadef_json):
        metadata = "metadata.json"
        result_metadata_filepath = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "data", "divided", "0001", "meta", metadata
        )

        with open(result_metadata_filepath, mode="r", encoding="utf-8") as f:
            contents = json.load(f)

        for k in contents["constant"].keys():
            constant_meta_key = setup_metadatadef_json.get(k)
            assert constant_meta_key

    def test_metadata_variable(self, setup_metadatadef_json):
        metadata = "metadata.json"
        result_metadata_filepath = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "data", "divided", "0001", "meta", metadata
        )

        with open(result_metadata_filepath, mode="r", encoding="utf-8") as f:
            contents = json.load(f)

        result_variable_keys = [k for item in contents["variable"] for k in item.keys()]
        for k in result_variable_keys:
            # metadata.json: variable
            variable_meta_key = setup_metadatadef_json.get(k)
            # check defined variable = 1
            except_variable_flag = setup_metadatadef_json[k].get("variable")

            assert (all(variable_meta_key)) and (except_variable_flag is not None)
