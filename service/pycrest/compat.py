import sys

PY3 = sys.version_info[0] == 3

if PY3:  # pragma: no cover
    string_types = str,
    text_type = str
    binary_type = bytes
else:  # pragma: no cover
    string_types = basestring,
    text_type = unicode
    binary_type = str


def text_(s, encoding='latin-1', errors='strict'):  # pragma: no cover
    if isinstance(s, binary_type):
        return s.decode(encoding, errors)
    return s


def bytes_(s, encoding='latin-1', errors='strict'):  # pragma: no cover
    if isinstance(s, text_type):
        return s.encode(encoding, errors)
    return s
