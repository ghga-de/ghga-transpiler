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

"""Module containing transformation functions"""

from typing import Callable


def split_by_semicolon(value: str) -> list[str]:
    """Splits a string by semicolon"""
    return [elem.strip() for elem in value.split(";")]


def to_list() -> Callable:
    """Returns a function that splits a string by semicolon"""
    return split_by_semicolon


def to_attributes() -> Callable:
    """Returns a function to convert string to attributes"""

    def split_one(value: str) -> dict:
        """Returns a dictionary with key, value as keys, splitted string as values"""
        splitted = (elem.strip() for elem in value.split("="))
        return dict(zip(("key", "value"), splitted))

    def split_mult(value: str) -> list[dict]:
        """Function to convert string to attributes"""
        return [split_one(elem) for elem in split_by_semicolon(value)]

    return split_mult
