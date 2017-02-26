# ===============================================================================
# Copyright (C) 2011 Anton Vorobyov
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

from sqlalchemy import Column, Table, String
from sqlalchemy.orm import mapper

from eos.db import saveddata_meta
from eos.saveddata.miscData import MiscData

miscdata_table = Table("miscdata", saveddata_meta,
                       Column("fieldName", String, primary_key=True),
                       Column("fieldValue", String))

mapper(MiscData, miscdata_table)
