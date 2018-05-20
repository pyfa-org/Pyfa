# coding: utf-8

# noinspection PyPackageRequirements
import wx

from service.fit import Fit
from service.market import Market
from eos.saveddata.module import Hardpoint
import gui.mainFrame
import gui.globalEvents as GE
from gui.contextMenu import ContextMenu
from gui.bitmap_loader import BitmapLoader
from service.settings import ContextMenuSettings


class ModuleAmmoPicker(ContextMenu):
    DAMAGE_TYPES = ("em", "explosive", "kinetic", "thermal")
    MISSILE_ORDER = ("em", "thermal", "kinetic", "explosive", "mixed")

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = ContextMenuSettings.getInstance()

    def display(self, srcContext, selection):
        if not self.settings.get('moduleAmmoPicker'):
            return False

        if self.mainFrame.getActiveFit() is None or srcContext not in ("fittingModule", "projectedModule"):
            return False

        modules = selection if srcContext == "fittingModule" else (selection[0],)

        validCharges = None
        checkedTypes = set()

        for mod in modules:
            # loop through modules and gather list of valid charges
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
        self.charges = list([charge for charge in validCharges if Market.getInstance().getPublicityByItem(charge)])
        return len(self.charges) > 0

    def getText(self, itmContext, selection):
        return "Charge"

    def turretSorter(self, charge):
        damage = 0
        range_ = (self.module.item.getAttribute("maxRange")) * \
                 (charge.getAttribute("weaponRangeMultiplier") or 1)
        falloff = (self.module.item.getAttribute("falloff")) * \
                  (charge.getAttribute("fallofMultiplier") or 1)
        for type_ in self.DAMAGE_TYPES:
            d = charge.getAttribute("%sDamage" % type_)
            if d > 0:
                damage += d

        # Take optimal and half falloff as range factor
        rangeFactor = range_ + falloff / 2

        return - rangeFactor, charge.name.rsplit()[-2:], damage, charge.name

    def missileSorter(self, charge):
        # Get charge damage type and total damage
        chargeDamageType, totalDamage = self.damageInfo(charge)
        # Find its position in sort list
        position = self.MISSILE_ORDER.index(chargeDamageType)
        return position, totalDamage, charge.name

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

    @staticmethod
    def numericConverter(string):
        return int(string) if string.isdigit() else string

    def nameSorter(self, charge):
        parts = charge.name.split(" ")
        return list(map(self.numericConverter, parts))

    def addCharge(self, menu, charge):
        id_ = ContextMenu.nextID()
        name = charge.name if charge is not None else "Empty"
        self.chargeIds[id_] = charge
        item = wx.MenuItem(menu, id_, name)
        menu.Bind(wx.EVT_MENU, self.handleAmmoSwitch, item)
        item.charge = charge
        if charge is not None and charge.icon is not None:
            bitmap = BitmapLoader.getBitmap(charge.icon.iconFile, "icons")
            if bitmap is not None:
                item.SetBitmap(bitmap)

        return item

    @staticmethod
    def addSeperator(m, text):
        id_ = ContextMenu.nextID()
        m.Append(id_, '─ %s ─' % text)
        m.Enable(id_, False)

    def getSubMenu(self, context, selection, rootMenu, i, pitem):
        msw = True if "wxMSW" in wx.PlatformInfo else False
        m = wx.Menu()
        self.chargeIds = {}
        hardpoint = self.module.hardpoint
        moduleName = self.module.item.name
        # Make sure we do not consider mining turrets as combat turrets
        if hardpoint == Hardpoint.TURRET and self.module.getModifiedItemAttr("miningAmount", None) is None:
            self.addSeperator(m, "Long Range")
            items = []
            range_ = None
            nameBase = None
            sub = None
            self.charges.sort(key=self.turretSorter)
            for charge in self.charges:
                # fix issue 71 - will probably have to change if CCP adds more Orbital ammo
                if "Orbital" in charge.name:
                    # uncomment if we ever want to include Oribital ammo in ammo picker - see issue #71
                    # This allows us to hide the ammo, but it's still loadable from the market
                    # item = self.addCharge(m, charge)
                    # items.append(item)
                    continue
                currBase = charge.name.rsplit()[-2:]
                currRange = charge.getAttribute("weaponRangeMultiplier")
                if nameBase is None or range_ != currRange or nameBase != currBase:
                    if sub is not None:
                        self.addSeperator(sub, "More Damage")

                    sub = None
                    base = charge
                    nameBase = currBase
                    range_ = currRange
                    item = self.addCharge(rootMenu if msw else m, charge)
                    items.append(item)
                else:
                    if sub is None and item and base:
                        sub = wx.Menu()
                        sub.Bind(wx.EVT_MENU, self.handleAmmoSwitch)
                        self.addSeperator(sub, "Less Damage")
                        item.SetSubMenu(sub)
                        sub.Append(self.addCharge(rootMenu if msw else sub, base))

                    sub.Append(self.addCharge(rootMenu if msw else sub, charge))

            if sub is not None:
                self.addSeperator(sub, "More Damage")

            for item in items:
                m.Append(item)

            self.addSeperator(m, "Short Range")
        elif hardpoint == Hardpoint.MISSILE and moduleName != 'Festival Launcher':
            self.charges.sort(key=self.missileSorter)
            type_ = None
            sub = None
            defender = None
            for charge in self.charges:
                currType = self.damageInfo(charge)[0]

                if currType != type_ or type_ is None:
                    if sub is not None:
                        self.addSeperator(sub, "More Damage")

                    type_ = currType
                    item = wx.MenuItem(m, wx.ID_ANY, type_.capitalize())
                    bitmap = BitmapLoader.getBitmap("%s_small" % type, "gui")
                    if bitmap is not None:
                        item.SetBitmap(bitmap)

                    sub = wx.Menu()
                    sub.Bind(wx.EVT_MENU, self.handleAmmoSwitch)
                    self.addSeperator(sub, "Less Damage")
                    item.SetSubMenu(sub)
                    m.Append(item)

                if charge.name not in ("Light Defender Missile I", "Heavy Defender Missile I"):
                    sub.Append(self.addCharge(rootMenu if msw else sub, charge))
                else:
                    defender = charge

            if defender is not None:
                m.Append(self.addCharge(rootMenu if msw else m, defender))
            if sub is not None:
                self.addSeperator(sub, "More Damage")
        else:
            self.charges.sort(key=self.nameSorter)
            for charge in self.charges:
                m.Append(self.addCharge(rootMenu if msw else m, charge))

        m.Append(self.addCharge(rootMenu if msw else m, None))
        return m

    def handleAmmoSwitch(self, event):
        charge = self.chargeIds.get(event.Id, False)
        if charge is False:
            event.Skip()
            return

        sFit = Fit.getInstance()
        fitID = self.mainFrame.getActiveFit()

        sFit.setAmmo(fitID, charge.ID if charge is not None else None, self.modules)
        wx.PostEvent(self.mainFrame, GE.FitChanged(fitID=fitID))


ModuleAmmoPicker.register()
