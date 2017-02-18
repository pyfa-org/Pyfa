from config import parsePath
import os


def test_parsePath():
    base = "C:\This\Is\A\Fake\Path"
    base = os.path.realpath(os.path.abspath(base))

    create_result = parsePath(base)

    assert create_result
    assert type(create_result) == unicode
    assert type(create_result) != str
    assert create_result == "C:\\This\\Is\\A\\Fake\\Path"

def test_parsePath_with_append():
    base = "C:\This\Is\A\Fake\Path"
    append = "file.py"
    base = os.path.realpath(os.path.abspath(base))

    create_result = parsePath(base, append)

    assert create_result
    assert type(create_result) == unicode
    assert type(create_result) != str
    assert create_result == "C:\\This\\Is\\A\\Fake\\Path\\file.py"
