"""import tests."""

import importlib
import os
import sys

import pytest

# Work around for Travic-CI to be able to import modules directly from out path
script_dir = os.path.dirname(os.path.abspath(__file__))
# Add Gnosis module to python paths
sys.path.append(os.path.realpath(os.path.join(script_dir, '..', '..')))
sys.path.append(os.path.realpath(os.path.join(script_dir, '..')))

import eos


def test_packages():
    # gui_service modules
    assert eos


def service_modules():
    for root, folders, files in os.walk("gui_service"):
        for file_ in files:
            if file_.endswith(".py") and not file_.startswith("_"):
                mod_name = "{}.{}".format(
                    root.replace(os.path.sep, "."),
                    file_.split(".py")[0],
                )
                yield mod_name


def eos_modules():
    for root, folders, files in os.walk("eos"):
        for file_ in files:
            if file_.endswith(".py") and not file_.startswith("_"):
                mod_name = "{}.{}".format(
                    root.replace(os.path.sep, "."),
                    file_.split(".py")[0],
                )
                yield mod_name


@pytest.mark.parametrize("mod_name", eos_modules())
def test_service_imports(mod_name):
    assert importlib.import_module(mod_name)
