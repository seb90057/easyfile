#!/bin/bash
#
# Compute and report code coverage

source venv/Scripts/activate
export PYTHONPATH=src
coverage erase && coverage run -m unittest discover && coverage html