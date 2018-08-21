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

from sqlalchemy.orm import eagerload
from sqlalchemy.sql import and_

replace = {
    "attributes"      : "_Item__attributes",
    "modules"         : "_Fit__modules",
    "projectedModules": "_Fit__projectedModules",
    "boosters"        : "_Fit__boosters",
    "drones"          : "_Fit__drones",
    "projectedDrones" : "_Fit__projectedDrones",
    "implants"        : "_Fit__implants",
    "character"       : "_Fit__character",
    "damagePattern"   : "_Fit__damagePattern",
    "projectedFits"   : "_Fit__projectedFits"
}


def processEager(eager):
    if eager is None:
        return tuple()
    else:
        l = []
        if isinstance(eager, str):
            eager = (eager,)

        for e in eager:
            l.append(eagerload(_replacements(e)))

        return l


def _replacements(eagerString):
    splitEager = eagerString.split(".")
    for i in range(len(splitEager)):
        part = splitEager[i]
        replacement = replace.get(part)
        if replacement:
            splitEager[i] = replacement

    return ".".join(splitEager)


def processWhere(clause, where):
    if where is not None:
        if not hasattr(where, "__iter__"):
            where = (where,)

        try:
            for extraClause in where:
                clause = and_(clause, extraClause)
        except NotImplementedError:
            clause = and_(clause, where)

    return clause
