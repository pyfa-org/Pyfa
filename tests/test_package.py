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

from gui_service import __all__ as all_gui_services
from gui_service import attribute
from gui_service import character
from gui_service import crest
from gui_service import damagePattern
from gui_service import eveapi
from gui_service import fit
from gui_service import fleet
from gui_service import implantSet
from gui_service import market
from gui_service import network
from gui_service import port
from gui_service import prefetch
from gui_service import price
from gui_service import server
from gui_service import settings
from gui_service import targetResists
from gui_service import update


def test_packages():
    # gui_service modules
    assert attribute
    assert character
    assert crest
    assert damagePattern
    assert eveapi
    assert fit
    assert fleet
    assert implantSet
    assert market
    assert network
    assert port
    assert prefetch
    assert price
    assert server
    assert settings
    assert targetResists
    assert update
    for _ in all_gui_services:
        assert _


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
