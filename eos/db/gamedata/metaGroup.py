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

from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orm import mapper, synonym

from eos.db import gamedata_meta
from eos.gamedata import MetaGroup
import eos.config

metagroups_table = Table(
    "invmetagroups",
    gamedata_meta,
    Column("metaGroupID", Integer, primary_key=True),
    *[Column("metaGroupName{}".format(lang), String) for lang in eos.config.translation_mapping.values()],
)

mapper(
    MetaGroup,
    metagroups_table,
    properties={
        "ID"  : synonym("metaGroupID"),
        "name": synonym("metaGroupName{}".format(eos.config.lang))
    }
)
