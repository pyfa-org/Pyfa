# Add root folder to python paths
# This must be done on every test in order to pass in Travis
import os
import sys
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.realpath(os.path.join(script_dir, '..', '..', '..')))

from gui.aboutData import versionString, licenses, developers, credits, description


def test_aboutData():
    """
    Simple test to validate all about data exists
    """
    assert versionString.__len__() > 0
    assert licenses.__len__() > 0
    assert developers.__len__() > 0
    assert credits.__len__() > 0
    assert description.__len__() > 0
