"""import tests."""

import os
import sys
import importlib

import pytest

# Workaround for Travis-CI so we can import directly from our module path
script_dir = os.path.dirname(os.path.abspath(__file__))
# Add Pyfa module to python paths
sys.path.append(os.path.realpath(os.path.join(script_dir, '..', '..')))

import gui
import gui_service
import eos
import utils


def test_packages():
    assert gui_service
    assert gui
    assert eos
    assert utils


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
