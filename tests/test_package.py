"""import tests."""

import importlib
import os
import sys

import pytest

# Workaround for Travis-CI so we can import directly from our module path
script_dir = os.path.dirname(os.path.abspath(__file__))
# Add Pyfa module to python paths
sys.path.append(os.path.realpath(os.path.join(script_dir, '..', '..')))

# Disabling test for now, issues importing :(
'''
from gui_service import *
from gui_service import __all__ as all_gui_services

def test_packages():
    # gui_service modules
    for _ in all_gui_services:
        assert _
'''


def service_modules():
    for root, folders, files in os.walk("gui_service"):
        for file_ in files:
            if file_.endswith(".py") and not file_.startswith("_"):
                mod_name = "{}.{}".format(
                    root.replace(os.path.sep, "."),
                    file_.split(".py")[0],
                )
                yield mod_name


@pytest.mark.parametrize("mod_name", service_modules())
def test_service_imports(mod_name):
    assert importlib.import_module(mod_name)
