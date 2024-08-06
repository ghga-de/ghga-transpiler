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
from arcticfreeze import FrozenDict
from openpyxl import Workbook
from schemapack.spec.datapack import DataPack

from ghga_transpiler.config import WorkbookConfig
from ghga_transpiler.io import read_workbook
from ghga_transpiler.models import GHGAWorkbook
from ghga_transpiler.parse import GHGAWorkbookParser
from ghga_transpiler.utils import read_meta_information, worksheet_meta_information


def get_workbook_config(workbook):
    """Gets workbook configurations from the worksheet __sheet_meta"""
    worksheet_meta = worksheet_meta_information(
        read_meta_information(workbook, "__column_meta"),
        read_meta_information(workbook, "__sheet_meta"),
    )
    return WorkbookConfig.model_validate({"worksheets": worksheet_meta})


def parse_workbook(workbook: Workbook, config: WorkbookConfig) -> GHGAWorkbook:
    """Converts a workbook into GHGAWorkbook"""
    return GHGAWorkbookParser().parse(workbook=workbook, config=config)


def produce_datapack(workbook: GHGAWorkbook) -> DataPack:
    """Convert GHAWorkbook into a Datapack instance."""
    return DataPack(
        datapack="0.3.0", resources=FrozenDict(workbook.model_dump()), rootResource=None
    )


def convert_workbook(spread_sheet: Path) -> GHGAWorkbook:
    """Flow to convert a spread_sheet into a GHGA workbook"""
    workbook = read_workbook(spread_sheet)
    workbook_config = get_workbook_config(workbook)
    return GHGAWorkbookParser().parse(workbook=workbook, config=workbook_config)

    # def convert_workbook_to_datapack(ghga_workbook: GHGAWorkbook) -> FrozenDict:
    #     """Converts workbook to a dictionary that is compatible with DataPack definition"""
    #     json_workbook = convert_workbook_to_json(ghga_workbook)
    #     datapack_resources: dict = {}
    #     for worksheet_name, worksheet_data in json_workbook.items():
    #         worksheet = ghga_workbook.config.worksheets[worksheet_name]
    #         ws_relations = worksheet.get_relations()
    #         ws_primary_key = worksheet.settings.primary_key
    #         for row in worksheet_data:
    #             content = _content_to_dict(
    #                 row, ws_primary_key, ws_relations[worksheet_name]
    #             )

    #             relations = _relations_to_dict(row, ws_relations[worksheet_name])
    #             try:
    #                 datapack_resources.setdefault(worksheet_name, {}).setdefault(
    #                     row[ws_primary_key], {
    #                         "content": content, "relations": relations}
    #                 )
    #             except KeyError as err:
    #                 raise PrimaryKeyNotFoundError(
    #                     f"Primary key column is not found in {
    #                         worksheet_name} worksheet"
    #                 ) from err
    #     return FrozenDict(datapack_resources)

    # def create_datapack(ghga_workbook: GHGAWorkbook) -> DataPack:
    #     """Returns a DataPack object"""
    #     return DataPack(
    #         datapack="0.3.0",
    #         resources=convert_workbook_to_datapack(ghga_workbook),
    #         rootResource=None,
    #     )

    # class InvalidSematicVersion(Exception):
    #     """Raised when a version string is invalid."""

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

    #     @staticmethod
    #     def _get_sheet_meta(workbook):
    #         """Gets workbook configurations from the worksheet __sheet_meta"""
    #         worksheet_meta = worksheet_meta_information(
    #             read_meta_information(workbook, "__column_meta"),
    #             read_meta_information(workbook, "__sheet_meta"),
    #         )
    #         return WorkbookConfig.model_validate({"worksheets": worksheet_meta})
