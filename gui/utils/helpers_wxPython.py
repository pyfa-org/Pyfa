import wx


def YesNoDialog(question='Are you sure you want to do this?', caption='Yes or no?'):
    dlg = wx.MessageDialog(None, question, caption, wx.YES_NO | wx.ICON_QUESTION)
    result = dlg.ShowModal() == wx.ID_YES
    dlg.Destroy()
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