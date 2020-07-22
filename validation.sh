#!/usr/bin/env bash
set -ex

isort -rc mfa tests
black --line-length 120 --target-version py36 mfa tests
pydocstyle mfa --add-ignore=D204,D403
mypy mfa
flake8 mfa tests
pylint -j 0 mfa
