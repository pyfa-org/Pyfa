
from sqlalchemy import Column, Table, Integer, String, ForeignKey, and_, select
from sqlalchemy.orm import mapper, column_property
from eos.types import Item, Traits
from eos.db import gamedata_meta

traits_table = Table("invtraits", gamedata_meta,
                     Column("typeID", Integer, ForeignKey("invtypes.typeID"), primary_key=True),
                     Column("skillID", Integer, ForeignKey("invtypes.typeID"), primary_key=True),
                     Column("bonusText", String, primary_key=True))


from .item import items_table

mapper(Traits, traits_table,
        properties = {"skillName" : column_property(
                                             select([items_table.c.typeName],
                                                and_(
                                                    items_table.c.typeID == traits_table.c.skillID,
                                                    traits_table.c.skillID != -1
                                                )))
        });
