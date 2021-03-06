#!/usr/bin/env bash

echo "bandit..."
poetry run bandit -vr --ini ./config.ini ./src
echo
echo "################################################################################"
echo

echo "flake8..."
poetry run flake8 --config=config.ini ./src
echo
echo "################################################################################"
echo

echo "mypy..."
poetry run mypy --config-file=config.ini ./src
echo
echo "################################################################################"
echo

echo "isort..."
poetry run isort --check --diff --sp=pyproject.toml ./src ./tests
echo
echo "################################################################################"
echo

echo "autopep8..."
poetry run autopep8 --recursive --diff --global-config=pyproject.toml ./src ./tests
echo
echo "################################################################################"
echo
