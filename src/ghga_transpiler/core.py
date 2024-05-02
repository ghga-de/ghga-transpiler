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

from collections.abc import Callable

import semver
from openpyxl import Workbook

from . import config
from .utils import read_meta_information, worksheet_meta_information


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
        worksheet_meta = worksheet_meta_information(
            read_meta_information(workbook, "__column_meta"),
            read_meta_information(workbook, "__sheet_meta"),
        )
        return config.WorkbookConfig.model_validate({"worksheets": worksheet_meta})


def get_worksheet_rows(
    worksheet,
    min_row: int | None,
    max_row: int,
    min_col: int | None,
    max_col: int | None,
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
    header_row: int | None,
    min_col: int | None,
    max_col: int | None,
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
            for key, value in zip(header, row, strict=True)
            if value is not None and value != ""
        }
        for row in rows
    ]


def transform_rows(
    rows: list[dict], transformations: dict[str, Callable]
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
    for name, worksheet in ghga_workbook.config.worksheets.items():
        if name in ghga_workbook.workbook:
            rows = get_worksheet_rows(
                ghga_workbook.workbook[name],
                worksheet.settings.start_row,
                ghga_workbook.workbook[name].max_row,
                worksheet.settings.start_column,
                worksheet.settings.end_column,
            )

            header = get_header(
                ghga_workbook.workbook[name],
                worksheet.settings.header_row,
                worksheet.settings.start_column,
                worksheet.settings.end_column,
            )
            converted_rows = convert_rows(header, rows)
            transformed_rows = transform_rows(converted_rows, worksheet.transformations)
            converted_workbook[name] = transformed_rows
        else:
            converted_workbook[name] = []

    return converted_workbook
