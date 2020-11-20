#!/bin/bash
#
# build and push to testpypi

python setup.py sdist bdist_wheel
python -m twine upload -r pypitest dist/*
