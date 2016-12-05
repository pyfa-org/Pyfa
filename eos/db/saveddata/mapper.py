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


from sqlalchemy import CheckConstraint
from sqlalchemy import Float
from sqlalchemy import ForeignKey, Boolean
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import reconstructor, relationship
from sqlalchemy.orm import relation, mapper
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.sql import and_

import eos.saveddata.character as Character
from eos.db import saveddata_meta
from eos.db import saveddata_session
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


class Modules:
    modules_table = Table("modules", saveddata_meta,
                          Column("ID", Integer, primary_key=True),
                          Column("fitID", Integer, ForeignKey("fits.ID"), nullable=False, index=True),
                          Column("itemID", Integer, nullable=True),
                          Column("dummySlot", Integer, nullable=True, default=None),
                          Column("chargeID", Integer),
                          Column("state", Integer, CheckConstraint("state >= -1"), CheckConstraint("state <= 2")),
                          Column("projected", Boolean, default=False, nullable=False),
                          Column("position", Integer),
                          CheckConstraint('("dummySlot" = NULL OR "itemID" = NULL) AND "dummySlot" != "itemID"'))

    mapper(es_Module, modules_table,
           properties={"owner": relation(es_Fit)})


class Boosters:
    boosters_table = Table("boosters", saveddata_meta,
                           Column("ID", Integer, primary_key=True),
                           Column("itemID", Integer),
                           Column("fitID", Integer, ForeignKey("fits.ID"), nullable=False),
                           Column("active", Boolean),
                           )

    # Legacy booster side effect code, should disable but a mapper relies on it.
    activeSideEffects_table = Table("boostersActiveSideEffects", saveddata_meta,
                                    Column("boosterID", ForeignKey("boosters.ID"), primary_key=True),
                                    Column("effectID", Integer, primary_key=True))

    class ActiveSideEffectsDummy(object):
        def __init__(self, effectID):
            self.effectID = effectID

    mapper(ActiveSideEffectsDummy, activeSideEffects_table)
    mapper(es_Booster, boosters_table,
           properties={"_Booster__activeSideEffectDummies": relation(ActiveSideEffectsDummy)})

    es_Booster._Booster__activeSideEffectIDs = association_proxy("_Booster__activeSideEffectDummies", "effectID")


class Cargo:
    cargo_table = Table("cargo", saveddata_meta,
                        Column("ID", Integer, primary_key=True),
                        Column("fitID", Integer, ForeignKey("fits.ID"), nullable=False, index=True),
                        Column("itemID", Integer, nullable=False),
                        Column("amount", Integer, nullable=False))

    mapper(es_Cargo, cargo_table)


class Implants:
    implants_table = Table("implants", saveddata_meta,
                           Column("ID", Integer, primary_key=True),
                           Column("itemID", Integer),
                           Column("active", Boolean))

    fitImplants_table = Table("fitImplants", saveddata_meta,
                              Column("fitID", ForeignKey("fits.ID"), index=True),
                              Column("implantID", ForeignKey("implants.ID"), primary_key=True))

    charImplants_table = Table("charImplants", saveddata_meta,
                               Column("charID", ForeignKey("characters.ID"), index=True),
                               Column("implantID", ForeignKey("implants.ID"), primary_key=True))

    implantsSetMap_table = Table("implantSetMap", saveddata_meta,
                                 Column("setID", ForeignKey("implantSets.ID"), index=True),
                                 Column("implantID", ForeignKey("implants.ID"), primary_key=True))

    mapper(es_Implant, implants_table)


class Characters:
    characters_table = Table("characters", saveddata_meta,
                             Column("ID", Integer, primary_key=True),
                             Column("name", String, nullable=False),
                             Column("apiID", Integer),
                             Column("apiKey", String),
                             Column("defaultChar", Integer),
                             Column("chars", String, nullable=True),
                             Column("defaultLevel", Integer, nullable=True),
                             Column("ownerID", ForeignKey("users.ID"), nullable=True))

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


class Crest:
    crest_table = Table("crest", saveddata_meta,
                        Column("ID", Integer, primary_key=True),
                        Column("name", String, nullable=False, unique=True),
                        Column("refresh_token", String, nullable=False))

    mapper(es_CrestChar, crest_table)


class Drones:
    drones_table = Table("drones", saveddata_meta,
                         Column("groupID", Integer, primary_key=True),
                         Column("fitID", Integer, ForeignKey("fits.ID"), nullable=False, index=True),
                         Column("itemID", Integer, nullable=False),
                         Column("amount", Integer, nullable=False),
                         Column("amountActive", Integer, nullable=False),
                         Column("projected", Boolean, default=False))

    mapper(es_Drone, drones_table)


class Fighters:
    fighters_table = Table("fighters", saveddata_meta,
                           Column("groupID", Integer, primary_key=True),
                           Column("fitID", Integer, ForeignKey("fits.ID"), nullable=False, index=True),
                           Column("itemID", Integer, nullable=False),
                           Column("active", Boolean, nullable=True),
                           Column("amount", Integer, nullable=False),
                           Column("projected", Boolean, default=False))

    fighter_abilities_table = Table("fightersAbilities", saveddata_meta,
                                    Column("groupID", Integer, ForeignKey("fighters.groupID"), primary_key=True,
                                           index=True),
                                    Column("effectID", Integer, nullable=False, primary_key=True),
                                    Column("active", Boolean, default=False))

    mapper(es_Fighter, fighters_table,
           properties={
               "owner": relation(es_Fit),
               "_Fighter__abilities": relation(
                   es_FighterAbility,
                   backref="fighter",
                   cascade='all, delete, delete-orphan'),
           })

    mapper(es_FighterAbility, fighter_abilities_table)


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


class Fits:
    fits_table = Table("fits", saveddata_meta,
                       Column("ID", Integer, primary_key=True),
                       Column("ownerID", ForeignKey("users.ID"), nullable=True, index=True),
                       Column("shipID", Integer, nullable=False, index=True),
                       Column("name", String, nullable=False),
                       Column("timestamp", Integer, nullable=False),
                       Column("characterID", ForeignKey("characters.ID"), nullable=True),
                       Column("damagePatternID", ForeignKey("damagePatterns.ID"), nullable=True),
                       Column("booster", Boolean, nullable=False, index=True, default=0),
                       Column("targetResistsID", ForeignKey("targetResists.ID"), nullable=True),
                       Column("modeID", Integer, nullable=True),
                       Column("implantLocation", Integer, nullable=False, default=es_ImplantLocation.FIT),
                       Column("notes", String, nullable=True),
                       )

    projectedFits_table = Table("projectedFits", saveddata_meta,
                                Column("sourceID", ForeignKey("fits.ID"), primary_key=True),
                                Column("victimID", ForeignKey("fits.ID"), primary_key=True),
                                Column("amount", Integer, nullable=False, default=1),
                                Column("active", Boolean, nullable=False, default=1),
                                )

    commandFits_table = Table("commandFits", saveddata_meta,
                              Column("boosterID", ForeignKey("fits.ID"), primary_key=True),
                              Column("boostedID", ForeignKey("fits.ID"), primary_key=True),
                              Column("active", Boolean, nullable=False, default=1)
                              )

    es_Fit._Fit__projectedFits = association_proxy(
        "victimOf",  # look at the victimOf association...
        "source_fit",  # .. and return the source fits
        creator=lambda sourceID, source_fit: ProjectedFit(sourceID, source_fit)
    )

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


class Fleet:
    gangs_table = Table("gangs", saveddata_meta,
                        Column("ID", Integer, primary_key=True),
                        Column("leaderID", ForeignKey("fits.ID")),
                        Column("boosterID", ForeignKey("fits.ID")),
                        Column("name", String))

    wings_table = Table("wings", saveddata_meta,
                        Column("ID", Integer, primary_key=True),
                        Column("gangID", ForeignKey("gangs.ID")),
                        Column("boosterID", ForeignKey("fits.ID")),
                        Column("leaderID", ForeignKey("fits.ID")))

    squads_table = Table("squads", saveddata_meta,
                         Column("ID", Integer, primary_key=True),
                         Column("wingID", ForeignKey("wings.ID")),
                         Column("leaderID", ForeignKey("fits.ID")),
                         Column("boosterID", ForeignKey("fits.ID")))

    squadmembers_table = Table("squadmembers", saveddata_meta,
                               Column("squadID", ForeignKey("squads.ID"), primary_key=True),
                               Column("memberID", ForeignKey("fits.ID"), primary_key=True))
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


class Implant_set:
    implant_set_table = Table("implantSets", saveddata_meta,
                              Column("ID", Integer, primary_key=True),
                              Column("name", String, nullable=False),
                              )

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


class Miscdata:
    miscdata_table = Table("miscdata", saveddata_meta,
                           Column("fieldName", String, primary_key=True),
                           Column("fieldValue", String))

    mapper(es_MiscData, miscdata_table)


class Overrides:
    overrides_table = Table("overrides", saveddata_meta,
                            Column("itemID", Integer, primary_key=True, index=True),
                            Column("attrID", Integer, primary_key=True, index=True),
                            Column("value", Float, nullable=False))

    mapper(es_Override, overrides_table)


class Prices:
    prices_table = Table("prices", saveddata_meta,
                         Column("typeID", Integer, primary_key=True),
                         Column("price", Float),
                         Column("time", Integer, nullable=False),
                         Column("failed", Integer))

    mapper(es_Price, prices_table)


class Skills:
    skills_table = Table("characterSkills", saveddata_meta,
                         Column("characterID", ForeignKey("characters.ID"), primary_key=True, index=True),
                         Column("itemID", Integer, primary_key=True),
                         Column("_Skill__level", Integer, nullable=True))

    mapper(es_Skill, skills_table)


class TargetResists:
    targetResists_table = Table("targetResists", saveddata_meta,
                                Column("ID", Integer, primary_key=True),
                                Column("name", String),
                                Column("emAmount", Float),
                                Column("thermalAmount", Float),
                                Column("kineticAmount", Float),
                                Column("explosiveAmount", Float),
                                Column("ownerID", ForeignKey("users.ID"), nullable=True))

    mapper(es_TargetResists, targetResists_table)


class Users:
    users_table = Table("users", saveddata_meta,
                        Column("ID", Integer, primary_key=True),
                        Column("username", String, nullable=False, unique=True),
                        Column("password", String, nullable=False),
                        Column("admin", Boolean, nullable=False))

    mapper(es_User, users_table)


class DamagePatterns:
    damagePatterns_table = Table("damagePatterns", saveddata_meta,
                                 Column("ID", Integer, primary_key=True),
                                 Column("name", String),
                                 Column("emAmount", Integer),
                                 Column("thermalAmount", Integer),
                                 Column("kineticAmount", Integer),
                                 Column("explosiveAmount", Integer),
                                 Column("ownerID", ForeignKey("users.ID"), nullable=True))

    mapper(es_DamagePattern, damagePatterns_table)
