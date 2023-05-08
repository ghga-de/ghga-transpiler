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

"""
Module containing the main FastAPI router and (optionally) top-level API enpoints.
Additional endpoints might be structured in dedicated modules
(each of them having a sub-router).

THIS INCLUDES PLACE HOLDERS. API IS NOT IMPLEMENTED
"""

from fastapi import FastAPI
from ghga_service_commons.api import configure_app

from ..config import CONFIG

app = FastAPI()
configure_app(app, config=CONFIG)


@app.post("/upload", summary="Upload excel spread-sheet")
async def upload_spread_sheet():
    """_summary_

    Returns:
        _type_: _description_
    """
    return "uploaded"


@app.get("/convert", summary="Convert excel spread-sheet to json")
async def convert_spread_sheet():
    """_summary_

    Returns:
        _type_: _description_
    """
    return "converted"


@app.get("/download_json", summary="Download json")
async def download_spread_sheet():
    """_summary_

    Returns:
        _type_: _description_
    """
    return "downloaded"
