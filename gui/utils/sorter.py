"""
Taken from https://stackoverflow.com/questions/2669059/how-to-sort-alpha-numeric-set-in-python
"""

import re


def _convert(text):
    return int(text) if text.isdigit() else text


def smartSort(key):
    return [_convert(c) for c in re.split('([0-9]+)', key)]
