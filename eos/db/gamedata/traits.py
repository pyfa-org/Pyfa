
from sqlalchemy import Column, Table, Integer, Float, String, ForeignKey, and_, select
from sqlalchemy.orm import mapper, column_property
from eos.types import Item, Traits
from eos.db import gamedata_meta

traits_table = Table("invtraits", gamedata_meta,
                    Column("traitID", Integer, primary_key=True),
                    Column("typeID", Integer, ForeignKey("invtypes.typeID")),
                    Column("skillID", Integer, ForeignKey("invtypes.typeID")),
                    Column("bonus", Float),
                    Column("bonusText", String),
                    Column("unitID", Integer))
                    
                    
from .item import items_table
from .unit import groups_table
                    
mapper(Traits, traits_table,
        properties = {"skillName" : column_property( 
                                             select([items_table.c.typeName],
                                                and_(
                                                    items_table.c.typeID == traits_table.c.skillID,
                                                    traits_table.c.skillID != -1
                                                ))),
                      "unit" : column_property(
                                              select([groups_table.c.displayName],
                                                and_(
                                                    groups_table.c.unitID == traits_table.c.unitID
                                                )))
        });