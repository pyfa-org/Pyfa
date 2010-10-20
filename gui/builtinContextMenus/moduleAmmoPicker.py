from gui.contextMenu import ContextMenu
import gui.mainFrame
import service
import gui.fittingView
import wx
from gui import bitmapLoader
from eos.types import Hardpoint

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

        self.charges = list(validCharges)
        self.hardpoint = mod.hardpoint
        return len(self.charges) > 0

    def getText(self, context, selection):
        return "Ammo"

    def activate(self, context, selection, i):
        pass

    def turretSorter(self, charge):
        range = charge.getAttribute("weaponRangeMultiplier")
        damage = 0
        for type in ("em", "explosive", "kinetic", "thermal"):
            damage += charge.getAttribute("%sDamage" % type)

        return (-range, damage)

    MISSILE_ORDER = ["em", "explosive", "kinetic", "thermal"]
    def missileSorter(self, charge):
        for i, type in enumerate(self.MISSILE_ORDER):
            damage = charge.getAttribute("%sDamage" % type)
            if damage > 0:
                return (type, damage)

    def nameSorter(self, charge):
        n = charge.name
        return (len(n), n)

    def addCharge(self, menu, charge):
        id = wx.NewId()
        name = charge.name if charge is not None else "Empty"
        self.chargeIds[id] = charge
        item = wx.MenuItem(menu, id, name)
        item.charge = charge
        if charge is not None and charge.icon is not None:
            bitmap = bitmapLoader.getBitmap(charge.icon.iconFile, "pack")
            if bitmap is not None:
                item.SetBitmap(bitmap)

        return item

    def getSubMenu(self, context, selection, menu, i):
        menu.Bind(wx.EVT_MENU, self.handleAmmoSwitch)
        m = wx.Menu()
        self.chargeIds = {}
        previousRangeMod = None
        if self.hardpoint == Hardpoint.TURRET:
            idRange = wx.NewId()
            m.Append(idRange, "--- Range ---")
            m.Enable(idRange, False)
            items = []
            self.charges.sort(key=self.turretSorter)
            for charge in self.charges:
                currRangeMod = charge.getAttribute("weaponRangeMultiplier")
                if previousRangeMod is None or previousRangeMod != currRangeMod:
                    sub = None
                    base = charge
                    previousRangeMod = currRangeMod
                    item = self.addCharge(m, charge)
                    items.append(item)
                else:
                    if sub is None:
                        sub = wx.Menu()
                        item.SetSubMenu(sub)
                        sub.AppendItem(self.addCharge(sub, base))
                    sub.AppendItem(self.addCharge(sub, charge))
            for item in items:
                m.AppendItem(item)

            idDamage = wx.NewId()
            m.Append(idDamage, "--- Damage ---")
            m.Enable(idDamage, False)
        elif self.hardpoint == Hardpoint.MISSILE:
            self.charges.sort(key=self.missileSorter)
            type = None
            sub = None
            for charge in self.charges:
                currType = None
                for t in ("em", "explosive", "kinetic", "thermal"):
                    if charge.getAttribute("%sDamage" % t) > 0:
                        currType = t
                        break

                if currType != type or type is None:
                    if sub is not None:
                        id = wx.NewId()
                        sub.Append(id, "--- More Damage ---")
                        sub.Enable(id, False)
                    type = currType
                    item = wx.MenuItem(m, wx.ID_ANY, type.capitalize())
                    bitmap = bitmapLoader.getBitmap("%s_small" % type, "icons")
                    if bitmap is not None:
                        item.SetBitmap(bitmap)

                    sub = wx.Menu()
                    id = wx.NewId()
                    sub.Append(id, "--- Less Damage ---")
                    sub.Enable(id, False)
                    item.SetSubMenu(sub)
                    m.AppendItem(item)

                if charge.name != "Defender I":
                    sub.AppendItem(self.addCharge(sub, charge))
                else:
                    defender = charge

            if defender is not None:
                m.AppendItem(self.addCharge(sub, defender))
        else:
            self.charges.sort(key=self.nameSorter)
            for charge in self.charges:
                m.AppendItem(self.addCharge(m, charge))

        m.AppendItem(self.addCharge(m, None))
        return m

    def handleAmmoSwitch(self, event):
        charge = self.chargeIds.get(event.Id, False)
        if charge is False:
            event.Skip()
            return

        sFit = service.Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()
        modules = map(lambda mod: mod.position, self.mainFrame.getFittingView().getSelectedMods())
        sFit.setAmmo(fitID, charge.ID if charge is not None else None, modules)
        wx.PostEvent(self.mainFrame, gui.fittingView.FitChanged(fitID=fitID))

ModuleAmmoPicker.register()
