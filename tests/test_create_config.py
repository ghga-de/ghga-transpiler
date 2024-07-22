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

"""Tests for creating the config"""

from openpyxl import load_workbook

from ghga_transpiler.core import get_workbook_config

from .fixtures.test_data_objects.config_objects import (
    BOOKS_COLUMN_META,
    BOOKS_SHEET_META,
    PUBLISHER_COLUMN_META,
    PUBLISHER_SHEET_META,
)
from .fixtures.utils import get_project_root


def test_sheet_meta_configs() -> None:
    """Testing if __sheet_meta contains the correct set of worksheet configurations"""
    workbook_path = (
        get_project_root() / "tests" / "fixtures" / "workbooks" / "a_workbook.xlsx"
    )
    workbook_config = get_workbook_config(load_workbook(workbook_path))

    expected_sheet_meta = {"books": BOOKS_SHEET_META, "publisher": PUBLISHER_SHEET_META}
    expected_column_meta = {
        "books": BOOKS_COLUMN_META,
        "publisher": PUBLISHER_COLUMN_META,
    }
    for worksheet_name, worksheet in workbook_config.worksheets.items():
        assert worksheet.settings == expected_sheet_meta[worksheet_name]
        assert worksheet.columns == expected_column_meta[worksheet_name]


# buraya bi tane unhappy test case olur da sheetname unique degilse bakalim config hata verecek mi
