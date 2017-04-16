from sqlalchemy import Column, Table, Integer, String, ForeignKey
from sqlalchemy.orm import mapper

from eos.db import gamedata_meta
from eos.gamedata import Traits

traits_table = Table("invtraits", gamedata_meta,
                     Column("typeID", Integer, ForeignKey("invtypes.typeID"), primary_key=True),
                     Column("traitText", String))

mapper(Traits, traits_table)
