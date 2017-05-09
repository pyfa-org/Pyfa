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

from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.sql import and_
from sqlalchemy.orm import relation, reconstructor, mapper, relationship
from sqlalchemy import ForeignKey, Column, Integer, String, Table, Boolean, DateTime
import datetime

from eos.db import saveddata_meta
from eos.db import saveddata_session
from eos.db.saveddata.cargo import cargo_table
from eos.db.saveddata.drone import drones_table
from eos.db.saveddata.fighter import fighters_table
from eos.db.saveddata.implant import fitImplants_table
from eos.db.saveddata.module import modules_table
from eos.effectHandlerHelpers import HandledModuleList, HandledImplantBoosterList, HandledProjectedModList, \
    HandledDroneCargoList, HandledProjectedDroneList
from eos.saveddata.implant import Implant
from eos.saveddata.character import Character
from eos.saveddata.user import User
from eos.saveddata.fighter import Fighter
from eos.saveddata.fit import Fit as es_Fit, ImplantLocation
from eos.saveddata.drone import Drone
from eos.saveddata.booster import Booster
from eos.saveddata.module import Module
from eos.saveddata.cargo import Cargo
from eos.saveddata.damagePattern import DamagePattern
from eos.saveddata.targetResists import TargetResists

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
                   Column("implantLocation", Integer, nullable=False, default=ImplantLocation.FIT),
                   Column("notes", String, nullable=True),
                   Column("ignoreRestrictions", Boolean, default=0),
                   Column("created", DateTime, nullable=True, default=datetime.datetime.now),
                   Column("modified", DateTime, nullable=True, default=datetime.datetime.now, onupdate=datetime.datetime.now)
                   )

projectedFits_table = Table("projectedFits", saveddata_meta,
                            Column("sourceID", ForeignKey("fits.ID"), primary_key=True),
                            Column("victimID", ForeignKey("fits.ID"), primary_key=True),
                            Column("amount", Integer, nullable=False, default=1),
                            Column("active", Boolean, nullable=False, default=1),
                            Column("created", DateTime, nullable=True, default=datetime.datetime.now),
                            Column("modified", DateTime, nullable=True, onupdate=datetime.datetime.now)
                            )

commandFits_table = Table("commandFits", saveddata_meta,
                          Column("boosterID", ForeignKey("fits.ID"), primary_key=True),
                          Column("boostedID", ForeignKey("fits.ID"), primary_key=True),
                          Column("active", Boolean, nullable=False, default=1),
                          Column("created", DateTime, nullable=True, default=datetime.datetime.now),
                          Column("modified", DateTime, nullable=True, onupdate=datetime.datetime.now)
                          )


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


# These relationships are broken out so that we can easily access it in the events stuff
# We sometimes don't want particular relationships to cause a fit modified update (eg: projecting
# a fit onto another would 'modify' both fits unless the following relationship is ignored)
projectedFitSourceRel = relationship(
   ProjectedFit,
   primaryjoin=projectedFits_table.c.sourceID == fits_table.c.ID,
   backref='source_fit',
   collection_class=attribute_mapped_collection('victimID'),
   cascade='all, delete, delete-orphan')


boostedOntoRel = relationship(
   CommandFit,
   primaryjoin=commandFits_table.c.boosterID == fits_table.c.ID,
   backref='booster_fit',
   collection_class=attribute_mapped_collection('boostedID'),
   cascade='all, delete, delete-orphan')

mapper(es_Fit, fits_table,
       properties={
           "_Fit__modules": relation(
                   Module,
                   collection_class=HandledModuleList,
                   primaryjoin=and_(modules_table.c.fitID == fits_table.c.ID, modules_table.c.projected == False),  # noqa
                   order_by=modules_table.c.position,
                   cascade='all, delete, delete-orphan'),
           "_Fit__projectedModules": relation(
                   Module,
                   collection_class=HandledProjectedModList,
                   cascade='all, delete, delete-orphan',
                   single_parent=True,
                   primaryjoin=and_(modules_table.c.fitID == fits_table.c.ID, modules_table.c.projected == True)),  # noqa
           "owner": relation(
                   User,
                   backref="fits"),
           "itemID": fits_table.c.shipID,
           "shipID": fits_table.c.shipID,
           "_Fit__boosters": relation(
                   Booster,
                   collection_class=HandledImplantBoosterList,
                   cascade='all, delete, delete-orphan',
                   backref='owner',
                   single_parent=True),
           "_Fit__drones": relation(
                   Drone,
                   collection_class=HandledDroneCargoList,
                   cascade='all, delete, delete-orphan',
                   single_parent=True,
                   primaryjoin=and_(drones_table.c.fitID == fits_table.c.ID, drones_table.c.projected == False)),  # noqa
           "_Fit__fighters": relation(
                   Fighter,
                   collection_class=HandledDroneCargoList,
                   cascade='all, delete, delete-orphan',
                   single_parent=True,
                   primaryjoin=and_(fighters_table.c.fitID == fits_table.c.ID, fighters_table.c.projected == False)),  # noqa
           "_Fit__cargo": relation(
                   Cargo,
                   collection_class=HandledDroneCargoList,
                   cascade='all, delete, delete-orphan',
                   single_parent=True,
                   primaryjoin=and_(cargo_table.c.fitID == fits_table.c.ID)),
           "_Fit__projectedDrones": relation(
                   Drone,
                   collection_class=HandledProjectedDroneList,
                   cascade='all, delete, delete-orphan',
                   single_parent=True,
                   primaryjoin=and_(drones_table.c.fitID == fits_table.c.ID, drones_table.c.projected == True)),  # noqa
           "_Fit__projectedFighters": relation(
                   Fighter,
                   collection_class=HandledProjectedDroneList,
                   cascade='all, delete, delete-orphan',
                   single_parent=True,
                   primaryjoin=and_(fighters_table.c.fitID == fits_table.c.ID, fighters_table.c.projected == True)),  # noqa
           "_Fit__implants": relation(
                   Implant,
                   collection_class=HandledImplantBoosterList,
                   cascade='all, delete, delete-orphan',
                   backref='owner',
                   single_parent=True,
                   primaryjoin=fitImplants_table.c.fitID == fits_table.c.ID,
                   secondaryjoin=fitImplants_table.c.implantID == Implant.ID,
                   secondary=fitImplants_table),
           "_Fit__character": relation(
                   Character,
                   backref="fits"),
           "_Fit__damagePattern": relation(DamagePattern),
           "_Fit__targetResists": relation(TargetResists),
           "projectedOnto": projectedFitSourceRel,
           "victimOf": relationship(
                   ProjectedFit,
                   primaryjoin=fits_table.c.ID == projectedFits_table.c.victimID,
                   backref='victim_fit',
                   collection_class=attribute_mapped_collection('sourceID'),
                   cascade='all, delete, delete-orphan'),
           "boostedOnto": boostedOntoRel,
           "boostedOf": relationship(
                   CommandFit,
                   primaryjoin=fits_table.c.ID == commandFits_table.c.boostedID,
                   backref='boosted_fit',
                   collection_class=attribute_mapped_collection('boosterID'),
                   cascade='all, delete, delete-orphan'),
       }
)

mapper(ProjectedFit, projectedFits_table,
   properties={
       "_ProjectedFit__amount": projectedFits_table.c.amount,
   }
)

mapper(CommandFit, commandFits_table)
