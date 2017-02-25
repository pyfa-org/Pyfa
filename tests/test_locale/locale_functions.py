import os

# https://msdn.microsoft.com/en-us/library/windows/desktop/dd317756(v=vs.85).aspx
windows_codecs = {
    'cp1252',  # Standard Windows
    'cp1251',  # Russian
    'cp037',
    'cp424',
    'cp437',
    'cp500',
    'cp720',
    'cp737',
    'cp775',
    'cp850',
    'cp852',
    'cp855',
    'cp856',
    'cp857',
    'cp858',
    'cp860',
    'cp861',
    'cp862',
    'cp863',
    'cp864',
    'cp865',
    'cp866',
    'cp869',
    'cp874',
    'cp875',
    'cp932',
    'cp949',
    'cp950',
    'cp1006',
    'cp1026',
    'cp1140',
    'cp1250',
    'cp1253',
    'cp1254',
    'cp1255',
    'cp1256',
    'cp1257',
    'cp1258',
}

linux_codecs = {
    'utf_8',  # Generic Linux/Mac
}

mac_codecs = [
    'utf_8',  # Generic Linux/Mac
    'mac_cyrillic',
    'mac_greek',
    'mac_iceland',
    'mac_latin2',
    'mac_roman',
    'mac_turkish',
]

universal_codecs = [
    'utf_16', 'utf_32', 'utf_32_be', 'utf_32_le', 'utf_16_be', 'utf_16_le', 'utf_7', 'utf_8_sig',
]

other_codecs = [
    'scii', 'big5', 'big5hkscs', 'euc_jp', 'euc_jis_2004', 'euc_jisx0213', 'euc_kr', 'gb2312', 'gbk', 'gb18030', 'hz', 'iso2022_jp', 'iso2022_jp_1',
    'iso2022_jp_2', 'iso2022_jp_2004', 'iso2022_jp_3', 'iso2022_jp_ext', 'iso2022_kr', 'latin_1', 'iso8859_2', 'iso8859_3', 'iso8859_4', 'iso8859_5',
    'iso8859_6', 'iso8859_7', 'iso8859_8', 'iso8859_9', 'iso8859_10', 'iso8859_11', 'iso8859_13', 'iso8859_14', 'iso8859_15', 'iso8859_16', 'johab', 'koi8_r',
    'koi8_u', 'ptcp154', 'shift_jis', 'shift_jis_2004', 'shift_jisx0213'
]

system_names = {
    'Windows': windows_codecs,
    'Linux': linux_codecs,
    'Darwin': mac_codecs,
}


def GetPath(root, file=None, codec=None):
    # Replace this with the function we actually use for this
    path = os.path.realpath(os.path.abspath(root))

    if file:
        path = os.path.join(path, file)

    if codec:
        path = path.decode(codec)

    return path

def GetUnicodePath(root, file=None, codec=None):
    # Replace this with the function we actually use for this
    path = os.path.realpath(os.path.abspath(root))

    if file:
        path = os.path.join(path, file)

    if codec:
        path = unicode(path, codec)
    else:
        path = unicode(path)

    return path
