#!/bin/bash

pipenv run server &

sleep 5

pipenv run python -m webbrowser http://localhost:8000


