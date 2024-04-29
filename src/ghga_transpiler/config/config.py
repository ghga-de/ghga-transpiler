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

"""Module to process config file"""

from collections import Counter
from typing import Callable, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .exceptions import DuplicatedName


class Worksheet(BaseModel):
    """A data model for a worksheet"""

    model_config = ConfigDict(populate_by_name=True)

    name: str = Field(..., alias="sheet")
    header_row: int
    start_row: int = Field(..., alias="data_start")
    start_column: int = 1
    end_column: int = Field(..., alias="n_cols")
    transformations: Optional[dict[str, Callable]] = None


class Config(BaseModel):
    """A data model for the transpiler config"""

    worksheets: list[Worksheet]

    @model_validator(mode="after")
    def check_name(cls, values):  # noqa
        """Function to ensure that each worksheets has a unique sheet_name and name attributes."""
        # Check for duplicate attribute names
        attrs_counter = Counter(ws.name for ws in values.worksheets)
        dup_attrs = [name for name, count in attrs_counter.items() if count > 1]
        if dup_attrs:
            raise DuplicatedName(
                "Duplicate target attribute names: " + ", ".join(dup_attrs)
            )

        # Check for duplicate worksheet names
        attrs_counter = Counter(ws.name for ws in values.worksheets)
        dup_ws_names = [name for name, count in attrs_counter.items() if count > 1]
        if dup_ws_names:
            raise DuplicatedName(
                "Duplicate worksheet names: " + ", ".join(dup_ws_names)
            )
        return values
