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
"""Unit tests for core functions"""

from ghga_transpiler.core.core import get_version

from .fixtures.utils import create_workbook


def test_get_version() -> None:
    """Function to check if it correctly gets workbook version from _properties worksheet"""
    workbook = create_workbook("__properties")
    value = workbook["__properties"].cell(row=1, column=1, value="a_string").value
    assert get_version(workbook) == value


def test_get_default_version() -> None:
    """Function to test if it returns default value when version is not coming from the workbook"""
    workbook = create_workbook("sheet1", "sheet2")
    assert get_version(workbook) == "0.0.1"
