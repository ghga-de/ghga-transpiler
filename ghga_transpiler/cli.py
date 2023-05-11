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
""" CLI-specific wrappers around core functions."""
import json
from pathlib import Path

import typer
from typing_extensions import Annotated

HERE = Path(__file__).parent.resolve()
DEFAULT_OUTPUT_FILE = HERE / "transpiled_metadata.yaml"

cli = typer.Typer()


def convert_workbook(filename: Path):
    """Function to run steps for conversion

    Args:
        filename: Path to input spread sheet

    """
    return filename


@cli.command()
def input_files(
    spread_sheet: Annotated[
        Path, typer.Option(None, exists=True, help="The path to input file")
    ],
    config: Annotated[
        Path,
        typer.Option(
            None,
            envvar="GHGA_TRANSPILER_CONFIG_YAML",
            help="Variable pointing config file",
        ),
    ],
    output_file: Annotated[Path, typer.Option(None, help="The path to output file")],
):
    """Function to convert excel spread sheet to JSON

    Args:
        spread_sheet (Annotated[str, typer.Argument): The path to the excel spread sheet
    """
    if spread_sheet is None:
        print("No input spread sheet is provided")
        raise typer.Abort()

    if config is None:
        print("No input spread sheet is provided")
        raise typer.Abort()

    if output_file is None:
        print("No input spread sheet is provided")
        output_file = DEFAULT_OUTPUT_FILE

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(convert_workbook(spread_sheet), file, ensure_ascii=False, indent=4)
