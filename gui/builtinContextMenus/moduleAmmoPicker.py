# -*- coding: utf-8 -*-
from gui.contextMenu import ContextMenu
import gui.mainFrame
import service
import wx
from gui import bitmapLoader
from eos.types import Hardpoint
import gui.globalEvents as GE

class ModuleAmmoPicker(ContextMenu):
    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, srcContext, selection):
        if self.mainFrame.getActiveFit() is None or srcContext not in ("fittingModule", "projectedModule"):
            return False

        modules = selection if srcContext == "fittingModule" else (selection[0],)

        validCharges = None
        checkedTypes = set()
        for mod in modules:
            if mod.item.ID in checkedTypes:
                continue
            checkedTypes.add(mod.item.ID)
            currCharges = mod.getValidCharges()
            if len(currCharges) > 0:
                if validCharges is not None and validCharges != currCharges:
                    return False

                validCharges = currCharges
                self.module = mod

        if validCharges is None:
            return False

        self.modules = modules
        self.charges = list(filter(lambda charge: service.Market.getInstance().getPublicityByItem(charge), validCharges))
        return len(self.charges) > 0

    def getText(self, itmContext, selection):
        return "Charge"

    def activate(self, fullContext, selection, i):
        pass

    DAMAGE_TYPES = ("em", "explosive", "kinetic", "thermal")
    def turretSorter(self, charge):
        damage = 0
        range = (self.module.getModifiedItemAttr("maxRange") or 0) * (charge.getAttribute("weaponRangeMultiplier") or 1)
        falloff = (self.module.getModifiedItemAttr("falloff") or 0) * (charge.getAttribute("fallofMultiplier") or 1)
        for type in self.DAMAGE_TYPES:
            d = charge.getAttribute("%sDamage" % type)
            if d > 0:
                damage += d

        # Take optimal and half falloff as range factor
        rangeFactor = range + falloff / 2

        return (- rangeFactor, charge.name.rsplit()[-2:], damage, charge.name)

    MISSILE_ORDER = ("em", "thermal", "kinetic", "explosive", "mixed")
    def missileSorter(self, charge):
        # Get charge damage type and total damage
        chargeDamageType, totalDamage = self.damageInfo(charge)
        # Find its position in sort list
        position = self.MISSILE_ORDER.index(chargeDamageType)
        return (position, totalDamage, charge.name)

    def damageInfo(self, charge):
        # Set up data storage for missile damage stuff
        damageMap = {}
        totalDamage = 0
        # Fill them with the data about charge
        for damageType in self.DAMAGE_TYPES:
            currentDamage = charge.getAttribute("{0}Damage".format(damageType)) or 0
            damageMap[damageType] = currentDamage
            totalDamage += currentDamage
        # Detect type of ammo
        chargeDamageType = None
        for damageType in damageMap:
            # If all damage belongs to certain type purely, set appropriate
            # ammoType
            if damageMap[damageType] == totalDamage:
                chargeDamageType = damageType
                break
        # Else consider ammo as mixed damage
        if chargeDamageType is None:
            chargeDamageType = "mixed"

        return chargeDamageType, totalDamage


    def numericConverter(self, string):
        return int(string) if string.isdigit() else string

    def nameSorter(self, charge):
        parts = charge.name.split(" ")
        return map(self.numericConverter, parts)

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

    def addSeperator(self, m, text):
        id = wx.NewId()
        m.Append(id, u'─ %s ─' % text)
        m.Enable(id, False)

    def getSubMenu(self, context, selection, menu, i, id):
        self.context = context
        menu.Bind(wx.EVT_MENU, self.handleAmmoSwitch)
        m = wx.Menu()
        m.Bind(wx.EVT_MENU, self.handleAmmoSwitch)
        self.chargeIds = {}
        hardpoint = self.module.hardpoint
        moduleName = self.module.item.name
        # Make sure we do not consider mining turrets as combat turrets
        if hardpoint == Hardpoint.TURRET and self.module.getModifiedItemAttr("miningAmount") is None:
            self.addSeperator(m, "Long Range")
            items = []
            range = None
            nameBase = None
            sub = None
            self.charges.sort(key=self.turretSorter)
            for charge in self.charges:
                # fix issue 71 - will probably have to change if CCP adds more Orbital ammo
                if "Orbital" in charge.name:
                    # uncomment if we ever want to include Oribital ammo in ammo picker - see issue #71
                    # This allows us to hide the ammo, but it's still loadable from the market
                    #item = self.addCharge(m, charge)
                    #items.append(item)
                    continue
                currBase = charge.name.rsplit()[-2:]
                currRange = charge.getAttribute("weaponRangeMultiplier")
                if nameBase is None or range != currRange or nameBase != currBase:
                    if sub is not None:
                        self.addSeperator(sub, "More Damage")

                    sub = None
                    base = charge
                    nameBase = currBase
                    range = currRange
                    item = self.addCharge(m, charge)
                    items.append(item)
                else:
                    if sub is None:
                        sub = wx.Menu()
                        sub.Bind(wx.EVT_MENU, self.handleAmmoSwitch)
                        self.addSeperator(sub, "Less Damage")
                        item.SetSubMenu(sub)
                        sub.AppendItem(self.addCharge(sub, base))

                    sub.AppendItem(self.addCharge(sub, charge))

            if sub is not None:
                self.addSeperator(sub, "More Damage")

            for item in items:
                m.AppendItem(item)

            self.addSeperator(m, "Short Range")
        elif hardpoint == Hardpoint.MISSILE and moduleName != 'Festival Launcher':
            self.charges.sort(key=self.missileSorter)
            type = None
            sub = None
            defender = None
            for charge in self.charges:
                currType = self.damageInfo(charge)[0]

                if currType != type or type is None:
                    if sub is not None:
                        self.addSeperator(sub, "More Damage")

                    type = currType
                    item = wx.MenuItem(m, wx.ID_ANY, type.capitalize())
                    bitmap = bitmapLoader.getBitmap("%s_small" % type, "icons")
                    if bitmap is not None:
                        item.SetBitmap(bitmap)

                    sub = wx.Menu()
                    sub.Bind(wx.EVT_MENU, self.handleAmmoSwitch)
                    self.addSeperator(sub, "Less Damage")
                    item.SetSubMenu(sub)
                    m.AppendItem(item)

                if charge.name not in ("Light Defender Missile I", "Heavy Defender Missile I"):
                    sub.AppendItem(self.addCharge(sub, charge))
                else:
                    defender = charge

            if defender is not None:
                m.AppendItem(self.addCharge(sub, defender))
            if sub is not None:
                self.addSeperator(sub, "More Damage")
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

        sFit.setAmmo(fitID, charge.ID if charge is not None else None, self.modules)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))

ModuleAmmoPicker.register()
