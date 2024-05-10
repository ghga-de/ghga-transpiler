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

"""Script to create datapack"""

from arcticfreeze import FrozenDict
from schemapack.spec.datapack import DataPack

from .core import GHGAWorkbook, convert_workbook_to_json


class PrimaryKeyNotFoundError(Exception):
    """Raised when a worksheet does not have an alias column as a primary key."""


def _get_content(row, primary_key, relations):
    """Creates content json"""
    return {
        key: value
        for key, value in row.items()
        if key != primary_key and key not in relations
    }


def _get_relations(row, relations):
    """Gets relations"""
    return {relation: row[relation] for relation in relations if relation in row}


def convert_workbook_to_datapack(ghga_workbook: GHGAWorkbook) -> FrozenDict:
    """Converts workbook to a dictionary that is compatible with DataPack definition"""
    json_workbook = convert_workbook_to_json(ghga_workbook)
    datapack_resources: dict = {}
    for worksheet_name, worksheet_data in json_workbook.items():
        worksheet = ghga_workbook.config.worksheets[worksheet_name]
        ws_relations = worksheet.relations
        ws_primary_key = worksheet.settings.primary_key
        for row in worksheet_data:
            content = _get_content(row, ws_primary_key, ws_relations[worksheet_name])

            relations = _get_relations(row, ws_relations[worksheet_name])
            try:
                datapack_resources.setdefault(worksheet_name, {}).setdefault(
                    row[ws_primary_key], {"content": content, "relations": relations}
                )
            except KeyError as err:
                raise PrimaryKeyNotFoundError(
                    f"Primary key column is not found in {worksheet_name} worksheet"
                ) from err
    return FrozenDict(datapack_resources)


def create_datapack(ghga_workbook: GHGAWorkbook):
    """Returns a DataPack object"""
    return DataPack(
        datapack="0.3.0",
        resources=convert_workbook_to_datapack(ghga_workbook),
        rootResource=None,
    )
