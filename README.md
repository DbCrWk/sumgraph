# sumgraph

![ci workflow badge](https://github.com/DbCrWk/sumgraph/actions/workflows/ci.yml/badge.svg?branch=develop)

![sumgraph](/logo/logo.png)

This package prodives `python`-based utilities for working with dynamic graphs and their summariziation.

## Authors

- Zara Memon ([@zm600](https://github.com/zm600))
- Dev Dabke ([@DbCrWk](https://github.com/DbCrWk))

## Dependencies

Please ensure that you have:

- `python` installed, ideally through `pyenv`
- `poetry` installed
- `make` installed

## Development

For first-time setup, run

```bash
make setup
```

Afterwards, when working on the project, run

```bash
source .venv/bin/activate
```

We use [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) for commit messages.
Please branch off of the `develop` branch and write code in a feature branch.
Then, open a pull request to merge into `develop`.
