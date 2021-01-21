#!/bin/bash

poetry run isort .
poetry run black .
poetry run pylint good_place/*