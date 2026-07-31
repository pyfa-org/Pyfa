# ===============================================================================
# Copyright (C) 2010 Diego Duclos
#
# This file is part of pyfa.
#
# pyfa is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfa.  If not, see <http://www.gnu.org/licenses/>.
# ===============================================================================

import copy
import datetime
from time import time
from weakref import WeakSet

import wx
from logbook import Logger

import eos.db
from eos.const import FittingModuleState, ImplantLocation
from eos.saveddata.character import Character as saveddata_Character
from eos.saveddata.citadel import Citadel as es_Citadel
from eos.saveddata.damagePattern import DamagePattern as es_DamagePattern
from eos.saveddata.fit import Fit as FitType
from eos.saveddata.ship import Ship as es_Ship
from service.character import Character
from service.damagePattern import DamagePattern
from service.settings import SettingsProvider


pyfalog = Logger(__name__)


class DeferRecalc:
    def __init__(self, fitID):
        self.fitID = fitID
        self.sFit = Fit.getInstance()

    def __enter__(self):
        self._recalc = self.sFit.recalc
        self.sFit.recalc = lambda x: pyfalog.debug('Deferred Recalc')

    def __exit__(self, *args):
        self.sFit.recalc = self._recalc
        self.sFit.recalc(self.fitID)


class Fit:
    instance = None
    processors = {}

    @classmethod
    def getInstance(cls):
        if cls.instance is None:
            cls.instance = Fit()

        return cls.instance

    def __init__(self):
        pyfalog.debug("Initialize Fit class")
        self.pattern = DamagePattern.getInstance().getDamagePattern("Uniform")
        self.targetProfile = None
        self.character = saveddata_Character.getAll5()
        self.booster = False
        self._loadedFits = WeakSet()

        serviceFittingDefaultOptions = {
            "useGlobalCharacter": False,
            "useCharacterImplantsByDefault": True,
            "useGlobalDamagePattern": False,
            "defaultCharacter": self.character.ID,
            "useGlobalForceReload": False,
            "colorFitBySlot": False,
            "rackSlots": True,
            "rackLabels": True,
            "compactSkills": True,
            "showTooltip": True,
            "showMarketShortcuts": False,
            "enableGaugeAnimation": True,
            "openFitInNew": False,
            "priceSystem": "Jita",
            "priceSource": "fuzzwork market",
            "showShipBrowserTooltip": True,
            "marketSearchDelay": 250,
            "ammoChangeAll": False,
            "additionsLabels": 1,
            "expandedMutantNames": False,
        }

        self.serviceFittingOptions = SettingsProvider.getInstance().getSettings(
            "pyfaServiceFittingOptions", serviceFittingDefaultOptions)

    @staticmethod
    def getAllFits():
        pyfalog.debug("Fetching all fits")
        fits = eos.db.getFitList()
        return fits

    @staticmethod
    def getAllFitsLite():
        fits = eos.db.getFitListLite()
        shipMap = {f.shipID: None for f in fits}
        for shipID in shipMap:
            ship = eos.db.getItem(shipID)
            if ship is not None:
                shipMap[shipID] = (ship.name, ship.getShortName())
        fitsToPurge = set()
        for fit in fits:
            try:
                fit.shipName, fit.shipNameShort = shipMap[fit.shipID]
            except (KeyError, TypeError):
                fitsToPurge.add(fit)
        for fit in fitsToPurge:
            fits.remove(fit)
        return fits

    @staticmethod
    def getFitsWithShip(shipID):
        """ Lists fits of shipID, used with shipBrowser """
        pyfalog.debug("Fetching all fits for ship ID: {0}", shipID)
        fits = eos.db.getFitsWithShip(shipID)
        names = []
        for fit in fits:
            names.append((fit.ID,
                          fit.name,
                          fit.booster,
                          fit.modified or fit.created or datetime.datetime.fromtimestamp(fit.timestamp),
                          fit.notes,
                          fit.ship.item.graphicID))

        return names

    @staticmethod
    def getRecentFits():
        """ Fetches recently modified fits, used with shipBrowser """
        pyfalog.debug("Fetching recent fits")
        fits = eos.db.getRecentFits()
        returnInfo = []

        for fit in fits:
            item = eos.db.getItem(fit[1])
            returnInfo.append((fit[0], fit[2], fit[3] or fit[4] or datetime.datetime.fromtimestamp(fit[5]), item, fit[6]))
            #                  ID      name    timestamps                                                   item  notes

        return returnInfo

    @staticmethod
    def getFitsWithModules(typeIDs):
        """ Lists fits flagged as booster """
        pyfalog.debug('Getting fits with modules')
        fits = eos.db.getFitsWithModules(typeIDs)
        return fits

    @staticmethod
    def countAllFits():
        pyfalog.debug("Getting count of all fits.")
        return eos.db.countAllFits()

    @staticmethod
    def countAllFitsGroupedByShip():
        count = eos.db.countFitGroupedByShip()
        return count

    @staticmethod
    def countFitsWithShip(stuff):
        pyfalog.debug("Getting count of all fits for: {0}", stuff)
        count = eos.db.countFitsWithShip(stuff)
        return count

    @staticmethod
    def getModule(fitID, pos):
        fit = eos.db.getFit(fitID)
        return fit.modules[pos]

    def newFit(self, shipID, name=None):
        pyfalog.debug("Creating new fit for ID: {0}", shipID)
        try:
            ship = es_Ship(eos.db.getItem(shipID))
        except ValueError:
            ship = es_Citadel(eos.db.getItem(shipID))
        fit = FitType(ship)
        fit.name = name if name is not None else "New %s" % fit.ship.item.name
        fit.damagePattern = self.pattern
        fit.targetProfile = self.targetProfile
        fit.character = self.character
        fit.booster = self.booster
        useCharImplants = self.serviceFittingOptions["useCharacterImplantsByDefault"]
        fit.implantLocation = ImplantLocation.CHARACTER if useCharImplants else ImplantLocation.FIT
        eos.db.save(fit)
        self.recalc(fit)
        self.fill(fit)
        return fit.ID

    @staticmethod
    def deleteFit(fitID):
        fit = eos.db.getFit(fitID)
        pyfalog.debug("Fit::deleteFit - Deleting fit: {}", fit)

        # refresh any fits this fit is projected onto. Otherwise, if we have
        # already loaded those fits, they will not reflect the changes

        # A note on refreshFits: we collect the target fits in a set because
        # if a target fit has the same fit for both projected and command,
        # it will be refreshed first during the projected loop and throw an
        # error during the command loop
        refreshFits = set()
        for projection in list(fit.projectedOnto.values()):
            if projection.victim_fit and projection.victim_fit != fit and projection.victim_fit in eos.db.saveddata_session:  # GH issue #359
                refreshFits.add(projection.victim_fit)

        for booster in list(fit.boostedOnto.values()):
            if booster.boosted_fit and booster.boosted_fit != fit and booster.boosted_fit in eos.db.saveddata_session:  # GH issue #359
                refreshFits.add(booster.boosted_fit)

        eos.db.remove(fit)

        if fitID in Fit.processors:
            del Fit.processors[fitID]

        pyfalog.debug("    Need to refresh {} fits: {}", len(refreshFits), refreshFits)
        for fit in refreshFits:
            eos.db.saveddata_session.refresh(fit)

        eos.db.saveddata_session.commit()

    @classmethod
    def getCommandProcessor(cls, fitID):
        if fitID not in cls.processors:
            cls.processors[fitID] = wx.CommandProcessor(maxCommands=100)
        return cls.processors[fitID]

    @staticmethod
    def copyFit(fitID):
        pyfalog.debug("Creating copy of fit ID: {0}", fitID)
        fit = eos.db.getFit(fitID)
        newFit = copy.deepcopy(fit)
        eos.db.save(newFit)
        return newFit.ID

    @staticmethod
    def clearFit(fitID):
        pyfalog.debug("Clearing fit for fit ID: {0}", fitID)
        if fitID is None:
            return None

        fit = eos.db.getFit(fitID)
        fit.clear()
        return fit

    @staticmethod
    def editNotes(fitID, notes):
        fit = eos.db.getFit(fitID)
        if fit:
            fit.notes = notes
            eos.db.commit()

    def toggleFactorReload(self, value=None):
        self.serviceFittingOptions['useGlobalForceReload'] = value if value is not None else not self.serviceFittingOptions['useGlobalForceReload']
        fitIDs = set()
        for fit in set(self._loadedFits):
            if fit is None:
                continue
            if fit.calculated:
                fit.factorReload = self.serviceFittingOptions['useGlobalForceReload']
                fit.clearFactorReloadDependentData()
                fitIDs.add(fit.ID)
        return fitIDs

    def processOverrideToggle(self):
        fitIDs = set()
        for fit in set(self._loadedFits):
            if fit is None:
                continue
            if fit.calculated:
                self.recalc(fit)
                fitIDs.add(fit.ID)
        return fitIDs

    def processTargetProfileChange(self):
        fitIDs = set()
        for fit in set(self._loadedFits):
            if fit is None:
                continue
            if not fit.targetProfile:
                continue
            if fit.calculated:
                self.recalc(fit)
                fitIDs.add(fit.ID)
        return fitIDs

    def switchFit(self, fitID):
        pyfalog.debug("Switching fit to fit ID: {0}", fitID)
        if fitID is None:
            return None

        fit = eos.db.getFit(fitID)

        if self.serviceFittingOptions["useGlobalCharacter"]:
            if fit.character != self.character:
                fit.calculated = False
                fit.character = self.character

        if self.serviceFittingOptions["useGlobalDamagePattern"]:
            if fit.damagePattern != self.pattern:
                fit.calculated = False
                fit.damagePattern = self.pattern

        eos.db.commit()

        if not fit.calculated:
            self.recalc(fit)
            self.fill(fit)

    def getFit(self, fitID, projected=False, basic=False):
        # type: (int, bool, bool) -> Fit
        """
        Gets fit from database

        Projected is a recursion flag that is set to reduce recursions into projected fits
        Basic is a flag to simply return the fit without any other processing
        """
        # pyfalog.debug("Getting fit for fit ID: {0}", fitID)
        if fitID is None:
            return None
        fit = eos.db.getFit(fitID)

        if fit is None:
            return None

        self._loadedFits.add(fit)

        if basic:
            return fit

        inited = getattr(fit, "inited", None)

        if inited is None or inited is False:
            if not projected:
                for fitP in fit.projectedFits:
                    self.getFit(fitP.ID, projected=True)
                self.recalc(fit)
                self.fill(fit)

                # this will loop through modules and set their restriction flag (set in m.fit())
                if fit.ignoreRestrictions:
                    for mod in fit.modules:
                        if not mod.isEmpty:
                            mod.fits(fit)

                # Check that the states of all modules are valid
                self.checkStates(fit, None)

            eos.db.commit()
            fit.inited = True
        return fit

    @staticmethod
    def searchFits(name):
        pyfalog.debug("Searching for fit: {0}", name)
        results = eos.db.searchFits(name)
        fits = []

        for fit in sorted(results, key=lambda f: (f.ship.item.group.name, f.ship.item.name, f.name)):
            fits.append((
                fit.ID,
                fit.name,
                fit.ship.item.ID,
                fit.ship.item.name,
                fit.booster,
                fit.modifiedCoalesce,
                fit.notes))
        return fits

    def changeMutatedValuePrelim(self, mutator, value):
        pyfalog.debug("Changing mutated value for {} / {}: {} => {}".format(mutator.item, mutator.item.mutaplasmid, mutator.value, value))
        if mutator.value != value:
            mutator.value = value
            eos.db.flush()
        return mutator.value

    def changeChar(self, fitID, charID):
        pyfalog.debug("Changing character ({0}) for fit ID: {1}", charID, fitID)
        if fitID is None or charID is None:
            if charID is not None:
                self.character = Character.getInstance().all5()

            return

        fit = eos.db.getFit(fitID)
        fit.character = self.character = eos.db.getCharacter(charID)
        self.recalc(fit)
        self.fill(fit)

    @staticmethod
    def getTargetProfile(fitID):
        pyfalog.debug("Get target profile for fit ID: {0}", fitID)
        if fitID is None:
            return

        fit = eos.db.getFit(fitID)
        return fit.targetProfile

    def setTargetProfile(self, fitID, pattern):
        pyfalog.debug("Set target resist for fit ID: {0}", fitID)
        if fitID is None:
            return

        fit = eos.db.getFit(fitID)
        fit.targetProfile = pattern
        eos.db.commit()

        self.recalc(fit)

    @staticmethod
    def getDamagePattern(fitID):
        pyfalog.debug("Get damage pattern for fit ID: {0}", fitID)
        if fitID is None:
            return

        fit = eos.db.getFit(fitID)
        return fit.damagePattern

    def setDamagePattern(self, fitID, pattern):
        pyfalog.debug("Set damage pattern for fit ID: {0}", fitID)
        if fitID is None:
            return

        fit = eos.db.getFit(fitID)
        fit.damagePattern = self.pattern = pattern
        eos.db.commit()

        self.recalc(fit)

    def setAsPattern(self, fitID, ammo):
        pyfalog.debug("Set as pattern for fit ID: {0}", fitID)
        if fitID is None:
            return

        sDP = DamagePattern.getInstance()
        dp = sDP.getDamagePattern("Selected Ammo")
        if dp is None:
            dp = es_DamagePattern()
            dp.rawName = "Selected Ammo"

        fit = eos.db.getFit(fitID)
        for attr in ("em", "thermal", "kinetic", "explosive"):
            setattr(dp, "%sAmount" % attr, ammo.getAttribute("%sDamage" % attr) or 0)

        fit.damagePattern = dp
        self.recalc(fit)

    def setRahPattern(self, fitID, module, pattern):
        pyfalog.debug("Set as pattern for fit ID: {0}", fitID)
        if fitID is None:
            return
        module.rahPatternOverride = pattern
        fit = eos.db.getFit(fitID)
        self.recalc(fit)

    def checkStates(self, fit, base):
        pyfalog.debug("Check states for fit ID: {0}", fit)
        changedMods = {}
        changedProjMods = {}
        changedProjDrones = {}
        for pos, mod in enumerate(fit.modules):
            if mod is not base:
                # fix for #529, where a module may be in incorrect state after CCP changes mechanics of module
                canHaveState = mod.canHaveState(mod.state)
                if canHaveState is not True:
                    changedMods[pos] = mod.state
                    mod.state = canHaveState
                elif not mod.isValidState(mod.state):
                    changedMods[pos] = mod.state
                    mod.state = FittingModuleState.ONLINE

        for pos, mod in enumerate(fit.projectedModules):
            # fix for #529, where a module may be in incorrect state after CCP changes mechanics of module
            canHaveState = mod.canHaveState(mod.state, fit)
            if canHaveState is not True:
                changedProjMods[pos] = mod.state
                mod.state = canHaveState
            elif not mod.isValidState(mod.state):
                changedProjMods[pos] = mod.state
                mod.state = FittingModuleState.OFFLINE

        for pos, drone in enumerate(fit.projectedDrones):
            if drone.amountActive > 0 and not drone.canBeApplied(fit):
                changedProjDrones[pos] = drone.amountActive
                drone.amountActive = 0

        return changedMods, changedProjMods, changedProjDrones

    @classmethod
    def fitObjectIter(cls, fit, forceFitImplants=False):
        yield fit.ship

        for mod in fit.modules:
            if not mod.isEmpty:
                yield mod
        implants = fit.implants if forceFitImplants else fit.appliedImplants
        for container in (fit.drones, fit.fighters, implants, fit.boosters, fit.cargo):
            for obj in container:
                yield obj

    @classmethod
    def fitItemIter(cls, fit, forceFitImplants=False):
        for fitobj in cls.fitObjectIter(fit, forceFitImplants):
            yield fitobj.item
            charge = getattr(fitobj, 'charge', None)
            if charge:
                yield charge

    def refreshFit(self, fitID):
        pyfalog.debug("Refresh fit for fit ID: {0}", fitID)
        if fitID is None:
            return None

        fit = eos.db.getFit(fitID)
        eos.db.commit()
        self.recalc(fit)
        self.fill(fit)

    def recalc(self, fit):
        if isinstance(fit, int):
            fit = self.getFit(fit)
        start_time = time()
        pyfalog.info("=" * 10 + "recalc: {0}" + "=" * 10, fit.name)

        fit.factorReload = self.serviceFittingOptions["useGlobalForceReload"]
        fit.clear()
        fit.calculateModifiedAttributes()
        pyfalog.info("=" * 10 + "recalc time: " + str(time() - start_time) + "=" * 10)

    def fill(self, fit):
        if isinstance(fit, int):
            fit = self.getFit(fit)
        return fit.fill()
