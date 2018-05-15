# noinspection PyPackageRequirements
import wx
import sys
import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
# Add root to python paths, this allows us to import submodules
sys.path.append(os.path.realpath(os.path.join(script_dir, '..', '..')))

from _development.helpers_locale import GetPath, GetUnicodePath

class MyForm(wx.Frame):
    # ----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "CTRL-O to open, CTRL-S to save", size=(500, 500))

        # Add a panel so it looks the correct on all platforms
        panel = wx.Panel(self, wx.ID_ANY)

        SAVE_FILE_ID = wx.NewId()
        self.Bind(wx.EVT_MENU, self.saveFile, id=SAVE_FILE_ID)

        LOAD_FILE_ID = wx.NewId()
        self.Bind(wx.EVT_MENU, self.loadFile, id=LOAD_FILE_ID)

        accel_tbl = wx.AcceleratorTable([(wx.ACCEL_CTRL, ord('O'), LOAD_FILE_ID),
                                         (wx.ACCEL_CTRL, ord('S'), SAVE_FILE_ID)]
                                        )
        self.SetAcceleratorTable(accel_tbl)

    # ----------------------------------------------------------------------
    def loadFile(self, event):
        openFileDialog = wx.FileDialog(self, "Open", "", "",
                                       "Python files (*.py)|*.py",
                                       wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        openFileDialog.ShowModal()
        path = openFileDialog.GetPath()
        try:
            os_walk_without_codec = GetPath(path)
        except (UnicodeEncodeError, UnicodeTranslateError, UnicodeError, UnicodeDecodeError, UnicodeWarning, TypeError) as e:
            os_walk_without_codec = e

        try:
            os_walk_with_system_codec = GetPath(path, None, sys.getdefaultencoding())
        except (UnicodeEncodeError, UnicodeTranslateError, UnicodeError, UnicodeDecodeError, UnicodeWarning, TypeError) as e:
            os_walk_with_system_codec = e

        try:
            os_walk_unicode_without_codec = GetUnicodePath(path)
        except (UnicodeEncodeError, UnicodeTranslateError, UnicodeError, UnicodeDecodeError, UnicodeWarning, TypeError) as e:
            os_walk_unicode_without_codec = e

        try:
            os_walk_unicode_with_system_codec = GetUnicodePath(path, None, sys.getdefaultencoding())
        except (UnicodeEncodeError, UnicodeTranslateError, UnicodeError, UnicodeDecodeError, UnicodeWarning, TypeError) as e:
            os_walk_unicode_with_system_codec = e

        print("Simple print:")
        print(path)

        print("Type:")
        print((type(path)))

        print("OS Walk: No Codec:")
        print(os_walk_without_codec)

        print("OS Walk: Default System Codec:")
        print(os_walk_with_system_codec)

        print("OS Unicode Walk: No Codec:")
        print(os_walk_unicode_without_codec)

        print("OS Unicode Walk: Default System Codec:")
        print(os_walk_unicode_with_system_codec)
        openFileDialog.Destroy()

    # ----------------------------------------------------------------------
    def saveFile(self, event):
        saveFileDialog = wx.FileDialog(self, "Save As", "", "",
                                       "Python files (*.py)|*.py",
                                       wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        saveFileDialog.ShowModal()
        saveFileDialog.GetPath()
        saveFileDialog.Destroy()


# Run the program
if __name__ == "__main__":
    app = wx.App(False)
    frame = MyForm()
    frame.Show()
    app.MainLoop()
