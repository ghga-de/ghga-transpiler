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

"""Generates a JSON schema from the service's Config class as well as a corresponding
example config yaml (or check whether these files are up to date).
"""


import importlib
import subprocess
import sys
from difflib import unified_diff
from pathlib import Path
from typing import Any

from script_utils.cli import echo_failure, echo_success, run

HERE = Path(__file__).parent.resolve()
REPO_ROOT_DIR = HERE.parent
GET_PACKAGE_NAME_SCRIPT = HERE / "get_package_name.py"
CONFIG_SCHEMA_JSON = REPO_ROOT_DIR / "config_schema.json"


class ValidationError(RuntimeError):
    """Raised when validation of config documentation fails."""


def get_config_class():
    """
    Dynamically imports and returns the Config class from the current service.
    This makes the script service repo agnostic.
    """
    # get the name of the microservice package
    with subprocess.Popen(
        args=[GET_PACKAGE_NAME_SCRIPT],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    ) as process:
        assert (
            process.wait() == 0 and process.stdout is not None
        ), "Failed to get package name."
        package_name = process.stdout.read().decode("utf-8").strip("\n")

    # import the Config class from the microservice package:
    config_module: Any = importlib.import_module(f"{package_name}.config")
    config_class = config_module.Config

    return config_class


def get_schema() -> str:
    """Returns a JSON schema generated from a Config class."""

    config = get_config_class()
    return config.schema_json(indent=2)  # change eventually to .model_json_schema(...)


def update_docs():
    """Update the example config and config schema files documenting the config
    options."""

    schema = get_schema()
    with open(CONFIG_SCHEMA_JSON, "w", encoding="utf-8") as schema_file:
        schema_file.write(schema)


def print_diff(expected: str, observed: str):
    """Print differences between expected and observed files."""
    echo_failure("Differences in Config YAML:")
    for line in unified_diff(
        expected.splitlines(keepends=True),
        observed.splitlines(keepends=True),
        fromfile="expected",
        tofile="observed",
    ):
        print("   ", line.rstrip())


def check_docs():
    """Check whether the example config and config schema files documenting the config
    options are up to date.

    Raises:
        ValidationError: if not up to date.
    """

    schema_expected = get_schema()
    with open(CONFIG_SCHEMA_JSON, encoding="utf-8") as schema_file:
        schema_observed = schema_file.read()
    if schema_expected != schema_observed:
        raise ValidationError(
            f"Config schema JSON at '{CONFIG_SCHEMA_JSON}' is not up to date."
        )


def main(check: bool = False):
    """Update or check the config documentation files."""

    if check:
        try:
            check_docs()
        except ValidationError as error:
            echo_failure(f"Validation failed: {error}")
            sys.exit(1)
        echo_success("Config docs are up to date.")
        return

    update_docs()
    echo_success("Successfully updated the config docs.")


if __name__ == "__main__":
    run(main)
