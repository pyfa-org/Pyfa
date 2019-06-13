def isCharCjk(char):
    # https://stackoverflow.com/questions/1366068/whats-the-complete-range-for-chinese-characters-in-unicode
    ranges = (
        ('\u4e00', '\u9fff'),
        ('\u3400', '\u4dbf'),
        ('\u20000', '\u2a6df'),
        ('\u2a700', '\u2b73f'),
        ('\u2b740', '\u2b81f'),
        ('\u2b820', '\u2ceaf'),
        ('\uf900', '\ufaff'),
        ('\u2f800', '\u2fa1f'),
        ('\uac00', '\ud7af'))
    for low, high in ranges:
        if low <= char <= high:
            return True
    return False


def isStringCjk(string):
    checked = set()
    for char in string:
        if char in checked:
            continue
        checked.add(char)
        if isCharCjk(char):
            return True
    return False
