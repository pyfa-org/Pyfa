# Russian

import os
import platform
from tests.test_locale.locale_functions import GetPath


def test_codec():
    use_codec = {
        "Windows": "cp1251",
        "Linux"  : "utf8",
        "Darwin" : "mac_cyrillic",
    }

    os_name = platform.system()
    current_directory = os.path.dirname(os.path.abspath(__file__))

    try:
        decoded_file = GetPath(current_directory, "testcodec", use_codec[os_name])
    except:
        assert False, "Specified codec (" + use_codec[os_name] + ") failed to decrypt file path."

    try:
        with open(decoded_file, 'r') as f:
            read_data = f.read()
        f.closed
    except:
        assert False, "Specified codec (" + use_codec[os_name] + ") failed to read file."

    assert read_data == "True"
