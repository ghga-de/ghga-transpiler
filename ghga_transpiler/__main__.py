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

"""Entrypoint of the package"""
import json
from pathlib import Path

import typer
from config.config import CONFIG
from core.convert import convert_rows, get_header, get_worksheet_rows, read_workbook
from typing_extensions import Annotated


def convert_workbook(filename: Path) -> dict:
    """Function to run steps for conversion

    Args:
        filename (Path): _description_

    Returns:
        dict: dictionary of worksheet names as keys and list of sheet row values as values.
    """
    converted_workbook = {}
    workbook = read_workbook(str(filename))
    for sheet_name in workbook.sheetnames:
        worksheet = workbook[sheet_name]
        sheet_annotation = getattr(CONFIG, sheet_name)
        rows = get_worksheet_rows(
            worksheet,
            sheet_annotation["start_row"],
            sheet_annotation["end_row"],
            sheet_annotation["start_column"],
            sheet_annotation["end_column"],
        )
        header = get_header(CONFIG, sheet_name, rows)
        converted_workbook[sheet_annotation["name"]] = convert_rows(header, rows[1:])
    return converted_workbook


def main(
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

    with open("metadata.json", "w", encoding="utf-8") as file:
        json.dump(convert_workbook(spread_sheet), file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    typer.run(main)
