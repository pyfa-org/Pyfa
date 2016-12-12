# ===============================================================================
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
# ===============================================================================

from sqlalchemy import CheckConstraint, Float, ForeignKey, Boolean, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import reconstructor

from eos.db.sqlAlchemy import sqlAlchemy

Base = declarative_base()


class Modules(Base):
    __tablename__ = 'modules'
    ID = Column(Integer, primary_key=True)
    fitID = Column(Integer, ForeignKey("fits.ID"), nullable=False, index=True)
    itemID = Column(Integer, nullable=True)
    dummySlot = Column(Integer, nullable=True, default=None)
    chargeID = Column(Integer)
    state = Column(Integer, CheckConstraint("state >= -1"), CheckConstraint("state <= 2"))
    projected = Column(Boolean, default=False, nullable=False)
    position = Column(Integer)
    CheckConstraint('("dummySlot" = NULL OR "itemID" = NULL) AND "dummySlot" != "itemID"')


class Boosters(Base):
    __tablename__ = 'boosters'
    ID = Column(Integer, primary_key=True)
    itemID = Column(Integer, nullable=True)
    fitID = Column(Integer, ForeignKey("fits.ID"), nullable=False, index=True)
    active = Column(Boolean, default=False, nullable=False)


class Cargo(Base):
    __tablename__ = 'cargo'
    ID = Column(Integer, primary_key=True)
    fitID = Column(Integer, ForeignKey("fits.ID"), nullable=False, index=True)
    itemID = Column(Integer, nullable=True)
    amount = Column(Integer, nullable=True)


class Implants(Base):
    __tablename__ = 'implants'
    ID = Column(Integer, primary_key=True)
    itemID = Column(Integer, nullable=True)
    amount = Column(Integer, nullable=True)
    active = Column(Boolean, default=False, nullable=False)


class FitImplants(Base):
    __tablename__ = 'fitImplants'
    fitID = Column(Integer, ForeignKey("fits.ID"), nullable=False, index=True)
    implantID = Column(Integer, ForeignKey("implants.ID"), nullable=False, primary_key=True)


class CharImplants(Base):
    __tablename__ = 'charImplants'
    charID = Column(Integer, ForeignKey("characters.ID"), nullable=False, index=True)
    implantID = Column(Integer, ForeignKey("implants.ID"), nullable=False, primary_key=True)


class ImplantSetMap(Base):
    __tablename__ = 'implantSetMap'
    setID = Column(Integer, ForeignKey("implantSets.ID"), nullable=False, index=True)
    implantID = Column(Integer, ForeignKey("implants.ID"), nullable=False, primary_key=True)


class Characters(Base):
    __tablename__ = 'characters'
    ID = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    apiID = Column(Integer)
    apiKey = Column(Integer)
    defaultChar = Column(Integer)
    chars = Column(String, nullable=True)
    defaultLevel = Column(Integer, nullable=True)
    ownerID = Column(Integer, ForeignKey("users.ID"), nullable=True)


class Crest(Base):
    __tablename__ = 'crest'
    ID = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    refresh_token = Column(String, nullable=False)


class Drones(Base):
    __tablename__ = 'drones'
    groupID = Column(Integer, primary_key=True)
    fitID = Column(Integer, ForeignKey("fits.ID"), nullable=False, index=True)
    itemID = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False)
    amountActive = Column(Integer, nullable=False)
    projected = Column(Boolean, default=False, nullable=False)


class Fighters(Base):
    __tablename__ = 'fighters'
    groupID = Column(Integer, primary_key=True)
    fitID = Column(Integer, ForeignKey("fits.ID"), nullable=False, index=True)
    itemID = Column(Integer, nullable=False)
    active = Column(Boolean, default=False, nullable=False)
    amount = Column(Integer, nullable=False)
    projected = Column(Boolean, default=False, nullable=False)


class FighterAbilities(Base):
    __tablename__ = 'fightersAbilities'
    groupID = Column(Integer, ForeignKey("fighters.groupID"), primary_key=True, index=True)
    effectID = Column(Integer, nullable=False, primary_key=True)
    active = Column(Boolean, default=False, nullable=False)


class ProjectedFit(object):
    def __init__(self, sourceID, source_fit, amount=1, active=True):
        self.sourceID = sourceID
        self.source_fit = source_fit
        self.active = active
        self.__amount = amount

    @reconstructor
    def init(self):
        if self.source_fit.isInvalid:
            # Very rare for this to happen, but be prepared for it
            sqlAlchemy.saveddata_session.delete(self.source_fit)
            sqlAlchemy.saveddata_session.flush()
            sqlAlchemy.saveddata_session.refresh(self.victim_fit)

    # We have a series of setters and getters here just in case someone
    # downgrades and screws up the table with NULL values
    @property
    def amount(self):
        return self.__amount or 1

    @amount.setter
    def amount(self, amount):
        self.__amount = amount

    def __repr__(self):
        return "ProjectedFit(sourceID={}, victimID={}, amount={}, active={}) at {}".format(
            self.sourceID, self.victimID, self.amount, self.active, hex(id(self))
        )


class CommandFit(object):
    def __init__(self, boosterID, booster_fit, active=True):
        self.boosterID = boosterID
        self.booster_fit = booster_fit
        self.active = active

    @reconstructor
    def init(self):
        if self.booster_fit.isInvalid:
            # Very rare for this to happen, but be prepared for it
            sqlAlchemy.saveddata_session.delete(self.booster_fit)
            sqlAlchemy.saveddata_session.flush()
            sqlAlchemy.saveddata_session.refresh(self.boosted_fit)

    def __repr__(self):
        return "CommandFit(boosterID={}, boostedID={}, active={}) at {}".format(
            self.boosterID, self.boostedID, self.active, hex(id(self))
        )


class Fits(Base):
    __tablename__ = 'fits'
    ID = Column(Integer, primary_key=True)
    ownerID = Column(ForeignKey("users.ID"), nullable=True, index=True)
    shipID = Column(Integer, nullable=False, index=True)
    name = Column(String, nullable=False)
    timestamp = Column(Integer, nullable=False)
    characterID = Column(ForeignKey("characters.ID"), nullable=True)
    damagePatternID = Column(ForeignKey("damagePatterns.ID"), nullable=True)
    booster = Column(Boolean, nullable=False, index=True, default=0)
    targetResistsID = Column(ForeignKey("targetResists.ID"), nullable=True)
    modeID = Column(Integer, nullable=True)
    # TODO: Import cleanup. Figure out what to do with this
    # implantLocation = Column(Integer, nullable=False, default=es_ImplantLocation.FIT)
    implantLocation = Column(Integer, nullable=False)
    notes = Column(String, nullable=True)


class ProjectedFits(Base):
    __tablename__ = 'projectedFits'
    sourceID = Column(ForeignKey("fits.ID"), primary_key=True)
    victimID = Column(ForeignKey("fits.ID"), primary_key=True)
    amount = Column(Integer, nullable=False, default=1)
    active = Column(Boolean, nullable=False, default=1)


class CommandFits(Base):
    __tablename__ = 'commandFits'
    boosterID = Column(ForeignKey("fits.ID"), primary_key=True)
    boostedID = Column(ForeignKey("fits.ID"), primary_key=True)
    active = Column(Boolean, nullable=False, default=1)


class Gangs(Base):
    __tablename__ = 'gangs'
    ID = Column(Integer, primary_key=True)
    leaderID = Column(ForeignKey("fits.ID"))
    boosterID = Column(ForeignKey("fits.ID"))
    name = Column(String)


class Wings(Base):
    __tablename__ = 'wings'
    ID = Column(Integer, primary_key=True)
    gangID = Column(ForeignKey("gangs.ID"))
    boosterID = Column(ForeignKey("fits.ID"))
    leaderID = Column(ForeignKey("fits.ID"))


class Squads(Base):
    __tablename__ = 'squads'
    ID = Column(Integer, primary_key=True)
    wingID = Column(ForeignKey("wings.ID"))
    leaderID = Column(ForeignKey("fits.ID"))
    boosterID = Column(ForeignKey("fits.ID"))


class SquadMembers(Base):
    __tablename__ = 'squadmembers'
    squadID = Column(ForeignKey("squads.ID"), primary_key=True)
    memberID = Column(ForeignKey("fits.ID"), primary_key=True)


class ImplantSets(Base):
    __tablename__ = 'implantSets'
    ID = Column(Integer, primary_key=True)
    name = Column(String, nullable=False),


class Miscdata(Base):
    __tablename__ = 'miscdata'
    fieldName = Column(String, primary_key=True)
    fieldValue = Column(String)


class Overrides(Base):
    __tablename__ = 'overrides'
    itemID = Column(Integer, primary_key=True, index=True)
    attrID = Column(Integer, primary_key=True, index=True)
    value = Column(Float, nullable=False)


class Prices(Base):
    __tablename__ = 'prices'
    typeID = Column(Integer, primary_key=True)
    price = Column(Float)
    time = Column(Integer, nullable=False)
    failed = Column(Integer)


class CharacterSkills(Base):
    __tablename__ = 'characterSkills'
    characterID = Column(ForeignKey("characters.ID"), primary_key=True, index=True)
    itemID = Column(Integer, primary_key=True)
    _Skill__level = Column(Integer, nullable=True)


class TargetResists(Base):
    __tablename__ = 'targetResists'
    ID = Column(Integer, primary_key=True)
    name = Column(String)
    emAmount = Column(Float)
    thermalAmount = Column(Float)
    kineticAmount = Column(Float)
    explosiveAmount = Column(Float)
    ownerID = Column(ForeignKey("users.ID"), nullable=True)


class Users(Base):
    __tablename__ = 'users'
    ID = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    admin = Column(Boolean, nullable=False)


class DamagePatterns(Base):
    __tablename__ = 'damagePatterns'
    ID = Column(Integer, primary_key=True)
    name = Column(String)
    emAmount = Column(Integer)
    thermalAmount = Column(Integer)
    kineticAmount = Column(Integer)
    explosiveAmount = Column(Integer)
    ownerID = Column(ForeignKey("users.ID"), nullable=True)
