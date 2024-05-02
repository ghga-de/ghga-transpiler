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

"""Tests for creating the config"""

from openpyxl import load_workbook

from ghga_transpiler.config import WorksheetSettings
from ghga_transpiler.core import GHGAWorkbook

from .fixtures.utils import get_project_root


def test_config_params() -> None:
    """Testing if __sheet_meta contains the correct set of worksheet configurations"""
    workbook_path = (
        get_project_root() / "tests" / "fixtures" / "workbooks" / "a_workbook.xlsx"
    )
    workbook_config = GHGAWorkbook._get_sheet_meta(load_workbook(workbook_path))

    books_settings = WorksheetSettings(
        name="books",
        header_row=1,
        start_row=2,
        start_column=1,
        end_column=5,
    )
    publisher_settings = WorksheetSettings(
        name="publisher",
        header_row=1,
        start_row=2,
        start_column=1,
        end_column=3,
    )
    expected_settings = {"books": books_settings, "publisher": publisher_settings}
    for worksheet_name, worksheet in workbook_config.worksheets.items():
        assert worksheet.settings == expected_settings[worksheet_name]
