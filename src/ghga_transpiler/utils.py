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

"""Helper functions to shape data"""

from openpyxl import Workbook


def read_meta_information(workbook: Workbook, meta_sheet_name: str):
    """Reads the content of a worksheet"""
    if meta_sheet_name in workbook.sheetnames:
        sheet_meta_header = [cell.value for cell in workbook[meta_sheet_name][1]]
        sheet_meta_values = list(
            workbook[meta_sheet_name].iter_rows(min_row=2, values_only=True)
        )
        return [
            dict(zip(sheet_meta_header, val, strict=True)) for val in sheet_meta_values
        ]
    raise SyntaxError(
        f"Unable to extract the sheet {meta_sheet_name} from the workbook."
    )


def reshape_columns_meta(column_meta: list) -> dict:
    """Reshapes column metadata into a dictionary where keys are sheet names and values are lists of column metadata dictionaries"""
    worksheet_columns: dict = {}
    for item in column_meta:
        sheet_name = item["sheet"]
        worksheet_columns.setdefault(sheet_name, []).append(item)
    return worksheet_columns


def reshape_settings_meta(settings_meta: list) -> dict:
    """Reshapes settings metadata into a dictionary where keys are sheet names and values are worksheet settings dictionaries."""
    worksheet_settings: dict = {}
    for item in settings_meta:
        sheet_name = item["sheet"]
        worksheet_settings.setdefault(sheet_name, item)
    return worksheet_settings


def worksheet_meta_information(column_meta: list, settings_meta: list):
    """Creates a dictionary containing both settings and columns metadata for each worksheet"""
    return {
        key: {
            "settings": reshape_settings_meta(settings_meta)[key],
            "columns": reshape_columns_meta(column_meta)[key],
        }
        for key in reshape_settings_meta(settings_meta)
    }
