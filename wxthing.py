import wx


# Custom class that forces the TextEntryDialog to accept a Validator on the TextCtrl
class TextEntryValidatedDialog(wx.TextEntryDialog):
    def __init__(self, parent, validator=None, *args, **kargs):
        wx.TextEntryDialog.__init__(self, parent, *args, **kargs)
        self.parent = parent

        self.txtctrl = self.FindWindowById(3000)
        if validator:
            self.txtctrl.SetValidator(validator())

# Define a base Validator class that all other Validators will extend
class BaseValidator(wx.Validator):
    def __init__(self):
        wx.Validator.__init__(self)

    def Validate(self, win):
        raise NotImplementedError()

    def TransferToWindow(self):
        return True

    def TransferFromWindow(self):
        return True

# Define my Custom Validator
class MyTextValidator(BaseValidator):
    def __init__(self):
        BaseValidator.__init__(self)

    def Clone(self):
        return MyTextValidator()

    def Validate(self, win):
        print("Validating!")
        textCtrl = self.GetWindow()
        text = textCtrl.GetValue().strip()
        try:
            if len(text) == 0:
                raise ValueError("You must supply a value!")
            elif text == "error":
                raise ValueError("Simulate another error!")
            return True
        except ValueError as e:
            wx.MessageBox("{}".format(e), "Error")
            textCtrl.SetFocus()
            return False


class MyForm(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, "List Control Tutorial")

        # Add a panel so it looks the correct on all platforms
        panel = wx.Panel(self, wx.ID_ANY)
        self.index = 0

        btn = wx.Button(panel, label="Pop Dialog")
        btn.Bind(wx.EVT_BUTTON, self.pop_dialog)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(btn, 0, wx.ALL | wx.CENTER, 5)
        panel.SetSizer(sizer)

    def pop_dialog(self, event):
        dlg = TextEntryValidatedDialog(self, MyTextValidator,
                                       "Enter some text here (or \"error\" if you want to simulate a validation failure",
                                       "Thing")
        dlg.txtctrl.SetInsertionPointEnd()
        dlg.CenterOnParent()

        if dlg.ShowModal() == wx.ID_OK:
            print("Entered Value: "+dlg.txtctrl.GetValue().strip())


if __name__ == "__main__":
    app = wx.App(False)
    frame = MyForm()
    frame.Show()
    app.MainLoop()