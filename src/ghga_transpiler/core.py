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

"""This module contains functionalities for processing excel sheets into json object."""

from collections.abc import Callable
from pathlib import Path

import semver
from openpyxl import Workbook

from ghga_transpiler.config import WorkbookConfig
from ghga_transpiler.io import read_workbook
from ghga_transpiler.models import GHGAWorkbook
from ghga_transpiler.parse import GHGAWorkbookParser


def parse_workbook(workbook: Workbook, config: WorkbookConfig) -> GHGAWorkbook:
    """Converts a workbook into GHGAWorkbook"""
    return GHGAWorkbookParser().parse(workbook=workbook, config=config)


def convert_workbook(spread_sheet: Path) -> GHGAWorkbook:
    """Flow to convert a spread_sheet into a GHGA workbook"""
    workbook = read_workbook(spread_sheet)
    workbook_config = get_workbook_config(workbook)
    return GHGAWorkbookParser().parse(workbook=workbook, config=workbook_config)

    # class GHGAWorkbook:
    #     """A GHGA metadata XLSX workbook"""

    #     def __init__(self, workbook: Workbook):
    #         """Create a new GHGAWorkbook object from an XLSX workbook"""
    #         self.workbook = workbook
    #         self.wb_version = GHGAWorkbook._get_transpiler_protocol(workbook)
    #         self.config = GHGAWorkbook._get_sheet_meta(self.workbook)

    #     @staticmethod
    #     def _get_transpiler_protocol(workbook):
    #         """Gets workbook version from the worksheet "__transpiler_protocol"""
    #         if "__transpiler_protocol" in workbook.sheetnames:
    #             try:
    #                 return semver.Version.parse(
    #                     workbook["__transpiler_protocol"].cell(1, 1).value
    #                 )
    #             except ValueError:
    #                 raise InvalidSematicVersion(
    #                     "Unable to extract metadata model version from the provided workbook (not a valid semantic version)."
    #                 ) from None
    #         raise SyntaxError(
    #             "Unable to extract metadata model version from the provided workbook (missing)."
    #         )
