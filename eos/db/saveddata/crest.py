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

from sqlalchemy import Table, Column, Integer, String, DateTime
from sqlalchemy.orm import mapper
import datetime

from eos.db import saveddata_meta
from eos.saveddata.crestchar import CrestChar

crest_table = Table("crest", saveddata_meta,
                    Column("ID", Integer, primary_key=True),
                    Column("name", String, nullable=False, unique=True),
                    Column("refresh_token", String, nullable=False),
                    # These records aren't updated. Instead, they are dropped and created, hence we don't have a modified field
                    Column("created", DateTime, nullable=True, default=datetime.datetime.now))

mapper(CrestChar, crest_table)
