import os

import wx


def isWayland():
    """
    Whether we are drawing through wayland rather than X.

    Worth knowing because wayland does not let a client place its own windows on screen, so
    anything which relies on positioning a window under the cursor cannot work there.
    """
    if 'wxGTK' not in wx.PlatformInfo:
        return False
    # an explicit choice wins, including "x11" while sitting in a wayland session
    backend = os.environ.get('GDK_BACKEND', '')
    if backend:
        return backend.split(',')[0].strip().lower() == 'wayland'
    return bool(os.environ.get('WAYLAND_DISPLAY'))


def YesNoDialog(question='Are you sure you want to do this?', caption='Yes or no?'):
    with wx.MessageDialog(None, question, caption, wx.YES_NO | wx.ICON_QUESTION) as dlg:
        result = dlg.ShowModal() == wx.ID_YES
    return result


def HandleCtrlBackspace(textControl):
    """
    Handles the behavior of Windows ctrl+space
    deletes everything from the cursor to the left,
    up to the next whitespace.
    """
    curPos = textControl.GetInsertionPoint()
    searchText = textControl.GetValue()
    foundChar = False
    for startIndex in range(curPos, -1, -1):
        if startIndex - 1 < 0:
            break
        if searchText[startIndex - 1] != " ":
            foundChar = True
        elif foundChar:
            break
    textControl.Remove(startIndex, curPos)
    textControl.SetInsertionPoint(startIndex)
