from sqlalchemy import Column, Table, Integer, String, ForeignKey
from sqlalchemy.orm import synonym

from eos.db import gamedata_meta, mapper
from eos.gamedata import Traits
import eos.config

traits_table = Table(
    "invtraits",
    gamedata_meta,
    Column("typeID", Integer, ForeignKey("invtypes.typeID"), primary_key=True),
    *[Column("traitText{}".format(lang), String) for lang in eos.config.translation_mapping.values()],
)

mapper(
    Traits,
    traits_table,
    properties={
        "display": synonym("traitText{}".format(eos.config.lang)),
    }
)
