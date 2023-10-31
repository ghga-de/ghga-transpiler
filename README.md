
[![tests](https://github.com/ghga-de/ghga-transpiler/actions/workflows/tests.yaml/badge.svg)](https://github.com/ghga-de/ghga-transpiler/actions/workflows/unit_and_int_tests.yaml)
[![Coverage Status](https://coveralls.io/repos/github/ghga-de/ghga-transpiler/badge.svg?branch=main)](https://coveralls.io/github/ghga-de/ghga-transpiler?branch=main)

# Ghga Transpiler

GHGA-Transpiler - excel to JSON converter

## Description

The GHGA Transpiler is a Python library and command line utility to transpile the official GHGA metadata XLSX workbooks to JSON. Please note that the GHGA Transpiler does not validate that the provided metadata is compliant with the [GHGA Metadata Schema](https://github.com/ghga-de/ghga-metadata-schema). This can be achieved by running the [GHGA Validator](https://github.com/ghga-de/ghga-validator/) on the JSON data generated by the GHGA Transpiler.


## Installation
We recommend installing the latest version of the GHGA transpiler using pip

```
pip install ghga-transpiler
```

### Usage:

```
Usage: ghga-transpiler [OPTIONS] SPREAD_SHEET [OUTPUT_FILE]

  ghga-transpiler is a command line utility to transpile the official GHGA
  metadata XLSX workbooks to JSON. Please note that ghga-transpiler does not
  validate that the provided metadata is compliant with the GHGA Metadata
  Schema. This can be achieved by running ghga-validator on the JSON data
  generated by the ghga-transpiler.

Arguments:
  SPREAD_SHEET   The path to input file (XLSX)  [required]
  [OUTPUT_FILE]  The path to output file (JSON).

Options:
  -f, --force                     Override output file if it exists.
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.
  --help                          Show this message and exit.
```
## Development
For setting up the development environment, we rely on the
[devcontainer feature](https://code.visualstudio.com/docs/remote/containers) of vscode
in combination with Docker Compose.

To use it, you have to have Docker Compose as well as vscode with its "Remote - Containers"
extension (`ms-vscode-remote.remote-containers`) installed.
Then open this repository in vscode and run the command
`Remote-Containers: Reopen in Container` from the vscode "Command Palette".

This will give you a full-fledged, pre-configured development environment including:
- infrastructural dependencies of the service (databases, etc.)
- all relevant vscode extensions pre-installed
- pre-configured linting and auto-formating
- a pre-configured debugger
- automatic license-header insertion

Moreover, inside the devcontainer, a convenience commands `dev_install` is available.
It installs the software with all development dependencies, installs pre-commit.

The installation is performed automatically when you build the devcontainer. However,
if you update dependencies in the [`./setup.cfg`](./setup.cfg) or the
[`./requirements-dev.txt`](./requirements-dev.txt), please run it again.

## License
This repository is free to use and modify according to the
[Apache 2.0 License](./LICENSE).

## Readme Generation
This readme is autogenerate, please see [`readme_generation.md`](./readme_generation.md)
for details.
