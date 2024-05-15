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

"""Tests for converting the workbook"""

import json

from schemapack._internals.dump import dumps_datapack

from ghga_transpiler import io
from ghga_transpiler.datapack import create_datapack

from .fixtures.test_data_objects.conversion_data import EXPECTED_CONVERSION
from .fixtures.utils import get_project_root


def test_convert_workbook() -> None:
    """Function to test workbook to json conversion"""
    workbook_path = (
        get_project_root() / "tests" / "fixtures" / "workbooks" / "a_workbook.xlsx"
    )
    ghga_workbook = io.read_workbook(workbook_path)

    datapack_dump = dumps_datapack(
        create_datapack(ghga_workbook=ghga_workbook), yaml_format=False
    )

    assert datapack_dump == json.dumps(EXPECTED_CONVERSION, indent=2)
