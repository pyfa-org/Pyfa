#===============================================================================
# Copyright (C) 2010 Diego Duclos
#
# This file is part of eos.
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

from itertools import chain
from eos.types import Skill, Module, Ship
from copy import deepcopy

class Fleet(object):
    def calculateModifiedAttributes(self):
        #Make sure ALL fits in the gang have been calculated
        for c in chain(self.wings, (self.leader,)):
            if c is not None: c.calculateModifiedAttributes()

        leader = self.leader
        self.booster = booster = self.booster if self.booster is not None else leader
        self.broken = False
        self.store = store = Store()
        store.set(booster, "fleet")
        #Go all the way down for each subtree we have.
        for wing in self.wings:
            wing.calculateGangBonusses(store)

        # Check skill requirements and wing amount to see if we break or not
        if len(self.wings) == 0 or leader is None or leader.character is None or leader.character.getSkill("Fleet Command").level < len(self.wings):
            self.broken = True

        #Now calculate our own if we aren't broken
        if self.broken == False:
            #We only get our own bonuses *Sadface*
            store.apply(leader, "fleet")

    def recalculateLinear(self, withBoosters=True, dirtyStorage=None):
        self.store = Store()
        self.linearBoosts = {}
        if withBoosters is True:
            if self.leader is not None and self.leader.character is not None and self.leader.character.getSkill("Fleet Command").level >= 1:
                self.leader.boostsFits.add(self.wings[0].squads[0].members[0].ID)
                self.leader.calculateModifiedAttributes()
                self.store.set(self.leader, "squad", clearingUpdate=True)
            else:
                self.store = Store()
                if self.leader is not None:
                    try:
                        self.leader.boostsFits.remove(self.wings[0].squads[0].members[0].ID)
                    except KeyError:
                        pass
        self.wings[0].recalculateLinear(self.store, withBoosters=withBoosters, dirtyStorage=dirtyStorage)
        return self.linearBoosts

    def count(self):
        total = 0
        for wing in self.wings:
            total += wing.count()

        return total

    def extend(self):
        self.wings.append(Wing())

    def __deepcopy__(self, memo):
        copy = Fleet()
        copy.name = self.name
        copy.booster = deepcopy(self.booster)
        copy.leader = deepcopy(self.leader)
        for wing in self.wings:
            copy.wings.append(deepcopy(wing))

        return copy

class Wing(object):
    def calculateModifiedAttributes(self):
        for c in chain(self.squads, (self.leader,)):
            if c is not None: c.calculateModifiedAttributes()

    def calculateGangBonusses(self, store):
        self.broken = False
        leader = self.leader
        self.booster = booster = self.booster if self.booster is not None else leader

        store.set(booster, "wing")

        #ALWAYS move down
        for squad in self.squads:
            squad.calculateGangBonusses(store)

        # Check skill requirements and squad amount to see if we break or not
        if len(self.squads) == 0 or leader is None or leader.character is None or leader.character.getSkill("Wing Command").level < len(self.squads):
            self.broken = True

        #Check if we aren't broken, if we aren't, boost
        if self.broken == False:
            store.apply(leader, "wing")
        else:
            #We broke, don't go up
            self.gang.broken = True

    def recalculateLinear(self, store, withBoosters=True, dirtyStorage=None):
        if withBoosters is True:
            if self.leader is not None and self.leader.character is not None and self.leader.character.getSkill("Wing Command").level >= 1:
                self.leader.boostsFits.add(self.squads[0].members[0].ID)
                self.leader.calculateModifiedAttributes()
                store.set(self.leader, "squad", clearingUpdate=False)
            else:
                store = Store()
                if self.gang.leader is not None:
                    try:
                        self.gang.leader.boostsFits.remove(self.squads[0].members[0].ID)
                    except KeyError:
                        pass
                if self.leader is not None:
                    try:
                        self.leader.boostsFits.remove(self.squads[0].members[0].ID)
                    except KeyError:
                        pass
        self.squads[0].recalculateLinear(store, withBoosters=withBoosters, dirtyStorage=dirtyStorage)

    def count(self):
        total = 0 if self.leader is None else 1
        for squad in self.squads:
            total += squad.count()

        return total

    def extend(self):
        self.squads.append(Squad())

    def __deepcopy__(self, memo):
        copy = Wing()
        copy.booster = deepcopy(self.booster)
        copy.leader = deepcopy(self.leader)
        for squad in self.squads:
            copy.squads.append(deepcopy(squad))

        return copy


class Squad(object):
    def calculateModifiedAttributes(self):
        for member in self.members:
            member.calculateModifiedAttributes()

    def calculateGangBonusses(self, store):
        self.broken = False
        leader = self.leader
        self.booster = booster = self.booster if self.booster is not None else leader
        store.set(booster, "squad")

        # Check skill requirements and squad size to see if we break or not
        if len(self.members) <= 0 or leader is None or leader.character is None or leader.character.getSkill("Leadership").level * 2 < len(self.members):
            self.broken = True

        if self.broken == False:
            for member in self.members:
                store.apply(member, "squad")
        else:
            self.wing.broken = True

    def recalculateLinear(self, store, withBoosters=True, dirtyStorage=None):
        if withBoosters is True:
            if self.leader is not None and self.leader.character is not None and self.leader.character.getSkill("Leadership").level >= 1:
                self.leader.boostsFits.add(self.members[0].ID)
                self.leader.calculateModifiedAttributes(dirtyStorage=dirtyStorage)
                store.set(self.leader, "squad", clearingUpdate=False)
            else:
                store = Store()
                if self.leader is not None:
                    try:
                        self.leader.boostsFits.remove(self.members[0].ID)
                    except KeyError:
                        pass
                if self.wing.leader is not None:
                    try:
                        self.wing.leader.boostsFits.remove(self.members[0].ID)
                    except KeyError:
                        pass
                if self.wing.gang.leader is not None:
                    try:
                        self.wing.gang.leader.boostsFits.remove(self.members[0].ID)
                    except KeyError:
                        pass
        if getattr(self.wing.gang, "linearBoosts", None) is None:
            self.wing.gang.linearBoosts = {}
        dict = store.bonuses["squad"]
        for boostedAttr, boostInfoList in dict.iteritems():
            for boostInfo in boostInfoList:
                effect, thing = boostInfo
                # Get current boost value for given attribute, use 0 as fallback if
                # no boosts applied yet
                currBoostAmount = self.wing.gang.linearBoosts.get(boostedAttr, (0,))[0]
                # Attribute name which is used to get boost value
                newBoostAttr = effect.getattr("gangBonus") or "commandBonus"
                # Get boost amount for current boost
                newBoostAmount = thing.getModifiedItemAttr(newBoostAttr) or 0
                # If skill takes part in gang boosting, multiply by skill level
                if type(thing) == Skill:
                    newBoostAmount *= thing.level
                # If new boost is more powerful, replace older one with it
                if abs(newBoostAmount) > abs(currBoostAmount):
                    self.wing.gang.linearBoosts[boostedAttr] = (newBoostAmount, boostInfo)

    def count(self):
        return len(self.members)

    def __deepcopy__(self, memo):
        copy = Squad()
        copy.booster = deepcopy(self.booster)
        copy.leader = deepcopy(self.leader)
        for member in self.members:
            copy.members.append(deepcopy(member))

        return copy

class Store(object):
    def __init__(self):
        # Container for gang boosters and their respective bonuses, three-layered
        self.bonuses = {}
        for dictType in ("fleet", "wing", "squad"):
            self.bonuses[dictType] = {}
        # Container for boosted fits and corresponding boosts applied onto them
        self.boosts = {}

    def set(self, fitBooster, layer, clearingUpdate=True):
        """Add all gang boosts of given fit for given layer to boost store"""
        if fitBooster is None:
            return

        # This dict contains all bonuses for specified layer
        dict = self.bonuses[layer]
        if clearingUpdate is True:
            # Clear existing bonuses
            dict.clear()

        # Go through everything which can be used as gang booster
        for thing in chain(fitBooster.modules, fitBooster.implants, fitBooster.character.iterSkills(), (fitBooster.ship,)):
            if thing.item is None:
                continue
            for effect in thing.item.effects.itervalues():
                # And check if it actually has gang boosting effects
                if effect.isType("gang"):
                    # Attribute which is boosted
                    boostedAttr = effect.getattr("gangBoost")
                    # List which contains all bonuses for given attribute for given layer
                    l = dict.get(boostedAttr)
                    # If there was no list, create it
                    if l is None:
                        l = dict[boostedAttr] = []
                    # And append effect which is used to boost stuff and carrier of this effect
                    l.append((effect, thing))

    contextMap = {Skill: "skill",
                  Ship: "ship",
                  Module: "module"}

    def apply(self, fitBoosted, layer):
        """Applies all boosts onto given fit for given layer"""
        if fitBoosted is None:
            return
        # Boosts dict contains all bonuses applied onto given fit
        self.boosts[fitBoosted] = boosts = {}
        # Go through all bonuses for given layer, and find highest one per boosted attribute
        for currLayer in ("fleet", "wing", "squad"):
            # Dictionary with boosts for given layer
            dict = self.bonuses[currLayer]
            for boostedAttr, boostInfoList in dict.iteritems():
                for boostInfo in boostInfoList:
                    effect, thing = boostInfo
                    # Get current boost value for given attribute, use 0 as fallback if
                    # no boosts applied yet
                    currBoostAmount = boosts.get(boostedAttr, (0,))[0]
                    # Attribute name which is used to get boost value
                    newBoostAttr = effect.getattr("gangBonus") or "commandBonus"
                    # Get boost amount for current boost
                    newBoostAmount = thing.getModifiedItemAttr(newBoostAttr) or 0
                    # If skill takes part in gang boosting, multiply by skill level
                    if type(thing) == Skill:
                        newBoostAmount *= thing.level
                    # If new boost is more powerful, replace older one with it
                    if abs(newBoostAmount) > abs(currBoostAmount):
                        boosts[boostedAttr] = (newBoostAmount, boostInfo)

            # Don't look further down then current layer, wing commanders don't get squad bonuses and all that
            if layer == currLayer:
                break

        self.modify(fitBoosted)

    def getBoosts(self, fit):
        """Return all boosts applied onto given fit"""
        return self.boosts.get(fit)

    def modify(self, fitBoosted):
        # Get all boosts which should be applied onto current fit
        boosts = self.getBoosts(fitBoosted)
        # Now we got it all figured out, actually do the useful part of all this
        for name, info in boosts.iteritems():
            # Unpack all data required to run effect properly
            effect, thing = info[1]
            context = ("gang", self.contextMap[type(thing)])
            # Run effect, and get proper bonuses applied
            try:
                effect.handler(fitBoosted, thing, context)
            except:
                pass
