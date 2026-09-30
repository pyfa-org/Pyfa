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

from sqlalchemy import inspect
from sqlalchemy.orm import joinedload
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


def processEager(entity, eager):
    """
    Compatibility layer to accept strings as eager options
    """
    if eager is None:
        return tuple()

    if isinstance(eager, str):
        eager = (eager,)

    options = []
    for e in eager:
        option = None
        cls = entity
        for part in _replacements(e).split("."):
            if cls is None:
                raise ValueError("cannot resolve eager path {!r} on {}".format(e, entity))
            option = joinedload(getattr(cls, part)) if option is None else option.joinedload(getattr(cls, part))
            relationship = inspect(cls).relationships.get(part)
            cls = relationship.mapper.class_ if relationship is not None else None
        if option is not None:
            options.append(option)

    return options


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
