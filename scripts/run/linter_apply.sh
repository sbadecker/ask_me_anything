#!/usr/bin/env bash

echo "isort..."
poetry run isort --sp=pyproject.toml ./src ./tests
echo
echo "################################################################################"
echo

echo "black..."
poetry run black --config=pyproject.toml ./src ./tests
echo
echo "################################################################################"
echo
