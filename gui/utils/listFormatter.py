def formatList(words):
    """Transforms ("a", "b", "c") into "a, b and c" string"""
    if not words:
        return ""
    if len(words) == 1:
        return words[0]
    last = words[-1:][0]
    beginning = ", ".join(words[:-1])
    return "{0} and {1}".format(beginning, last)
