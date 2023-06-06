# Copyright 2021 - 2023 Universität Tübingen, DKFZ, EMBL, and Universität zu Köln
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
from openpyxl import load_workbook

from ghga_transpiler.cli import convert_workbook
from ghga_transpiler.config.config import Config

from .fixtures.test_data_objects.test_data_objects import (
    config_dict,
    expected_conversion_result,
)
from .fixtures.utils import get_project_root


def test_convert_workbook():
    """Test convert functionality"""

    workbook_path = get_project_root() / "example_data" / "a_workbook.xlsx"
    workbook = load_workbook(workbook_path)
    config = Config.parse_obj(config_dict())

    assert convert_workbook(workbook, config) == expected_conversion_result()
