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

from ghga_transpiler.config.config import Config, read_config
from ghga_transpiler.config.exceptions import MissingWorkbookContent
from ghga_transpiler.core.core import (
    convert_rows,
    get_header,
    get_worksheet_rows,
    read_workbook,
)

HERE = Path(__file__).parent.resolve()
DEFAULT_OUTPUT_FILE = HERE / "transpiled_metadata.yaml"

cli = typer.Typer()

CONFIG = Config.parse_obj(read_config())


def convert_workbook(filename: Path):
    """Function to run steps for conversion"""
    converted_workbook = {}
    workbook = read_workbook(str(filename))
    for sheet in CONFIG.worksheets:
        try:
            rows = get_worksheet_rows(
                workbook[sheet.sheet_name],
                sheet.settings.start_row,
                workbook[sheet.sheet_name].max_row,
                sheet.settings.start_column,
                sheet.settings.end_column,
            )
            converted_workbook[sheet.sheet_name] = convert_rows(
                get_header(rows), rows[1:]
            )
            return converted_workbook
        except KeyError as exc:
            raise MissingWorkbookContent(
                f"Workbook does not contain {sheet.sheet_name} worksheet."
            ) from exc


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
):
    """Function to convert excel spread sheet to JSON"""

    if output_file is None:
        print(convert_workbook(spread_sheet))
    elif output_file.exists():
        print(f"{output_file} exits.")
        raise typer.Abort()
    else:
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(
                convert_workbook(spread_sheet), file, ensure_ascii=False, indent=4
            )
