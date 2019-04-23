# noinspection PyPackageRequirements
import wx

import gui.fitCommands as cmd
import gui.mainFrame
from eos.const import FittingHardpoint
from eos.saveddata.module import Module
from gui.bitmap_loader import BitmapLoader
from gui.contextMenu import ContextMenuCombined
from gui.fitCommands.helpers import getSimilarModPositions
from service.fit import Fit
from service.market import Market
from service.settings import ContextMenuSettings


class ChangeModuleAmmo(ContextMenuCombined):

    DAMAGE_TYPES = ("em", "explosive", "kinetic", "thermal")
    MISSILE_ORDER = ("em", "thermal", "kinetic", "explosive", "mixed")

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()
        self.settings = ContextMenuSettings.getInstance()
        # Format: {type ID: set(loadable, charges)}
        self.loadableCharges = {}

    def display(self, srcContext, mainItem, selection):
        if srcContext not in ("fittingModule", "projectedModule"):
            return False

        if self.mainFrame.getActiveFit() is None:
            return False

        self.mainCharges = self.getChargesForMod(mainItem)
        if not self.mainCharges:
            return False

        self.module = mainItem
        self.selection = selection
        self.srcContext = srcContext
        return True

    def getText(self, itmContext, mainItem, selection):
        return "Charge"

    def getChargesForMod(self, mod):
        sMkt = Market.getInstance()
        if mod is None or mod.isEmpty:
            return set()
        typeID = mod.item.ID
        if typeID in self.loadableCharges:
            return self.loadableCharges[typeID]
        chargeSet = self.loadableCharges.setdefault(typeID, set())
        # Do not try to grab it for modes which can also be passed as part of selection
        if isinstance(mod, Module):
            for charge in mod.getValidCharges():
                if sMkt.getPublicityByItem(charge):
                    chargeSet.add(charge)
        return chargeSet

    def turretSorter(self, charge):
        damage = 0
        range_ = (self.module.item.getAttribute("maxRange")) * \
                 (charge.getAttribute("weaponRangeMultiplier") or 1)
        falloff = (self.module.item.getAttribute("falloff") or 0) * \
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
        id_ = ContextMenuCombined.nextID()
        name = charge.name if charge is not None else "Empty"
        self.chargeIds[id_] = charge
        item = wx.MenuItem(menu, id_, name)
        menu.Bind(wx.EVT_MENU, self.handleAmmoSwitch, item)
        item.charge = charge
        if charge is not None and charge.iconID is not None:
            bitmap = BitmapLoader.getBitmap(charge.iconID, "icons")
            if bitmap is not None:
                item.SetBitmap(bitmap)

        return item

    @staticmethod
    def addSeperator(m, text):
        id_ = ContextMenuCombined.nextID()
        m.Append(id_, '─ %s ─' % text)
        m.Enable(id_, False)

    def getSubMenu(self, context, mainItem, selection, rootMenu, i, pitem):
        msw = True if "wxMSW" in wx.PlatformInfo else False
        m = wx.Menu()
        self.chargeIds = {}
        hardpoint = self.module.hardpoint
        moduleName = self.module.item.name
        # Make sure we do not consider mining turrets as combat turrets
        if hardpoint == FittingHardpoint.TURRET and self.module.getModifiedItemAttr("miningAmount", None) is None:
            self.addSeperator(m, "Long Range")
            items = []
            range_ = None
            nameBase = None
            sub = None
            chargesSorted = sorted(self.mainCharges, key=self.turretSorter)
            for charge in chargesSorted:
                if "civilian" in charge.name.lower():
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
        elif hardpoint == FittingHardpoint.MISSILE and moduleName != 'Festival Launcher':
            type_ = None
            sub = None
            defender = None
            chargesSorted = sorted(self.mainCharges, key=self.missileSorter)
            for charge in chargesSorted:
                currType = self.damageInfo(charge)[0]

                if currType != type_ or type_ is None:
                    if sub is not None:
                        self.addSeperator(sub, "More Damage")

                    type_ = currType
                    item = wx.MenuItem(m, wx.ID_ANY, type_.capitalize())
                    bitmap = BitmapLoader.getBitmap("%s_small" % type_, "gui")
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
            chargesSorted = sorted(self.mainCharges, key=self.nameSorter)
            for charge in chargesSorted:
                m.Append(self.addCharge(rootMenu if msw else m, charge))

        m.Append(self.addCharge(rootMenu if msw else m, None))
        return m

    def handleAmmoSwitch(self, event):
        charge = self.chargeIds.get(event.Id, False)
        if charge is False:
            event.Skip()
            return

        fitID = self.mainFrame.getActiveFit()
        sFit = Fit.getInstance()
        fit = sFit.getFit(fitID)
        mstate = wx.GetMouseState()
        # Switch in selection or all modules, depending on modifier key state and settings
        switchAll = sFit.serviceFittingOptions['ammoChangeAll'] is not (mstate.cmdDown or mstate.altDown)
        if switchAll:
            if self.srcContext == 'fittingModule':
                command = cmd.GuiChangeLocalModuleChargesCommand
                modContainer = fit.modules
            elif self.srcContext == 'projectedModule':
                command = cmd.GuiChangeProjectedModuleChargesCommand
                modContainer = fit.projectedModules
            else:
                return
            positions = getSimilarModPositions(modContainer, self.module)
            self.mainFrame.command.Submit(command(
                fitID=fitID,
                positions=positions,
                chargeItemID=charge.ID if charge is not None else None))
        else:
            if self.srcContext == 'fittingModule':
                command = cmd.GuiChangeLocalModuleChargesCommand
                modContainer = fit.modules
            elif self.srcContext == 'projectedModule':
                command = cmd.GuiChangeProjectedModuleChargesCommand
                modContainer = fit.projectedModules
            else:
                return
            positions = []
            for position, mod in enumerate(modContainer):
                if mod in self.selection:
                    modCharges = self.getChargesForMod(mod)
                    if modCharges.issubset(self.mainCharges):
                        positions.append(position)
            self.mainFrame.command.Submit(command(
                fitID=fitID,
                positions=positions,
                chargeItemID=charge.ID if charge is not None else None))


ChangeModuleAmmo.register()
