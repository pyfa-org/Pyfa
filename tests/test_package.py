"""import tests."""

import os
import sys
import importlib

# noinspection PyPackageRequirements
import pytest


script_dir = os.path.dirname(os.path.abspath(__file__))
# Add root to python paths, this allows us to import submodules
sys.path.append(os.path.realpath(os.path.join(script_dir, '..')))

# noinspection PyPep8
import service
# noinspection PyPep8
import gui
# noinspection PyPep8
import eos
# noinspection PyPep8
import utils


def test_packages():
    assert service
    assert gui
    assert eos
    assert utils


def service_modules():
    for root, folders, files in os.walk("service"):
        for file_ in files:
            if file_.endswith(".py") and not file_.startswith("_"):
                mod_name = "{}.{}".format(
                    root.replace("/", "."),
                    file_.split(".py")[0],
                )
                yield mod_name


def eos_modules():
    for root, folders, files in os.walk("eos"):
        for file_ in files:
            if file_.endswith(".py") and not file_.startswith("_"):
                mod_name = "{}.{}".format(
                    root.replace("/", "."),
                    file_.split(".py")[0],
                )
                yield mod_name

# TODO: Disable walk through Eos paths until eos.types is killed.  eos.types causes the import to break
'''
@pytest.mark.parametrize("mod_name", eos_modules())
def test_eos_imports(mod_name):
    assert importlib.import_module(mod_name)
'''
