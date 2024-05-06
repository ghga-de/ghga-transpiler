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

"""Module to process config file"""

from collections import Counter
from collections.abc import Callable

from pydantic import BaseModel, ConfigDict, Field, computed_field, model_validator

from .exceptions import DuplicatedName
from .transformations import to_attributes, to_list, to_snake_case, to_snake_case_list


class ColumnProperties(BaseModel):
    """A data model for column properties"""

    model_config = ConfigDict(populate_by_name=True)

    sheet_name: str = Field(..., alias="sheet")
    column_name: str = Field(..., alias="column")
    multivalued: bool
    type: str
    ref_class: str | None
    ref_id: str | None = Field(..., alias="ref_class_id_property")
    enum: bool
    required: bool

    @computed_field  # type: ignore [misc]
    @property
    def transformation(self) -> Callable | None:
        """Assigns transformation function based on column properties"""
        if self.multivalued and self.enum:
            return to_snake_case_list()
        elif self.enum:
            return to_snake_case()
        elif self.multivalued and self.type == "object":
            return to_attributes()
        elif self.multivalued:
            return to_list()
        else:
            return None


class WorksheetSettings(BaseModel):
    """A data model for worksheet settings"""

    model_config = ConfigDict(populate_by_name=True)

    name: str = Field(..., validation_alias="sheet")
    header_row: int
    start_row: int = Field(..., validation_alias="data_start")
    start_column: int = 1
    end_column: int = Field(..., validation_alias="n_cols")


class Worksheet(BaseModel):
    """A data model for a worksheet"""

    settings: WorksheetSettings
    columns: list[ColumnProperties]

    @cached_property
    def transformations(self) -> dict:
        """Merges the transformation of a worksheet"""
        return {
            column.column_name: column.transformation
            for column in self.columns
            if column.transformation != None
        }


class WorkbookConfig(BaseModel):
    """A data model containing transpiler configurations"""

    worksheets: dict[str, Worksheet]

    @model_validator(mode="after")
    def check_name(cls, values):  # noqa
        """Function to ensure that each worksheets has a unique sheet_name and name attributes."""
        # Check for duplicate attribute names
        attrs_counter = Counter(ws for ws in values.worksheets)
        dup_attrs = [name for name, count in attrs_counter.items() if count > 1]
        if dup_attrs:
            raise DuplicatedName(
                "Duplicate target attribute names: " + ", ".join(dup_attrs)
            )

        # Check for duplicate worksheet names
        attrs_counter = Counter(ws for ws in values.worksheets)
        dup_ws_names = [name for name, count in attrs_counter.items() if count > 1]
        if dup_ws_names:
            raise DuplicatedName(
                "Duplicate worksheet names: " + ", ".join(dup_ws_names)
            )
        return values
