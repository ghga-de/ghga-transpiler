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
from typing import Optional

import typer

from .process_workbook import convert_workbook, params

cli = typer.Typer()


@cli.command()
def cli_main(
    spread_sheet: Path = typer.Argument(
        ...,
        exists=True,
        help="The path to input file",
        dir_okay=False,
        readable=True,
    ),
    output_file: Optional[Path] = typer.Argument(None, help="The path to output file."),
    force: bool = typer.Option(
        False, "--force", "-f", help="Override output file if it exists."
    ),
):
    """Function to get options and channel those to the convert workbook functionality"""
    workbook, config = params(spread_sheet)
    if output_file is None:
        print(convert_workbook(workbook, config))
    elif output_file.exists() and not force:
        print(f"{output_file} exits.")
        raise typer.Abort()
    else:
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(
                convert_workbook(workbook, config),
                file,
                ensure_ascii=False,
                indent=4,
            )
