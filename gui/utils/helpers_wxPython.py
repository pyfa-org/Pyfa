import wx


def YesNoDialog(question=u'Are you sure you want to do this?', caption=u'Yes or no?'):
    dlg = wx.MessageDialog(None, question, caption, wx.YES_NO | wx.ICON_QUESTION)
    result = dlg.ShowModal() == wx.ID_YES
    dlg.Destroy()
    return result
