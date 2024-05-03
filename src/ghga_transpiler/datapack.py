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

import json
from io import StringIO
from typing import Any

import ruamel.yaml
from pydantic import BaseModel
from schemapack.spec.datapack import DataPack

from .core import GHGAWorkbook, convert_workbook_to_json

yaml = ruamel.yaml.YAML(typ="rt")


class PrimaryKeyNotFoundError(Exception):
    """Raised when a worksheet does not have an alias column as a primary key."""


def _get_content(row, primary_key, relations):
    """Function to create content json"""
    return {
        key: value
        for key, value in row.items()
        if key != primary_key and key not in relations
    }


def _get_relations(row, relations):
    """Function to get relations"""
    return {relation: row[relation] for relation in relations if relation in row}


def convert_workbook_to_datapack(ghga_workbook: GHGAWorkbook) -> dict:
    """Function"""
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
    return datapack_resources


def create_datapack(ghga_workbook: GHGAWorkbook):
    """Returns a DataPack object"""
    return DataPack(
        datapack="0.3.0",
        resources=convert_workbook_to_datapack(ghga_workbook),
        rootResource=None,
    )


def model_to_serializable_dict(
    model: BaseModel,
) -> dict[str, Any]:
    """Converts the provided pydantic model to a JSON-serializable dictionary.

    Returns:
        A dictionary representation of the provided model.

    Function is taken from schemapack's main branch since it is not a part of the alpha-3 release
    """
    return json.loads(model.model_dump_json(exclude_defaults=True))


def dumps_model(
    model: BaseModel,
    *,
    yaml_format: bool = True,
) -> str:
    """Dumps the provided pydantic model as a JSON or YAML-formatted string.

    Args:
        model:
            The model to dump.
        yaml_format:
            Whether to dump as YAML (`True`) or JSON (`False`).

    Function is taken from schemapack's main branch since it is not a part of the alpha-3 release
    """
    model_dict = model_to_serializable_dict(model)

    if yaml_format:
        with StringIO() as buffer:
            yaml.dump(model_dict, buffer)
            return buffer.getvalue().strip()

    return json.dumps(model_dict, indent=2)


def dumps_datapack(
    datapack: DataPack,
    *,
    yaml_format: bool = True,
) -> str:
    """Dumps the provided datapack as a JSON or YAML-formatted string.

    Args:
        datapack:
            The datapack to dump.
        yaml_format:
            Whether to dump as YAML (`True`) or JSON (`False`).

    Function is taken from schemapack's main branch since it is not a part of the alpha-3 release
    """
    return dumps_model(datapack, yaml_format=yaml_format)
