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

from dataclasses import dataclass
from os.path import exists
from pathlib import Path

import yaml

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


@dataclass
class Config:
    """Class to create config object"""

    config: dict

    @property
    def from_dict(self):
        """Config constructor from dictionary"""
        for key, value in self.config.items():
            setattr(self, key, value)
        return self

    def get_param(self, worksheet_name, key):
        """Function to manage parameters of global and worksheet specific configuration"""
        try:
            return getattr(self, worksheet_name)[key]
        except KeyError:
            return getattr(self, "Global")[key]
