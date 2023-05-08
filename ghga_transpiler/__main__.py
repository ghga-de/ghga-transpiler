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
from pathlib import Path

import typer
from typing_extensions import Annotated


def main(
    spread_sheet: Annotated[
        Path, typer.Option(None, exists=True, help="The path to the excel spread sheet")
    ]
):
    """Function to convert excel spread sheet to JSON

    Args:
        spread_sheet (Annotated[str, typer.Argument): The path to the excel spread sheet
    """
    if spread_sheet is None:
        print("No input spread sheet is provided")
        raise typer.Abort()


if __name__ == "__main__":
    typer.run(main)
