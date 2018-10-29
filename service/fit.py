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

import wx
from logbook import Logger

import eos.db
from eos.saveddata.character import Character as saveddata_Character
from eos.saveddata.citadel import Citadel as es_Citadel
from eos.saveddata.damagePattern import DamagePattern as es_DamagePattern
from eos.saveddata.drone import Drone as es_Drone
from eos.saveddata.fighter import Fighter as es_Fighter
from eos.saveddata.fit import Fit as FitType, ImplantLocation
from eos.saveddata.module import Module as es_Module, State
from eos.saveddata.ship import Ship as es_Ship
from service.character import Character
from service.damagePattern import DamagePattern
from service.fitDeprecated import FitDeprecated
from service.settings import SettingsProvider
from utils.deprecated import deprecated

pyfalog = Logger(__name__)


class DeferRecalc:
    def __init__(self, fitID):
        self.fitID = fitID
        self.sFit = Fit.getInstance()

    def __enter__(self):
        self._recalc = self.sFit.recalc
        self.sFit.recalc = lambda x: print('Deferred Recalc')

    def __exit__(self, *args):
        self.sFit.recalc = self._recalc
        self.sFit.recalc(self.fitID)


# inherits from FitDeprecated so that I can move all the dead shit, but not affect functionality
class Fit(FitDeprecated):
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
        self.targetResists = None
        self.character = saveddata_Character.getAll5()
        self.booster = False
        self.dirtyFitIDs = set()

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
            "exportCharges": True,
            "openFitInNew": False,
            "priceSystem": "Jita",
            "priceSource": "eve-marketdata.com",
            "showShipBrowserTooltip": True,
            "marketSearchDelay": 250
        }

        self.serviceFittingOptions = SettingsProvider.getInstance().getSettings(
            "pyfaServiceFittingOptions", serviceFittingDefaultOptions)

    @staticmethod
    def getAllFits():
        pyfalog.debug("Fetching all fits")
        fits = eos.db.getFitList()
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
        fits = eos.db.getFitsWithModules(typeIDs)
        return fits

    @staticmethod
    def countAllFits():
        pyfalog.debug("Getting count of all fits.")
        return eos.db.countAllFits()

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
        fit.targetResists = self.targetResists
        fit.character = self.character
        fit.booster = self.booster
        useCharImplants = self.serviceFittingOptions["useCharacterImplantsByDefault"]
        fit.implantLocation = ImplantLocation.CHARACTER if useCharImplants else ImplantLocation.FIT
        eos.db.save(fit)
        self.recalc(fit)
        return fit.ID

    @staticmethod
    def toggleBoostFit(fitID):
        pyfalog.debug("Toggling as booster for fit ID: {0}", fitID)
        fit = eos.db.getFit(fitID)
        fit.booster = not fit.booster
        eos.db.commit()

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
            cls.processors[fitID] = wx.CommandProcessor()
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

    def toggleFactorReload(self, fitID):
        pyfalog.debug("Toggling factor reload for fit ID: {0}", fitID)
        if fitID is None:
            return None

        fit = eos.db.getFit(fitID)
        fit.factorReload = not fit.factorReload
        eos.db.commit()
        self.recalc(fit)

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

    def getFit(self, fitID, projected=False, basic=False):
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

        if basic:
            return fit

        inited = getattr(fit, "inited", None)

        if inited is None or inited is False:
            if not projected:
                for fitP in fit.projectedFits:
                    self.getFit(fitP.ID, projected=True)
                self.recalc(fit)
                fit.fill()

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

    def toggleProjected(self, fitID, thing, click):
        pyfalog.debug("Toggling projected on fit ({0}) for: {1}", fitID, thing)
        fit = eos.db.getFit(fitID)
        if isinstance(thing, es_Drone):
            if thing.amountActive == 0 and thing.canBeApplied(fit):
                thing.amountActive = thing.amount
            else:
                thing.amountActive = 0
        elif isinstance(thing, es_Fighter):
            thing.active = not thing.active
        elif isinstance(thing, es_Module):
            thing.state = es_Module.getProposedState(thing, click)
            if not thing.canHaveState(thing.state, fit):
                thing.state = State.OFFLINE
        elif isinstance(thing, FitType):
            projectionInfo = thing.getProjectionInfo(fitID)
            if projectionInfo:
                projectionInfo.active = not projectionInfo.active

        eos.db.commit()
        self.recalc(fit)

    def changeMutatedValue(self, mutator, value):
        pyfalog.debug("Changing mutated value for {} / {}: {} => {}".format(mutator.module, mutator.module.mutaplasmid, mutator.value, value))
        mutator.value = value

        eos.db.commit()
        return mutator.value

    def convertMutaplasmid(self, fitID, position, mutaplasmid):
        # this is mostly the same thing as the self.changeModule method, however it initializes an abyssal module with
        # the old module as it's base, and then replaces it
        fit = eos.db.getFit(fitID)
        base = fit.modules[position]
        fit.modules.toDummy(position)

        try:
            m = es_Module(mutaplasmid.resultingItem, base.item, mutaplasmid)
        except ValueError:
            pyfalog.warning("Invalid item: {0} AHHHH")
            return False

        if m.fits(fit):
            m.owner = fit
            fit.modules.toModule(position, m)
            if m.isValidState(State.ACTIVE):
                m.state = State.ACTIVE

            # As some items may affect state-limiting attributes of the ship, calculate new attributes first
            self.recalc(fit)
            # Then, check states of all modules and change where needed. This will recalc if needed
            self.checkStates(fit, m)

            fit.fill()
            eos.db.commit()

            return True
        else:
            return None

    @deprecated
    def addDrone(self, fitID, itemID, numDronesToAdd=1, recalc=True):
        pyfalog.debug("Adding {0} drones ({1}) to fit ID: {2}", numDronesToAdd, itemID, fitID)
        if fitID is None:
            return False

        fit = eos.db.getFit(fitID)
        item = eos.db.getItem(itemID, eager=("attributes", "group.category"))
        if item.category.name == "Drone":
            drone = None
            for d in fit.drones.find(item):
                if d is not None and d.amountActive == 0 and d.amount < max(5, fit.extraAttributes["maxActiveDrones"]):
                    drone = d
                    break

            if drone is None:
                drone = es_Drone(item)
                if drone.fits(fit) is True:
                    fit.drones.append(drone)
                else:
                    return False
            drone.amount += numDronesToAdd
            eos.db.commit()
            if recalc:
                self.recalc(fit)
            return True
        else:
            return False

    def toggleRestrictionIgnore(self, fitID):
        pyfalog.debug("Toggling restriction ignore for fit ID: {0}", fitID)
        fit = eos.db.getFit(fitID)
        fit.ignoreRestrictions = not fit.ignoreRestrictions

        # remove invalid modules when switching back to enabled fitting restrictions
        if not fit.ignoreRestrictions:
            for m in fit.modules:
                if not m.isEmpty and not m.fits(fit, False):
                    self.removeModule(fit.ID, m.modPosition)

        eos.db.commit()
        self.recalc(fit)
        return True

    def toggleFighterAbility(self, fitID, ability):
        pyfalog.debug("Toggling fighter ability for fit ID: {0}", fitID)
        fit = eos.db.getFit(fitID)
        ability.active = not ability.active
        eos.db.commit()
        self.recalc(fit)

    def toggleBoosterSideEffect(self, fitID, sideEffect):
        pyfalog.debug("Toggling booster side effect for fit ID: {0}", fitID)
        fit = eos.db.getFit(fitID)
        sideEffect.active = not sideEffect.active
        eos.db.commit()
        self.recalc(fit)

    def changeChar(self, fitID, charID):
        pyfalog.debug("Changing character ({0}) for fit ID: {1}", charID, fitID)
        if fitID is None or charID is None:
            if charID is not None:
                self.character = Character.getInstance().all5()

            return

        fit = eos.db.getFit(fitID)
        fit.character = self.character = eos.db.getCharacter(charID)
        self.recalc(fit)

    @staticmethod
    def isAmmo(itemID):
        # todo: get rid of this form the service, use directly from item
        return eos.db.getItem(itemID).isCharge

    @staticmethod
    def getTargetResists(fitID):
        pyfalog.debug("Get target resists for fit ID: {0}", fitID)
        if fitID is None:
            return

        fit = eos.db.getFit(fitID)
        return fit.targetResists

    def setTargetResists(self, fitID, pattern):
        pyfalog.debug("Set target resist for fit ID: {0}", fitID)
        if fitID is None:
            return

        fit = eos.db.getFit(fitID)
        fit.targetResists = pattern
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
            dp.name = "Selected Ammo"

        fit = eos.db.getFit(fitID)
        for attr in ("em", "thermal", "kinetic", "explosive"):
            setattr(dp, "%sAmount" % attr, ammo.getAttribute("%sDamage" % attr) or 0)

        fit.damagePattern = dp
        self.recalc(fit)

    def checkStates(self, fit, base):
        pyfalog.debug("Check states for fit ID: {0}", fit)
        changed = False
        for mod in fit.modules:
            if mod != base:
                # fix for #529, where a module may be in incorrect state after CCP changes mechanics of module
                if not mod.canHaveState(mod.state) or not mod.isValidState(mod.state):
                    mod.state = State.ONLINE
                    changed = True

        for mod in fit.projectedModules:
            # fix for #529, where a module may be in incorrect state after CCP changes mechanics of module
            if not mod.canHaveState(mod.state, fit) or not mod.isValidState(mod.state):
                mod.state = State.OFFLINE
                changed = True

        for drone in fit.projectedDrones:
            if drone.amountActive > 0 and not drone.canBeApplied(fit):
                drone.amountActive = 0
                changed = True

        return changed
        # If any state was changed, recalculate attributes again
        # if changed:
        #     self.recalc(fit)

    def refreshFit(self, fitID):
        pyfalog.debug("Refresh fit for fit ID: {0}", fitID)
        if fitID is None:
            return None

        fit = eos.db.getFit(fitID)
        eos.db.commit()
        self.recalc(fit)

    def recalc(self, fit):
        if isinstance(fit, int):
            fit = self.getFit(fit)
        start_time = time()
        pyfalog.info("=" * 10 + "recalc: {0}" + "=" * 10, fit.name)

        fit.factorReload = self.serviceFittingOptions["useGlobalForceReload"]
        fit.clear()

        fit.calculateModifiedAttributes()
        fit.fill()
        pyfalog.info("=" * 10 + "recalc time: " + str(time() - start_time) + "=" * 10)
