<!--
 Copyright 2021 - 2024 Universität Tübingen, DKFZ, EMBL, and Universität zu Köln
 for the German Human Genome-Phenome Archive (GHGA)

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.

-->

# Generating the pyproject.toml

The pyproject.toml of the service is generated by combining static configuration
captured in [`./pyproject_template.toml`](./pyproject_template.toml) and custom
package metadata specified in [`./pyproject_custom.toml`](./pyproject_custom.toml).

The `./pyproject_template.toml` is managed by the template, please do not edit manually.

You may specify properties in the `./pyproject_custom.toml` which are already specified
in the `./pyproject_template.toml`. In that case, the `./pyproject_custom.toml` takes
priority.