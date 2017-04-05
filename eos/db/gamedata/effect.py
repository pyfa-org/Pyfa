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

from sqlalchemy import Column, String, Integer, Boolean, Table, ForeignKey
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import mapper, synonym, relation, deferred

from eos.db import gamedata_meta
from eos.gamedata import Effect, EffectInfo

typeeffects_table = Table("dgmtypeeffects", gamedata_meta,
                          Column("typeID", Integer, ForeignKey("invtypes.typeID"), primary_key=True, index=True),
                          Column("effectID", Integer, ForeignKey("dgmeffects.effectID"), primary_key=True))

effects_table = Table("dgmeffects", gamedata_meta,
                      Column("effectID", Integer, primary_key=True),
                      Column("effectName", String),
                      Column("description", String),
                      Column("published", Boolean),
                      Column("isAssistance", Boolean),
                      Column("isOffensive", Boolean))

mapper(EffectInfo, effects_table,
       properties={
           "ID"         : synonym("effectID"),
           "name"       : synonym("effectName"),
           "description": deferred(effects_table.c.description)
       })

mapper(Effect, typeeffects_table,
       properties={
           "ID"  : synonym("effectID"),
           "info": relation(EffectInfo, lazy=False)
       })

Effect.name = association_proxy("info", "name")
Effect.description = association_proxy("info", "description")
Effect.published = association_proxy("info", "published")
