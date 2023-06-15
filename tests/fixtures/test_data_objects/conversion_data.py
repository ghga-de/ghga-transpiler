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

"""Data that are used in unit tests"""

CONFIG_DICT = {
    "library_version": 1.0,
    "default_settings": {
        "header_row": 1,
        "start_row": 2,
        "start_column": 1,
        "end_column": 2,
    },
    "worksheets": [
        {"sheet_name": "books", "settings": {"name": "books", "end_column": 3}},
        {
            "sheet_name": "publisher",
            "settings": {"name": "publisher"},
        },
    ],
}


EXPECTED_CONVERSION = {
    "books": [
        {
            "writer_name": "Albert Camus",
            "book_name": "The Plague",
            "isbn": "9780679720218",
        },
        {
            "writer_name": "George Orwell",
            "book_name": "1984",
            "isbn": "9783548234106",
        },
    ],
    "publisher": [
        {"isbn": "9780679720218", "publisher_name": "Hamish Hamilton"},
        {"isbn": "9783548234106", "publisher_name": "Secker and Warburg"},
    ],
}
