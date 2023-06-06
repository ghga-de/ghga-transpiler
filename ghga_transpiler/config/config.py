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

from os.path import exists
from pathlib import Path
from typing import List, Optional

import yaml
from pydantic import BaseModel, root_validator

from ..core.core import VERSION
from .exceptions import MissingConfigFile

HERE = Path(__file__).parent.resolve()
CONFIG_LOCATION = HERE / "configs" / f"worksheet_config_{VERSION}.yaml"


def read_config():
    """Function to load yaml file"""

    if exists(CONFIG_LOCATION):
        with open(CONFIG_LOCATION, "r", encoding="utf-8") as file:
            return yaml.safe_load(file)
    raise MissingConfigFile(f"Config file for version {VERSION} cannot be found.")


class DefaultSettings(BaseModel):
    """Class to create worksheet setting"""

    start_row: int = 0
    start_column: int = 0
    end_column: int = 0


class WorksheetSettings(BaseModel):
    """Class to create worksheet setting"""

    name: Optional[str]
    start_row: Optional[int]
    start_column: Optional[int]
    end_column: Optional[int]


class Worksheet(BaseModel):
    """class"""

    sheet_name: Optional[str]
    settings: Optional[WorksheetSettings]


class Config(BaseModel):
    """Class to create config object"""

    ghga_version: Optional[str]
    default_settings: DefaultSettings
    worksheets: List[Worksheet]

    @root_validator(pre=False)
    def get_param(cls, values):  # pylint: disable=no-self-argument
        """Function to manage parameters of global and worksheet specific configuration"""
        for sheet in values.get("worksheets"):
            for key in values.get("default_settings").__dict__:
                if not getattr(sheet.settings, key):
                    val = getattr(values.get("default_settings"), key)
                    setattr(sheet.settings, key, val)
        return values
