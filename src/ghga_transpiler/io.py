# Copyright 2021 - 2024 Universität Tübingen, DKFZ, EMBL, and Universität zu Köln
# for the German Human Genome-Phenome Archive (GHGA)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""IO related functionality"""

import json
import sys
from pathlib import Path
from typing import TextIO

from openpyxl import Workbook, load_workbook
from schemapack import dumps_datapack
from schemapack.spec.datapack import DataPack

from .core import WorkbookConfig
from .utils import read_meta_information, worksheet_meta_information


def read_workbook(path: Path) -> Workbook:
    """Function to read-in a workbook"""
    return load_workbook(path)


def read_workbook_config(workbook: Workbook) -> WorkbookConfig:
    """Gets workbook configurations from the worksheet __sheet_meta"""
    worksheet_meta = worksheet_meta_information(
        read_meta_information(workbook, "__column_meta"),
        read_meta_information(workbook, "__sheet_meta"),
    )
    return WorkbookConfig.model_validate({"worksheets": worksheet_meta})


# def _write_json(data: str, file: TextIO):
#     """Writes data to the specified file"""
#     json.dump(obj=data, fp=file, ensure_ascii=False, indent=4)


def write_datapack(
    data: DataPack, path: Path | None, yaml_format: bool, force: bool
) -> None:
    """Writes data as JSON to the specified output path or
    to stdout if the path is None.
    """
    datapack = dumps_datapack(data, yaml_format=yaml_format)
    if path is None:
        sys.stdout.write(datapack)
    elif path.exists() and not force:
        raise FileExistsError(f"File already exists: {path}")
    else:
        with open(file=path, mode="w", encoding="utf8") as outfile:
            outfile.write(datapack)
