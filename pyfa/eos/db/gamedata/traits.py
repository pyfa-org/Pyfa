
from sqlalchemy import Column, Table, Integer, String, ForeignKey
from sqlalchemy.orm import mapper
from eos.types import Traits
from eos.db import gamedata_meta

traits_table = Table("invtraits", gamedata_meta,
                     Column("typeID", Integer, ForeignKey("invtypes.typeID"), primary_key=True),
                     Column("traitText", String))

mapper(Traits, traits_table);
