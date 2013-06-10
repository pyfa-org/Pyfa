#===============================================================================
# Copyright (C) 2010 Diego Duclos
#               2010 Anton Vorobyov
#
# This file and all other files in this folder (and its subfolders) are part of eos.
#
# eos is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# eos is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with eos.  If not, see <http://www.gnu.org/licenses/>.
#===============================================================================

import unittest

from eos import db
from eos.types import Fit, Character, Skill, Ship, Module, Drone, Booster, Fleet, Wing, Squad, State

class TestBase(unittest.TestCase):
    def setUp(self):
        db.saveddata_meta.create_all()

    def tearDown(self):
        db.saveddata_meta.drop_all()
        db.saveddata_session.expunge_all()

    def __addFitItem(self, fit, item, state=None):
        # Map textual description to actual states
        statemap = {"offline": State.OFFLINE,
                    "online": State.ONLINE,
                    "active": State.ACTIVE,
                    "overheated": State.OVERHEATED}
        # Gather some data about item being fitted
        item_itm = db.getItem(item)
        cat = item_itm.category.name.lower()
        grp = item_itm.group.name.lower()
        # Append it to proper category
        if cat == "drone":
            item_inst = Drone(item_itm)
            fit.drones.append(item_inst)
        elif cat in ("module", "subsystem"):
            item_inst = Module(item_itm)
            fit.modules.append(item_inst)
            if state and state in statemap:
                item_inst.state = statemap[state]
        elif cat == "charge":
            # Use dummy container for any charge
            item_inst = Module(db.getItem("Bomb Launcher I"))
            item_inst.charge = item_itm
            fit.modules.append(item_inst)
        elif cat == "implant" and grp == "booster":
            item_inst = Booster(item_itm)
            fit.boosters.append(item_inst)
        # We need item_inst outside of the method
        return item_inst

    def __detectTupleType(self, tuple):
        # Define acceptable textual state descriptions
        states = ("offline", "online", "active", "overheated")
        # Do not check anything, assume that it's proper item
        if len(tuple) == 1:
            return "itm"
        # Detect if it's item with state or 2 single items
        elif len(tuple) == 2:
            if tuple[1] in states:
                return "itmstt"
            else:
                return "itms"
        elif len(tuple) > 2:
            return "itms"
        else:
            return None

    def __fitItems(self, fit, itms):
        if isinstance(itms, (tuple, list)):
            tt = self.__detectTupleType(itms)
            if tt == "itm":
                self.__addFitItem(fit, itms)
            elif tt == "itmstt":
                self.__addFitItem(fit, itms[0], state=itms[1])
            elif tt == "itms":
                for itm in itms:
                    if isinstance(itm, (tuple, list)):
                        tt = self.__detectTupleType(itm)
                        if tt == "itm":
                            self.__addFitItem(fit, itm)
                        elif tt == "itmstt":
                            self.__addFitItem(fit, itm[0], state=itm[1])
                    else:
                        self.__addFitItem(fit, itm)
        elif itms:
            self.__addFitItem(fit, itms)

    def getItemAttr(self, attr, item, skill=None, ship="Rifter", getCharge=False, gang=False, miscitms=None):
        # Create a fit which will be tested
        fit = Fit()
        # Create character for fit and assign it
        char = Character("test")
        # Assign skills to character only when requested
        if not gang and skill:
            skill_itm = db.getItem(skill[0])
            skill_lvl = skill[1]
            char.addSkill(Skill(skill_itm, skill_lvl))
        fit.character = char
        # Create ship and assign to fit; use default Rifter dummy
        # in any case as some items affect ship attributes, they can't
        # be tested w/o ship
        fit.ship = Ship(db.getItem(ship))
        # Create and fit an item which will be tested
        item_inst = self.__addFitItem(fit, item)
        # Add other modules which can affect ship attributes
        if miscitms:
            self.__fitItems(fit, miscitms)
        # Finish composing of tested fit by calculating its attributes
        fit.calculateModifiedAttributes()
        # Use special fit as gang booster when requested
        if gang:
            # Do the same for character which will be
            # squad booster
            squad_fit = Fit()
            squad_char = Character("squad_test")
            # Add leadership skill which is required to boost squad members
            squad_char.addSkill(Skill(db.getItem("Leadership"), 1))
            if skill:
                squad_skill_itm = db.getItem(skill[0])
                squad_skill_lvl = skill[1]
                squad_char.addSkill(Skill(squad_skill_itm, squad_skill_lvl))
            squad_fit.character = squad_char
            squad_fit.ship = Ship(db.getItem(ship))
            squad_fit.calculateModifiedAttributes()
            # Create full fleet structure and assign roles
            squad = Squad()
            squad.leader = squad_fit
            squad.members.append(squad_fit)
            squad.members.append(fit)
            wing = Wing()
            wing.squads.append(squad)
            fleet = Fleet()
            fleet.wings.append(wing)
            # Calculate fleet relationships
            fleet.calculateModifiedAttributes()
        # Use charge as an item when it was requested to be tested,
        # and passed item itself in all other cases
        cat = db.getItem(item).category.name.lower()
        if (cat == "drone" and getCharge) or cat == "charge":
            result = item_inst.getModifiedChargeAttr(attr)
        else:
            result = item_inst.getModifiedItemAttr(attr)
        return result

    def getShipAttr(self, attr, ship="Rifter", skill=None, gang=False, miscitms=None, unmod=False):
        # Create a fit for testing
        fit = Fit()
        # Create character for fit
        char = Character("test")
        # Assign skills only when we need to do so
        if not gang and skill:
            skill_itm = db.getItem(skill[0])
            skill_lvl = skill[1]
            char.addSkill(Skill(skill_itm, skill_lvl))
        fit.character = char
        # Create a ship and assign it to the fitting
        fit.ship = Ship(db.getItem(ship))
        # Add other modules which can affect ship attributes
        if miscitms:
            self.__fitItems(fit, miscitms)
        # We're done, calculate attributes
        fit.calculateModifiedAttributes()
        # Define a gang booster
        if gang:
            squad_fit = Fit()
            squad_char = Character("squad_test")
            # Add leadership skill which is required to boost squad members
            squad_char.addSkill(Skill(db.getItem("Leadership"), 1))
            if skill:
                squad_skill_itm = db.getItem(skill[0])
                squad_skill_lvl = skill[1]
                squad_char.addSkill(Skill(squad_skill_itm, squad_skill_lvl))
            squad_fit.character = squad_char
            squad_fit.ship = Ship(db.getItem(ship))
            squad_fit.calculateModifiedAttributes()
            squad = Squad()
            squad.leader = squad_fit
            squad.members.append(squad_fit)
            squad.members.append(fit)
            wing = Wing()
            wing.squads.append(squad)
            fleet = Fleet()
            fleet.wings.append(wing)
            fleet.calculateModifiedAttributes()
        # Autodetect which attributes group to use
        if attr in fit.extraAttributes:
            result = fit.extraAttributes[attr]
        else:
            if unmod:
                result = fit.ship.item.attributes[attr].value
            else:
                result = fit.ship.getModifiedItemAttr(attr)
        return result
