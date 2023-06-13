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
"""Module to load yaml file and return the config onject"""

from importlib import resources

import yaml

from ghga_transpiler.config.config import Config


def load_config(version: str) -> Config:
    """Reads yaml file from default location and creates config object"""
    config_resource = resources.files("ghga_transpiler.config.configs").joinpath(
        f"{version}.yaml"
    )
    config_str = config_resource.read_text(encoding="utf8")
    return Config.parse_obj(yaml.full_load(config_str))
