#!/usr/bin/env bash

echo "isort..."
poetry run isort --sp=pyproject.toml ./src ./tests
echo
echo "################################################################################"
echo

echo "autopep8..."
poetry run autopep8 --recursive --in-place --global-config=pyproject.toml ./src ./tests
echo
echo "################################################################################"
echo
