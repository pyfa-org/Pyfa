import sys
import inspect
import re
import platform

version_block = ''


class PreCheckException(Exception):
    pass


class PreCheckMessage():
    def __init__(self, msg):
        # wx may not be installed, in which case print to console. For all other prechecks, should pop up a MessageDialog
        try:
            import wx
            app = wx.App(False)
            wx.MessageBox(msg, 'Error', wx.ICON_ERROR | wx.STAY_ON_TOP)
            app.MainLoop()
        except:
            pass
        finally:
            print(msg)


def version_precheck():
    global version_block

    version_block += "\nOS version: {}".format(platform.platform())
    version_block += "\nPython version: {}".format(sys.version)

    if sys.version_info < (3, 6):
        msg = "pyfa requires python 3.6"
        raise PreCheckException(msg)

    try:
        # the way that the version string is imported in wx is odd, causing us to have to split out the imports like this. :(
        from wx.__version__ import VERSION, VERSION_STRING

        if VERSION[0] < 4:
            raise Exception()
        if VERSION[3] != '':
            if VERSION[3][0] == 'b' and int(VERSION[3][-1]) < 2:
                raise Exception()

        import wx
        version_block += "\nwxPython version: {} ({})".format(VERSION_STRING, wx.wxWidgets_version)
    except:
        msg = "pyfa requires wxPython v4.0.0b2+. You can download wxPython from https://wxpython.org/pages/downloads/"
        raise PreCheckException(msg)

    try:
        import sqlalchemy
        saMatch = re.match("([0-9]+).([0-9]+).([0-9]+)(([b\.])([0-9]+))?", sqlalchemy.__version__)
        version_block += "\nSQLAlchemy version: {}".format(sqlalchemy.__version__)

        if (int(saMatch.group(1)), int(saMatch.group(2)), int(saMatch.group(3))) < (1, 0, 5):
            raise Exception()
    except:
        msg = "pyfa requires SQLAlchemy v1.0.5+. You can download SQLAlchemy from https://www.sqlalchemy.org/download.html"
        raise PreCheckException(msg)

    try:
        import logbook
        logVersion = logbook.__version__.split('.')
        version_block += "\nLogbook version: {}".format(logbook.__version__)

        if int(logVersion[0]) < 1:
            raise Exception()
    except:
        raise PreCheckException("pyfa requires Logbook version 1.0.0+. You can download Logbook from https://pypi.python.org/pypi/Logbook")

    try:
        import requests
        version_block += "\nRequests version: {}".format(requests.__version__)
    except:
        msg = "pyfa requires the requests module. You can download requests from https://pypi.python.org/pypi/requests"
        raise PreCheckException(msg)

    try:
        import dateutil
        version_block += "\nDateutil version: {}".format(dateutil.__version__)
    except:
        msg = "pyfa requires the python-dateutil module. You can download python-dateutil form https://pypi.python.org/pypi/python-dateutil"
        raise PreCheckException(msg)
