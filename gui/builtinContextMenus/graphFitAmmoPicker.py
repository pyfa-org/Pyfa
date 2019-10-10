# noinspection PyPackageRequirements
import wx

import gui.mainFrame
from gui.contextMenu import ContextMenuSingle
from service.market import Market


class GraphFitAmmoPicker(ContextMenuSingle):

    def __init__(self):
        self.mainFrame = gui.mainFrame.MainFrame.getInstance()

    def display(self, callingWindow, srcContext, mainItem):
        if srcContext != 'graphFitList':
            return False
        if mainItem is None or not mainItem.isFit:
            return False
        if callingWindow.graphFrame.getView().internalName != 'dmgStatsGraph':
            return False
        return True

    def getText(self, callingWindow, itmContext, mainItem):
        return 'Plot with Different Ammo...'

    def activate(self, callingWindow, fullContext, mainItem, i):
        with AmmoPicker(self.mainFrame, mainItem.item) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                pass
            else:
                pass


GraphFitAmmoPicker.register()


class AmmoPicker(wx.Dialog):

    def __init__(self, parent, fit):
        super().__init__(parent, title='Choose Different Ammo', style=wx.DEFAULT_DIALOG_STYLE)

        mods = self.getMods(fit)
        drones = self.getDrones(fit)
        fighters = self.getFighters(fit)

        self.SetMinSize((346, 156))

    def getMods(self, fit):
        sMkt = Market.getInstance()
        loadableCharges = {}
        # Modules, Format: {frozenset(ammo): [module list]}
        mods = {}
        if fit is not None:
            for mod in fit.modules:
                if not mod.canDealDamage():
                    continue
                typeID = mod.item.ID
                if typeID in loadableCharges:
                    charges = loadableCharges[typeID]
                else:
                    charges = loadableCharges.setdefault(typeID, set())
                    for charge in mod.getValidCharges():
                        if sMkt.getPublicityByItem(charge):
                            charges.add(charge)
                # We're not interested in modules which contain no charges
                if charges:
                    mods.setdefault(frozenset(charges), []).append(mod)
        return mods

    def getDrones(self, fit):
        drones = set()
        if fit is not None:
            for drone in fit.drones:
                if drone.item is None:
                    continue
                # Drones are our "ammo", so we want to pick even those which are inactive
                if drone.canDealDamage(ignoreState=True):
                    drones.add(drone)
                    continue
                if {'remoteWebifierEntity', 'remoteTargetPaintEntity'}.intersection(drone.item.effects):
                    drones.add(drone)
                    continue
        return drones

    def getFighters(self, fit):
        fighters = set()
        if fit is not None:
            for fighter in fit.fighters:
                if fighter.item is None:
                    continue
                # Fighters are our "ammo" as well
                if fighter.canDealDamage(ignoreState=True):
                    fighters.add(fighter)
                    continue
                for ability in fighter.abilities:
                    if not ability.active:
                        continue
                    if ability.effect.name == 'fighterAbilityStasisWebifier':
                        fighters.add(fighter)
                        break
        return fighters
