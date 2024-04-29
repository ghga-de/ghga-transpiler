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

"""This module contains functionalities for processing excel sheets into json object."""

from typing import Callable, Optional, Union

import semver
from openpyxl import Workbook

from . import config


class InvalidSematicVersion(Exception):
    """Raised when a version string is invalid."""


class GHGAWorkbook:
    """A GHGA metadata XLSX workbook"""

    def __init__(self, workbook: Workbook):
        """Create a new GHGAWorkbook object from an XLSX workbook"""
        self.workbook = workbook
        self.wb_version = GHGAWorkbook._get_transpiler_protocol(workbook)
        self.config = GHGAWorkbook._get_sheet_meta(self.workbook)

    @staticmethod
    def _get_transpiler_protocol(workbook):
        """Gets workbook version from the worksheet "__transpiler_protocol"""
        if "__transpiler_protocol" in workbook.sheetnames:
            try:
                return semver.Version.parse(
                    workbook["__transpiler_protocol"].cell(1, 1).value
                )
            except ValueError:
                raise InvalidSematicVersion(
                    "Unable to extract metadata model version from the provided workbook (not a valid semantic version)."
                ) from None
        raise SyntaxError(
            "Unable to extract metadata model version from the provided workbook (missing)."
        )

    @staticmethod
    def _get_sheet_meta(workbook):
        """Gets workbook configurations from the worksheet __sheet_meta"""
        if "__sheet_meta" in workbook.sheetnames:
            sheet_meta_header = [cell.value for cell in workbook["__sheet_meta"][1]]
            sheet_meta_values = list(
                workbook["__sheet_meta"].iter_rows(min_row=2, values_only=True)
            )
            values = [dict(zip(sheet_meta_header, val)) for val in sheet_meta_values]
            return config.Config.model_validate({"worksheets": values})

        raise SyntaxError("Unable to extract the sheet metadata from the workbook.")


def get_worksheet_rows(
    worksheet,
    min_row: Union[int, None],
    max_row: int,
    min_col: Union[int, None],
    max_col: Union[int, None],
) -> list:
    """Function to create a list of rows of a worksheet"""
    return list(
        row
        for row in worksheet.iter_rows(
            min_row, max_row, min_col, max_col, values_only=True
        )
        if not all(cell is None for cell in row)
    )


def get_header(
    worksheet,
    header_row: Union[int, None],
    min_col: Union[int, None],
    max_col: Union[int, None],
) -> list[str]:
    """Function to return a list column names of a worksheet"""
    return list(
        cell.value
        for row in worksheet.iter_rows(header_row, header_row, min_col, max_col)
        for cell in row
    )


def convert_rows(header, rows) -> list[dict]:
    """Function to return list of dictionaries, rows as worksheet row values and
    column names as keys
    """
    return [
        {
            key: value
            for key, value in zip(header, row)
            if value is not None and value != ""
        }
        for row in rows
    ]


def transform_rows(
    rows: list[dict], transformations: Optional[dict[str, Callable]]
) -> list[dict]:
    """Transforms row values if it is applicable with a given function"""
    transformed = []
    for row in rows:
        transformed_row = {}
        for key, value in row.items():
            if transformations and key in transformations:
                transformed_row[key] = transformations[key](value)
            else:
                transformed_row[key] = value
        transformed.append(transformed_row)
    return transformed


def convert_workbook(ghga_workbook: GHGAWorkbook) -> dict:
    """Function to convert an input spreadsheet into JSON"""
    converted_workbook = {}
    for sheet in ghga_workbook.config.worksheets:
        if sheet.name in ghga_workbook.workbook:
            rows = get_worksheet_rows(
                ghga_workbook.workbook[sheet.name],
                sheet.start_row,
                ghga_workbook.workbook[sheet.name].max_row,
                sheet.start_column,
                sheet.end_column,
            )

            header = get_header(
                ghga_workbook.workbook[sheet.name],
                sheet.header_row,
                sheet.start_column,
                sheet.end_column,
            )
            converted_rows = convert_rows(header, rows)
            transformed_rows = transform_rows(converted_rows, sheet.transformations)
            converted_workbook[sheet.name] = transformed_rows
        else:
            converted_workbook[sheet.name] = []

    return converted_workbook
