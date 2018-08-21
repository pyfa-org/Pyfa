# noinspection PyPackageRequirements
import wx
from gui.bitmap_loader import BitmapLoader


class BaseValidator(wx.Validator):
    def __init__(self):
        wx.Validator.__init__(self)

    def Validate(self, win):
        raise NotImplementedError()

    def TransferToWindow(self):
        return True

    def TransferFromWindow(self):
        return True


class TextEntryValidatedDialog(wx.TextEntryDialog):
    def __init__(self, parent, validator=None, *args, **kargs):
        wx.TextEntryDialog.__init__(self, parent, *args, **kargs)
        self.parent = parent

        # See https://github.com/wxWidgets/Phoenix/issues/611
        self.txtctrl = self.FindWindowById(3000, self)

        if validator:
            self.txtctrl.SetValidator(validator())


class EntityEditor(wx.Panel):
    """
    Entity Editor is a panel that takes some sort of list as a source and populates a drop down with options to add/
    rename/clone/delete an entity. Comes with dialogs that take user input. Classes that derive this class must override
    functions that get the list from the source, what to do when user does an action, and how to validate the input.
    """

    def __init__(self, parent, entityName):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, style=wx.TAB_TRAVERSAL)
        self.entityName = entityName
        self.validator = None
        self.navSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.choices = []
        self.choices.sort(key=lambda p: p.name)
        self.entityChoices = wx.Choice(self, choices=[p.name for p in self.choices])
        self.navSizer.Add(self.entityChoices, 1, wx.ALL, 5)

        buttons = (("new", wx.ART_NEW, self.OnNew),
                   ("rename", BitmapLoader.getBitmap("rename", "gui"), self.OnRename),
                   ("copy", wx.ART_COPY, self.OnCopy),
                   ("delete", wx.ART_DELETE, self.OnDelete))

        size = None
        for name, art, func in buttons:
            bitmap = wx.ArtProvider.GetBitmap(art, wx.ART_BUTTON) if name != "rename" else art
            btn = wx.BitmapButton(self, wx.ID_ANY, bitmap)
            if size is None:
                size = btn.GetSize()

            btn.SetMinSize(size)
            btn.SetMaxSize(size)

            btn.SetToolTip("{} {}".format(name.capitalize(), self.entityName))
            btn.Bind(wx.EVT_BUTTON, func)
            setattr(self, "btn%s" % name.capitalize(), btn)
            self.navSizer.Add(btn, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 2)

        self.SetSizer(self.navSizer)
        self.Layout()

        self.refreshEntityList()

    def SetEditorValidator(self, validator=None):
        """ Sets validator class (not an instance of the class) """
        self.validator = validator

    def getEntitiesFromContext(self):
        """ Gets list of entities from current context """
        raise NotImplementedError()

    def DoNew(self, name):
        """Override method to do new entity logic. Must return the new entity"""
        raise NotImplementedError()

    def DoCopy(self, entity, name):
        """Override method to copy entity. Must return the copy"""
        raise NotImplementedError()

    def DoRename(self, entity, name):
        """Override method to rename an entity"""
        raise NotImplementedError()

    def DoDelete(self, entity):
        """Override method to delete entity"""
        raise NotImplementedError()

    def OnNew(self, event):
        dlg = TextEntryValidatedDialog(self, self.validator,
                                       "Enter a name for your new {}:".format(self.entityName),
                                       "New {}".format(self.entityName))
        dlg.CenterOnParent()

        if dlg.ShowModal() == wx.ID_OK:
            # using dlg.textctrl.GetValue instead of simply dlg.GetValue because the proper way does not work in wxPython 2.8
            new = self.DoNew(dlg.txtctrl.GetValue().strip())
            self.refreshEntityList(new)
            wx.PostEvent(self.entityChoices, wx.CommandEvent(wx.wxEVT_COMMAND_CHOICE_SELECTED))
        else:
            return False

    def OnCopy(self, event):
        dlg = TextEntryValidatedDialog(self, self.validator,
                                       "Enter a name for your {} copy:".format(self.entityName),
                                       "Copy {}".format(self.entityName))
        active = self.getActiveEntity()
        dlg.SetValue("{} Copy".format(active.name))
        dlg.txtctrl.SetInsertionPointEnd()
        dlg.CenterOnParent()

        if dlg.ShowModal() == wx.ID_OK:
            copy = self.DoCopy(active, dlg.txtctrl.GetValue().strip())
            self.refreshEntityList(copy)
            wx.PostEvent(self.entityChoices, wx.CommandEvent(wx.wxEVT_COMMAND_CHOICE_SELECTED))

    def OnRename(self, event):
        dlg = TextEntryValidatedDialog(self, self.validator,
                                       "Enter a new name for your {}:".format(self.entityName),
                                       "Rename {}".format(self.entityName))
        active = self.getActiveEntity()
        dlg.SetValue(active.name)
        dlg.txtctrl.SetInsertionPointEnd()
        dlg.CenterOnParent()

        if dlg.ShowModal() == wx.ID_OK:
            self.DoRename(active, dlg.txtctrl.GetValue().strip())
            self.refreshEntityList(active)
            wx.PostEvent(self.entityChoices, wx.CommandEvent(wx.wxEVT_COMMAND_CHOICE_SELECTED))

    def OnDelete(self, event):
        dlg = wx.MessageDialog(self,
                               "Do you really want to delete the {} {}?".format(self.getActiveEntity().name,
                                                                                self.entityName),
                               "Confirm Delete", wx.YES | wx.NO | wx.ICON_QUESTION)
        dlg.CenterOnParent()

        if dlg.ShowModal() == wx.ID_YES:
            self.DoDelete(self.getActiveEntity())
            self.refreshEntityList()
            wx.PostEvent(self.entityChoices, wx.CommandEvent(wx.wxEVT_COMMAND_CHOICE_SELECTED))

    def refreshEntityList(self, selected=None):
        self.choices = self.getEntitiesFromContext()
        self.entityChoices.Clear()

        self.entityChoices.AppendItems([p.name for p in self.choices])
        if selected:
            idx = self.choices.index(selected)
            self.entityChoices.SetSelection(idx)
        else:
            self.entityChoices.SetSelection(0)

    def getActiveEntity(self):
        if len(self.choices) == 0:
            return None

        return self.choices[self.entityChoices.GetSelection()]

    def setActiveEntity(self, entity):
        self.entityChoices.SetSelection(self.choices.index(entity))

    def checkEntitiesExist(self):
        if len(self.choices) == 0:
            self.Parent.Hide()
            if self.OnNew(None) is False:
                return False
            self.Parent.Show()

        return True
