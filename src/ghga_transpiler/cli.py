# Copyright 2021 - 2024 Universität Tübingen, DKFZ, EMBL, and Universität zu Köln
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
"""CLI-specific wrappers around core functions."""

import sys
from pathlib import Path

import typer

from ghga_transpiler.core import convert_workbook, produce_datapack

from . import __version__, io

# from .core import InvalidSematicVersion, convert_workbook
from .exceptions import UnknownVersionError

cli = typer.Typer()


def version_callback(value: bool):
    """Prints the package version"""
    if value:
        print(__version__)
        raise typer.Exit()


@cli.command()
def transpile(
    spread_sheet: Path = typer.Argument(
        ...,
        exists=True,
        help="The path to input file (XLSX)",
        dir_okay=False,
        readable=True,
    ),
    output_file: Path | None = typer.Argument(
        None, help="The path to output file (JSON).", dir_okay=False
    ),
    force: bool = typer.Option(
        False, "--force", "-f", help="Override output file if it exists."
    ),
    transpiler_protocol: bool = typer.Option(
        False,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Print package version",
    ),
):
    """ghga-transpiler is a command line utility to transpile the official GHGA
    metadata XLSX workbooks to JSON. TODO Validation
    """
    try:
        ghga_workbook = convert_workbook(spread_sheet)
    except (SyntaxError, UnknownVersionError) as exc:
        sys.exit(f"Unable to parse input file '{spread_sheet}': {exc}")

    converted = produce_datapack(ghga_workbook)

    try:
        io.write_datapack(data=converted, path=output_file, force=force)
    except FileExistsError as exc:
        sys.exit(f"ERROR: {exc}")
