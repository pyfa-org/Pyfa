# Hebrew

import os
import platform
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
# Add root to python paths, this allows us to import submodules
sys.path.append(os.path.realpath(os.path.join(script_dir, '..', '..', '..')))

from _development.helpers_locale import GetPath


def test_codec_hebrew():
    use_codec = {
        "Windows": "cp1252",
        "Linux"  : "utf8",
        "Darwin" : "utf8",
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
