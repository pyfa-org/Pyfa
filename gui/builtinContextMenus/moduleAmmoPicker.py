from gui.contextMenu import ContextMenu
import gui.mainFrame
import service
import gui.fittingView
import wx
from gui import bitmapLoader

class ModuleAmmoPicker(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, context, selection):
        if self.mainFrame.getActiveFit() is None or context != "module":
            return False

        modules = self.mainFrame.getFittingView().getSelectedMods()
        validCharges = None
        for mod in modules:
            currCharges = mod.getValidCharges()
            if validCharges is not None and validCharges != currCharges:
                return False

            validCharges = currCharges

        self.charges = validCharges
        return True

    def getText(self, context, selection):
        return "Ammo"

    def activate(self, context, selection, i):
        pass

    def getSubMenu(self, context, selection, menu, i):
        menu.Bind(wx.EVT_MENU, self.handleAmmoSwitch)
        m = wx.Menu()
        self.chargeIds = {}
        for charge in self.charges:
            id = wx.NewId()
            self.chargeIds[id] = charge
            item = wx.MenuItem(m, id, charge.name)
            item.charge = charge
            if charge.icon is not None:
                bitmap = bitmapLoader.getBitmap(charge.icon.iconFile, "pack")
                if bitmap is not None:
                    item.SetBitmap(bitmap)
            m.AppendItem(item)

        return m

    def handleAmmoSwitch(self, event):
        charge = self.chargeIds.get(event.Id)
        if charge is None:
            event.Skip()
            return

        sFit = service.Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        modules = map(lambda mod: mod.position, self.mainFrame.getFittingView().getSelectedMods())
        sFit.setAmmo(fitID, charge.ID, modules)
        wx.PostEvent(self.mainFrame, gui.fittingView.FitChanged(fitID=fitID))

ModuleAmmoPicker.register()
