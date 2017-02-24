from config import parsePath
import os


def test_parsePath():
    basepath = "\This\Is\A\Fake\Path"
    base = os.path.normpath(basepath)

    create_result = parsePath(base)

    assert create_result
    assert type(create_result) == unicode
    assert type(create_result) != str
    assert create_result == "\\This\\Is\\A\\Fake\\Path"


def test_parsePath_with_append():
    basepath = "\This\Is\A\Fake\Path"
    append = "file.py"
    base = os.path.normpath(basepath)

    create_result = parsePath(base, append)

    assert create_result
    assert type(create_result) == unicode
    assert type(create_result) != str
    # On Linux this can show differently. Left side for Windows, right side for Linux.
    assert (create_result == "\\This\\Is\\A\\Fake\\Path\\file.py" or create_result == "\This\Is\A\Fake\Path/file.py")
