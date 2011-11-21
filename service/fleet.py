#===============================================================================
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
#===============================================================================

import eos.db
from eos.types import Fleet as Fleet_, Wing, Squad
import copy

class Fleet(object):
    instance = None
    @classmethod
    def getInstance(cls):
        if cls.instance is None:
            cls.instance = Fleet()

        return cls.instance

    def __init__(self):
        pass

    def getFleetList(self):
        fleetList = []
        fleets = eos.db.getFleetList()
        for fleet in fleets:
            fleetList.append((fleet.ID, fleet.name, fleet.count()))

        return fleetList

    def getFleetByID(self, ID):
        f = eos.db.getFleet(ID)
        return f

    def addFleet(self):
        f = Fleet_()
        eos.db.save(f)
        return f

    def renameFleet(self, fleet, newName):
        fleet.name = newName
        eos.db.commit()

    def copyFleet(self, fleet):
        newFleet = copy.deepcopy(fleet)
        eos.db.save(newFleet)
        return newFleet

    def copyFleetByID(self, ID):
        fleet = self.getFleetByID(ID)
        return self.copyFleet(fleet)

    def deleteFleet(self, fleet):
        eos.db.remove(fleet)

    def deleteFleetByID(self, ID):
        fleet = self.getFleetByID(ID)
        self.deleteFleet(fleet)

    def makeLinearFleet(self, fit):
        f = Fleet_()
        w = Wing()
        f.wings.append(w)
        s = Squad()
        w.squads.append(s)
        s.members.append(fit)
        eos.db.save(f)

    def setLinearFleetCom(self, boostee, booster):
        if boostee == booster:
            return
        if self.isInLinearFleet(boostee) is False:
            self.removeAssociatedFleetData(boostee)
            self.makeLinearFleet(boostee)
        squadIDs = set(eos.db.getSquadsIDsWithFitID(boostee.ID))
        squad = eos.db.getSquad(squadIDs.pop())
        squad.wing.gang.leader = booster
        if self.anyBoosters(squad):
            squad.wing.gang.calculateModifiedAttributes()
        else:
            self.removeAssociatedFleetData(boostee)

    def setLinearWingCom(self, boostee, booster):
        if boostee == booster:
            return
        if self.isInLinearFleet(boostee) is False:
            self.removeAssociatedFleetData(boostee)
            self.makeLinearFleet(boostee)
        squadIDs = set(eos.db.getSquadsIDsWithFitID(boostee.ID))
        squad = eos.db.getSquad(squadIDs.pop())
        squad.wing.leader = booster
        if self.anyBoosters(squad):
            squad.wing.gang.calculateModifiedAttributes()
        else:
            self.removeAssociatedFleetData(boostee)

    def setLinearSquadCom(self, boostee, booster):
        if boostee == booster:
            return
        if self.isInLinearFleet(boostee) is False:
            self.removeAssociatedFleetData(boostee)
            self.makeLinearFleet(boostee)
        squadIDs = set(eos.db.getSquadsIDsWithFitID(boostee.ID))
        squad = eos.db.getSquad(squadIDs.pop())
        squad.leader = booster
        if self.anyBoosters(squad):
            squad.wing.gang.calculateModifiedAttributes()
        else:
            self.removeAssociatedFleetData(boostee)

    def isInLinearFleet(self, fit):
        sqIDs = eos.db.getSquadsIDsWithFitID(fit.ID)
        if len(sqIDs) != 1:
            return False
        s = eos.db.getSquad(sqIDs[0])
        if len(s.members) != 1:
            return False
        w = s.wing
        if len(w.squads) != 1:
            return False
        f = w.gang
        if len(f.wings) != 1:
            return False
        return True

    def removeAssociatedFleetData(self, fit):
        squadIDs = set(eos.db.getSquadsIDsWithFitID(fit.ID))
        if len(squadIDs) == 0:
            return
        squads = list(eos.db.getSquad(sqID) for sqID in squadIDs)
        wingIDs = set(squad.wing.ID for squad in squads)
        fleetIDs = set(squad.wing.gang.ID for squad in squads)
        for fleetID in fleetIDs:
            fleet = eos.db.getFleet(fleetID)
            for wing in fleet.wings:
                wingIDs.add(wing.ID)
        for wingID in wingIDs:
            wing = eos.db.getWing(wingID)
            for squad in wing.squads:
                squadIDs.add(squad.ID)
        for squadID in squadIDs:
            squad = eos.db.getSquad(squadID)
            eos.db.remove(squad)
        for wingID in wingIDs:
            wing = eos.db.getWing(wingID)
            eos.db.remove(wing)
        for fleetID in fleetIDs:
            fleet = eos.db.getFleet(fleetID)
            eos.db.remove(fleet)
        return

    def anyBoosters(self, squad):
        wing = squad.wing
        fleet = wing.gang
        if squad.leader is None and wing.leader is None and fleet.leader is None:
            return False
        return True
