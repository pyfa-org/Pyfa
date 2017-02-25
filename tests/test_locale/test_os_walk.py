import os
import platform
from tests.test_locale.locale_functions import GetPath

def test_os_walk():
    os_name = platform.system()
    current_directory = os.path.dirname(os.path.abspath(unicode(__file__)))
    subfolders = os.listdir(current_directory)
    subfolders = [e for e in subfolders if not (e.endswith(".py") or e.endswith(".pyc") or e.endswith(".md"))]

    subfolder_count = 0
    for subfolder in subfolders:
        subdir = GetPath(current_directory, subfolder)
        testfile = GetPath(subdir, "testcodec")

        try:
            with open(testfile, 'r') as f:
                read_data = f.read()
            f.closed
        except:
            assert False, "Failed to read file."

        assert read_data == "True"
        subfolder_count += 1

    assert len(subfolders) == subfolder_count