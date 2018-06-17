# simulated.agency

## Description

Code for the project covered here: https://simulated.agency

## Requirements

You will need Python 3

Additional requirements are to be installed by executing `pip install -r requirements.txt`

## Running the Examples

1. Download the code
2. Change into the directory containing this README.md
3. Execute e.g. `python -m examples.game_of_life`

## Running the tests

1. Change into the directory containing this README.md
2. Execute `python -m pytest`, adding a `-v` flag for more detail

If you want to generate a coverage report then do this: `python -m pytest -v --cov=simulated_agency --cov-report=term`. Replace `term` with `html` to generate an HTML version of the coverage report identifying which code is not covered.
 