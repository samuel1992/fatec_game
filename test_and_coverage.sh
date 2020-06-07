#!/bin/sh

echo "\nChecking coverage for Python code\n"

COV_THRESHOLD=100;
coverage run --source=game --omit='game/migrations/*' manage.py test
coverage report -m
