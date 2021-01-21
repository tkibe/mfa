#!/usr/bin/env bash
set -ex

isort mfa
black --line-length 120 --target-version py37 mfa
pydocstyle mfa --add-ignore=D204,D403
mypy mfa
flake8 mfa
pylint --max-line-length=120 -j 0 mfa
pipenv check