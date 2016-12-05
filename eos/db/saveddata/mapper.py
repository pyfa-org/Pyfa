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

'''
Old sqlAlchemy imports
from sqlalchemy import CheckConstraint, Float, ForeignKey, Boolean, Table, Column, Integer, String
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import reconstructor, relationship, relation, mapper
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.sql import and_
from sqlalchemy.ext.declarative import declarative_base
'''

from sqlalchemy import CheckConstraint, Float, ForeignKey, Boolean, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import reconstructor

from eos.db import saveddata_session

'''
import eos.saveddata.character as Character
from eos.db import saveddata_meta
from eos.effectHandlerHelpers import HandledImplantBoosterList
from eos.effectHandlerHelpers import HandledModuleList, HandledProjectedModList, HandledDroneCargoList, \
    HandledProjectedDroneList
from eos.saveddata.booster import Booster as es_Booster
from eos.saveddata.cargo import Cargo as es_Cargo
from eos.saveddata.crestchar import CrestChar as es_CrestChar
from eos.saveddata.damagePattern import DamagePattern as es_DamagePattern
from eos.saveddata.drone import Drone as es_Drone
from eos.saveddata.fighter import Fighter as es_Fighter
from eos.saveddata.fighterAbility import FighterAbility as es_FighterAbility
from eos.saveddata.fit import Fit as es_Fit
from eos.saveddata.fit import ImplantLocation as es_ImplantLocation
from eos.saveddata.fleet import Fleet as es_Fleet
from eos.saveddata.fleet import Squad as es_Squad
from eos.saveddata.fleet import Wing as es_Wing
from eos.saveddata.implant import Implant as es_Implant
from eos.saveddata.implantSet import ImplantSet as es_ImplantSet
from eos.saveddata.miscData import MiscData as es_MiscData
from eos.saveddata.module import Module as es_Module
from eos.saveddata.override import Override as es_Override
from eos.saveddata.price import Price as es_Price
from eos.saveddata.skill import Skill as es_Skill
from eos.saveddata.targetResists import TargetResists as es_TargetResists
from eos.saveddata.user import User as es_User
'''

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

    # Legacy code
    '''
    mapper(es_Module, modules_table,
           properties={"owner": relation(es_Fit)})
    '''


class Boosters(Base):
    __tablename__ = 'boosters'
    ID = Column(Integer, primary_key=True)
    itemID = Column(Integer, nullable=True)
    fitID = Column(Integer, ForeignKey("fits.ID"), nullable=False, index=True)
    active = Column(Boolean, default=False, nullable=False)

    # Legacy code
    '''
    mapper(es_Booster, boosters_table,
           properties={"_Booster__activeSideEffectDummies": relation(ActiveSideEffectsDummy)})
    '''


class Cargo(Base):
    __tablename__ = 'cargo'
    ID = Column(Integer, primary_key=True)
    fitID = Column(Integer, ForeignKey("fits.ID"), nullable=False, index=True)
    itemID = Column(Integer, nullable=True)
    amount = Column(Integer, nullable=True)

    # Legacy Code
    # mapper(es_Cargo, cargo_table)


class Implants(Base):
    __tablename__ = 'implants'
    ID = Column(Integer, primary_key=True)
    itemID = Column(Integer, nullable=True)
    amount = Column(Integer, nullable=True)
    active = Column(Boolean, default=False, nullable=False)

    # mapper(es_Implant, implants_table)


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

    # Legacy code
    '''
    mapper(Character.Character, characters_table,
           properties={
               "savedName": characters_table.c.name,
               "_Character__owner": relation(
                   es_User,
                   backref="characters"),
               "_Character__skills": relation(
                   Character.Skill,
                   backref="character",
                   cascade="all,delete-orphan"),
               "_Character__implants": relation(
                   es_Implant,
                   collection_class=HandledImplantBoosterList,
                   cascade='all,delete-orphan',
                   backref='character',
                   single_parent=True,
                   primaryjoin=Implants.charImplants_table.c.charID == characters_table.c.ID,
                   secondaryjoin=Implants.charImplants_table.c.implantID == es_Implant.ID,
                   secondary=Implants.charImplants_table),
           })
    '''


class Crest(Base):
    __tablename__ = 'crest'
    ID = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    refresh_token = Column(String, nullable=False)

    # mapper(es_CrestChar, crest_table)


class Drones(Base):
    __tablename__ = 'drones'
    groupID = Column(Integer, primary_key=True)
    fitID = Column(Integer, ForeignKey("fits.ID"), nullable=False, index=True)
    itemID = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False)
    amountActive = Column(Integer, nullable=False)
    projected = Column(Boolean, default=False, nullable=False)

    # mapper(es_Drone, drones_table)


class Fighters(Base):
    __tablename__ = 'fighters'
    groupID = Column(Integer, primary_key=True)
    fitID = Column(Integer, ForeignKey("fits.ID"), nullable=False, index=True)
    itemID = Column(Integer, nullable=False)
    active = Column(Boolean, default=False, nullable=False)
    amount = Column(Integer, nullable=False)
    projected = Column(Boolean, default=False, nullable=False)

    '''
    mapper(es_Fighter, fighters_table,
           properties={
               "owner": relation(es_Fit),
               "_Fighter__abilities": relation(
                   es_FighterAbility,
                   backref="fighter",
                   cascade='all, delete, delete-orphan'),
           })
    '''


class FighterAbilities(Base):
    __tablename__ = 'fightersAbilities'
    groupID = Column(Integer, ForeignKey("fighters.groupID"), primary_key=True, index=True)
    effectID = Column(Integer, nullable=False, primary_key=True)
    active = Column(Boolean, default=False, nullable=False)

    # mapper(es_FighterAbility, fighter_abilities_table)


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
            saveddata_session.delete(self.source_fit)
            saveddata_session.flush()
            saveddata_session.refresh(self.victim_fit)

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
            saveddata_session.delete(self.booster_fit)
            saveddata_session.flush()
            saveddata_session.refresh(self.boosted_fit)

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


'''
es_Fit._Fit__projectedFits = association_proxy(
    "victimOf",  # look at the victimOf association...
    "source_fit",  # .. and return the source fits
    creator=lambda sourceID, source_fit: ProjectedFit(sourceID, source_fit)
es_Fit._Fit__commandFits = association_proxy(
    "boostedOf",  # look at the boostedOf association...
    "booster_fit",  # .. and return the booster fit
    creator=lambda boosterID, booster_fit: CommandFit(boosterID, booster_fit)
)

mapper(
    es_Fit,
    fits_table,
    properties={
        "_Fit__modules": relation(
            es_Module,
            collection_class=HandledModuleList,
            primaryjoin=and_(Modules.modules_table.c.fitID == fits_table.c.ID,
                             Modules.modules_table.c.projected is False),
            order_by=Modules.modules_table.c.position,
            cascade='all, delete, delete-orphan'),
        "_Fit__projectedModules": relation(
            es_Module,
            collection_class=HandledProjectedModList,
            cascade='all, delete, delete-orphan',
            single_parent=True,
            primaryjoin=and_(Modules.modules_table.c.fitID == fits_table.c.ID,
                             Modules.modules_table.c.projected is True)),
        "owner": relation(
            es_User,
            backref="fits"),
        "itemID": fits_table.c.shipID,
        "shipID": fits_table.c.shipID,
        "_Fit__boosters": relation(
            es_Booster,
            collection_class=HandledImplantBoosterList,
            cascade='all, delete, delete-orphan',
            single_parent=True),
        "_Fit__drones": relation(
            es_Drone,
            collection_class=HandledDroneCargoList,
            cascade='all, delete, delete-orphan',
            single_parent=True,
            primaryjoin=and_(Drones.drones_table.c.fitID == fits_table.c.ID,
                             Drones.drones_table.c.projected is False)),
        "_Fit__fighters": relation(
            es_Fighter,
            collection_class=HandledDroneCargoList,
            cascade='all, delete, delete-orphan',
            single_parent=True,
            primaryjoin=and_(Fighters.fighters_table.c.fitID == fits_table.c.ID,
                             Fighters.fighters_table.c.projected is False)),
        "_Fit__cargo": relation(
            es_Cargo,
            collection_class=HandledDroneCargoList,
            cascade='all, delete, delete-orphan',
            single_parent=True,
            primaryjoin=and_(Cargo.cargo_table.c.fitID == fits_table.c.ID)),
        "_Fit__projectedDrones": relation(
            es_Drone,
            collection_class=HandledProjectedDroneList,
            cascade='all, delete, delete-orphan',
            single_parent=True,
            primaryjoin=and_(Drones.drones_table.c.fitID == fits_table.c.ID,
                             Drones.drones_table.c.projected is True)),
        "_Fit__projectedFighters": relation(
            es_Fighter,
            collection_class=HandledProjectedDroneList,
            cascade='all, delete, delete-orphan',
            single_parent=True,
            primaryjoin=and_(Fighters.fighters_table.c.fitID == fits_table.c.ID,
                             Fighters.fighters_table.c.projected is True)),
        "_Fit__implants": relation(
            es_Implant,
            collection_class=HandledImplantBoosterList,
            cascade='all, delete, delete-orphan',
            backref='fit',
            single_parent=True,
            primaryjoin=Implants.fitImplants_table.c.fitID == fits_table.c.ID,
            secondaryjoin=Implants.fitImplants_table.c.implantID == es_Implant.ID,
            secondary=Implants.fitImplants_table),
        "_Fit__character": relation(
            Character.Character,
            backref="fits"),
        "_Fit__damagePattern": relation(es_DamagePattern),
        "_Fit__targetResists": relation(es_TargetResists),
        "projectedOnto": relationship(
            ProjectedFit,
            primaryjoin=projectedFits_table.c.sourceID == fits_table.c.ID,
            backref='source_fit',
            collection_class=attribute_mapped_collection('victimID'),
            cascade='all, delete, delete-orphan'),
        "victimOf": relationship(
            ProjectedFit,
            primaryjoin=fits_table.c.ID == projectedFits_table.c.victimID,
            backref='victim_fit',
            collection_class=attribute_mapped_collection('sourceID'),
            cascade='all, delete, delete-orphan'),
        "boostedOnto": relationship(
            CommandFit,
            primaryjoin=commandFits_table.c.boosterID == fits_table.c.ID,
            backref='booster_fit',
            collection_class=attribute_mapped_collection('boostedID'),
            cascade='all, delete, delete-orphan'),
        "boostedOf": relationship(
            CommandFit,
            primaryjoin=fits_table.c.ID == commandFits_table.c.boostedID,
            backref='boosted_fit',
            collection_class=attribute_mapped_collection('boosterID'),
            cascade='all, delete, delete-orphan'),
    }
)


mapper(ProjectedFit, projectedFits_table,
       properties={"_ProjectedFit__amount": projectedFits_table.c.amount})

mapper(CommandFit, commandFits_table)
'''


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


'''
mapper(es_Fleet, gangs_table,
       properties={"wings": relation(es_Wing, backref="gang"),
                   "leader": relation(es_Fit, primaryjoin=gangs_table.c.leaderID == Fits.fits_table.c.ID),
                   "booster": relation(es_Fit, primaryjoin=gangs_table.c.boosterID == Fits.fits_table.c.ID)})

mapper(es_Wing, wings_table,
       properties={"squads": relation(es_Squad, backref="wing"),
                   "leader": relation(es_Fit, primaryjoin=wings_table.c.leaderID == Fits.fits_table.c.ID),
                   "booster": relation(es_Fit, primaryjoin=wings_table.c.boosterID == Fits.fits_table.c.ID)})

mapper(es_Squad, squads_table,
       properties={"leader": relation(es_Fit, primaryjoin=squads_table.c.leaderID == Fits.fits_table.c.ID),
                   "booster": relation(es_Fit, primaryjoin=squads_table.c.boosterID == Fits.fits_table.c.ID),
                   "members": relation(es_Fit,
                                       primaryjoin=squads_table.c.ID == squadmembers_table.c.squadID,
                                       secondaryjoin=squadmembers_table.c.memberID == Fits.fits_table.c.ID,
                                       secondary=squadmembers_table)})
'''


class ImplantSets(Base):
    __tablename__ = 'implantSets'
    ID = Column(Integer, primary_key=True)
    name = Column(String, nullable=False),


'''
mapper(es_ImplantSet, implant_set_table,
       properties={
           "_ImplantSet__implants": relation(
               es_Implant,
               collection_class=HandledImplantBoosterList,
               cascade='all, delete, delete-orphan',
               backref='set',
               single_parent=True,
               primaryjoin=Implants.implantsSetMap_table.c.setID == implant_set_table.c.ID,
               secondaryjoin=Implants.implantsSetMap_table.c.implantID == es_Implant.ID,
               secondary=Implants.implantsSetMap_table),
       }
       )
'''


class Miscdata(Base):
    __tablename__ = 'miscdata'
    fieldName = Column(String, primary_key=True)
    fieldValue = Column(String)


# mapper(es_MiscData, miscdata_table)


class Overrides(Base):
    __tablename__ = 'overrides'
    itemID = Column(Integer, primary_key=True, index=True)
    attrID = Column(Integer, primary_key=True, index=True)
    value = Column(Float, nullable=False)


# mapper(es_Override, overrides_table)


class Prices(Base):
    __tablename__ = 'prices'
    typeID = Column(Integer, primary_key=True)
    price = Column(Float)
    time = Column(Integer, nullable=False)
    failed = Column(Integer)


# mapper(es_Price, prices_table)


class CharacterSkills(Base):
    __tablename__ = 'characterSkills'
    characterID = Column(ForeignKey("characters.ID"), primary_key=True, index=True)
    itemID = Column(Integer, primary_key=True)
    _Skill__level = Column(Integer, nullable=True)


# mapper(es_Skill, skills_table)


class TargetResists(Base):
    __tablename__ = 'targetResists'
    ID = Column(Integer, primary_key=True)
    name = Column(String)
    emAmount = Column(Float)
    thermalAmount = Column(Float)
    kineticAmount = Column(Float)
    explosiveAmount = Column(Float)
    ownerID = Column(ForeignKey("users.ID"), nullable=True)


# mapper(es_TargetResists, targetResists_table)


class Users(Base):
    __tablename__ = 'users'
    ID = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    admin = Column(Boolean, nullable=False)


# mapper(es_User, users_table)


class DamagePatterns(Base):
    __tablename__ = 'damagePatterns'
    ID = Column(Integer, primary_key=True)
    name = Column(String)
    emAmount = Column(Integer)
    thermalAmount = Column(Integer)
    kineticAmount = Column(Integer)
    explosiveAmount = Column(Integer)
    ownerID = Column(ForeignKey("users.ID"), nullable=True)

# mapper(es_DamagePattern, damagePatterns_table)
