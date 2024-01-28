### GPT4ALL
Part of this repo is a [helper script](#helper-cli-script) providing cli utility for development in the form of easy to use predefined commands
## Installing dependencies
1. install invoke and pip-tools
`pip install invoke pip-tools`
2. use the [helper script](#helper-cli-script) to install dependencies
`inv sync`

## Helper CLI script
Commands for:
* installing dependencies
* building the project into a package
* creating documentation
* deploying the package

can be found inside the `task.py` file.
You can use `inv --list` to see all available commands and read their docstrings and you can do
`inv <command_name> --help`
to get more information about a single command.
In case you want to expand this utility I suggest reading the introduction of the [invoke documentation](https://www.pyinvoke.org/).

## apt dependencies
```
python3.11 python-dev libpq-dev
```