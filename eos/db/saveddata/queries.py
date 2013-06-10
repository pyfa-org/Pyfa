#===============================================================================
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
#===============================================================================

from eos.db.util import processEager, processWhere
from eos.db import saveddata_session, sd_lock
from eos.types import User, Character, Fit, Price, DamagePattern, Fleet, MiscData, Wing, Squad
from eos.db.saveddata.fleet import squadmembers_table
from sqlalchemy.sql import and_
import eos.config

configVal = getattr(eos.config, "saveddataCache", None)
if configVal is True:
    import weakref
    itemCache = {}
    queryCache = {}
    def cachedQuery(type, amount, *keywords):
        itemCache[type] = localItemCache = weakref.WeakValueDictionary()
        queryCache[type] = typeQueryCache = {}
        def deco(function):
            localQueryCache = typeQueryCache[function] = {}
            def setCache(cacheKey, args, kwargs):
                items = function(*args, **kwargs)
                IDs = set()
                localQueryCache[cacheKey] = (isinstance(items, list), IDs)
                stuff = items if isinstance(items, list) else (items,)
                for item in stuff:
                    ID = getattr(item, "ID", None)
                    if ID is None:
                        #Some uncachable data, don't cache this query
                        del localQueryCache[cacheKey]
                        break
                    localItemCache[ID] = item
                    IDs.add(ID)

                return items

            def checkAndReturn(*args, **kwargs):
                useCache = kwargs.pop("useCache", True)
                cacheKey = []
                cacheKey.extend(args)
                for keyword in keywords:
                    cacheKey.append(kwargs.get(keyword))

                cacheKey = tuple(cacheKey)
                info = localQueryCache.get(cacheKey)
                if info is None or not useCache:
                    items = setCache(cacheKey, args, kwargs)
                else:
                    l, IDs = info
                    if l:
                        items = []
                        for ID in IDs:
                            data = localItemCache.get(ID)
                            if data is None:
                                #Fuck, some of our stuff isn't cached it seems.
                                items = setCache(cacheKey, args, kwargs)
                                break
                            items.append(data)
                    else:
                        for ID in IDs:
                            items = localItemCache.get(ID)
                            if items is None:
                                items = setCache(cacheKey, args, kwargs)
                            break

                return items
            return checkAndReturn
        return deco

    def removeCachedEntry(type, ID):
        if not type in queryCache:
            return
        functionCache = queryCache[type]
        for _, localCache in functionCache.iteritems():
            toDelete = set()
            for cacheKey, info in localCache.iteritems():
                IDs = info[1]
                if ID in IDs:
                    toDelete.add(cacheKey)

            for cacheKey in toDelete:
                del localCache[cacheKey]

            if ID in itemCache[type]:
                del itemCache[type][ID]

elif callable(configVal):
    cachedQuery, removeCachedEntry = eos.config.gamedataCache
else:
    def cachedQuery(amount, *keywords):
        def deco(function):
            def checkAndReturn(*args, **kwargs):
                return function(*args, **kwargs)

            return checkAndReturn
        return deco

    def removeCachedEntry(*args, **kwargs):
        return

def sqlizeString(line):
    # Escape backslashes first, as they will be as escape symbol in queries
    # Then escape percent and underscore signs
    # Finally, replace generic wildcards with sql-style wildcards
    line = line.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_").replace("*", "%")
    return line

@cachedQuery(User, 1, "lookfor")
def getUser(lookfor, eager=None):
    if isinstance(lookfor, int):
        if eager is None:
            with sd_lock:
                user = saveddata_session.query(User).get(lookfor)
        else:
            eager = processEager(eager)
            with sd_lock:
                user = saveddata_session.query(User).options(*eager).filter(User.ID == lookfor).first()
    elif isinstance(lookfor, basestring):
        eager = processEager(eager)
        with sd_lock:
            user = saveddata_session.query(User).options(*eager).filter(User.username == lookfor).first()
    else:
        raise TypeError("Need integer or string as argument")
    return user

@cachedQuery(Character, 1, "lookfor")
def getCharacter(lookfor, eager=None):
    if isinstance(lookfor, int):
        if eager is None:
            with sd_lock:
                character = saveddata_session.query(Character).get(lookfor)
        else:
            eager = processEager(eager)
            with sd_lock:
                character = saveddata_session.query(Character).options(*eager).filter(Character.ID == lookfor).first()
    elif isinstance(lookfor, basestring):
        eager = processEager(eager)
        with sd_lock:
            character = saveddata_session.query(Character).options(*eager).filter(Character.name == lookfor).first()
    else:
        raise TypeError("Need integer or string as argument")
    return character

def getCharacterList(eager=None):
    eager = processEager(eager)
    with sd_lock:
        characters = saveddata_session.query(Character).options(*eager).all()
    return characters

def getCharactersForUser(lookfor, eager=None):
    if isinstance(lookfor, int):
        eager = processEager(eager)
        with sd_lock:
            characters = saveddata_session.query(Character).options(*eager).filter(Character.ownerID == lookfor).all()
    else:
        raise TypeError("Need integer as argument")
    return characters

@cachedQuery(Fit, 1, "lookfor")
def getFit(lookfor, eager=None):
    if isinstance(lookfor, int):
        if eager is None:
            with sd_lock:
                fit = saveddata_session.query(Fit).get(lookfor)
        else:
            eager = processEager(eager)
            with sd_lock:
                fit = saveddata_session.query(Fit).options(*eager).filter(Fit.ID == fitID).first()
    else:
        raise TypeError("Need integer as argument")
    return fit

@cachedQuery(Fleet, 1, "fleetID")
def getFleet(fleetID, eager=None):
    if isinstance(fleetID, int):
        if eager is None:
            with sd_lock:
                fleet = saveddata_session.query(Fleet).get(fleetID)
        else:
            eager = processEager(eager)
            with sd_lock:
                fleet = saveddata_session.query(Fleet).options(*eager).filter(Fleet.ID == fleetID).first()
    else:
        raise TypeError("Need integer as argument")
    return fleet

@cachedQuery(Wing, 1, "wingID")
def getWing(wingID, eager=None):
    if isinstance(wingID, int):
        if eager is None:
            with sd_lock:
                wing = saveddata_session.query(Wing).get(wingID)
        else:
            eager = processEager(eager)
            with sd_lock:
                wing = saveddata_session.query(Wing).options(*eager).filter(Wing.ID == wingID).first()
    else:
        raise TypeError("Need integer as argument")
    return wing

@cachedQuery(Squad, 1, "squadID")
def getSquad(squadID, eager=None):
    if isinstance(squadID, int):
        if eager is None:
            with sd_lock:
                squad = saveddata_session.query(Squad).get(squadID)
        else:
            eager = processEager(eager)
            with sd_lock:
                squad = saveddata_session.query(Squad).options(*eager).filter(Fleet.ID == squadID).first()
    else:
        raise TypeError("Need integer as argument")
    return squad

def getFitsWithShip(shipID, ownerID=None, where=None, eager=None):
    """
    Get all the fits using a certain ship.
    If no user is passed, do this for all users.
    """
    if isinstance(shipID, int):
        if ownerID is not None and not isinstance(ownerID, int):
            raise TypeError("OwnerID must be integer")
        filter = Fit.shipID == shipID
        if ownerID is not None:
            filter = and_(filter, Fit.ownerID == ownerID)

        filter = processWhere(filter, where)
        eager = processEager(eager)
        with sd_lock:
            fits = saveddata_session.query(Fit).options(*eager).filter(filter).all()
    else:
        raise TypeError("ShipID must be integer")
    return fits

def countFitsWithShip(shipID, ownerID=None, where=None, eager=None):
    """
    Get all the fits using a certain ship.
    If no user is passed, do this for all users.
    """
    if isinstance(shipID, int):
        if ownerID is not None and not isinstance(ownerID, int):
            raise TypeError("OwnerID must be integer")
        filter = Fit.shipID == shipID
        if ownerID is not None:
            filter = and_(filter, Fit.ownerID == ownerID)

        filter = processWhere(filter, where)
        eager = processEager(eager)
        with sd_lock:
            count = saveddata_session.query(Fit).options(*eager).filter(filter).count()
    else:
        raise TypeError("ShipID must be integer")
    return count

def getFitList(eager=None):
    eager = processEager(eager)
    with sd_lock:
        fits = saveddata_session.query(Fit).options(*eager).all()
    return fits

def getFleetList(eager=None):
    eager = processEager(eager)
    with sd_lock:
        fleets = saveddata_session.query(Fleet).options(*eager).all()
    return fleets

@cachedQuery(Price, 1, "typeID")
def getPrice(typeID):
    if isinstance(typeID, int):
        with sd_lock:
            price = saveddata_session.query(Price).get(typeID)
    else:
        raise TypeError("Need integer as argument")
    return price

def getMiscData(field):
    if isinstance(field, basestring):
        with sd_lock:
            data = saveddata_session.query(MiscData).get(field)
    else:
        raise TypeError("Need string as argument")
    return data

def getDamagePatternList(eager=None):
    eager = processEager(eager)
    with sd_lock:
        patterns = saveddata_session.query(DamagePattern).options(*eager).all()
    return patterns

@cachedQuery(DamagePattern, 1, "lookfor")
def getDamagePattern(lookfor, eager=None):
    if isinstance(lookfor, int):
        if eager is None:
            with sd_lock:
                pattern = saveddata_session.query(DamagePattern).get(lookfor)
        else:
            eager = processEager(eager)
            with sd_lock:
                pattern = saveddata_session.query(DamagePattern).options(*eager).filter(DamagePattern.ID == lookfor).first()
    elif isinstance(lookfor, basestring):
        eager = processEager(eager)
        with sd_lock:
            pattern = saveddata_session.query(DamagePattern).options(*eager).filter(DamagePattern.name == lookfor).first()
    else:
        raise TypeError("Need integer or string as argument")
    return pattern

def searchFits(nameLike, where=None, eager=None):
    if not isinstance(nameLike, basestring):
        raise TypeError("Need string as argument")
    # Prepare our string for request
    nameLike = u"%{0}%".format(sqlizeString(nameLike))

    #Add any extra components to the search to our where clause
    filter = processWhere(Fit.name.like(nameLike, escape="\\"), where)
    eager = processEager(eager)
    with sd_lock:
        fits = saveddata_session.query(Fit).options(*eager).filter(filter).all()
    return fits

def getSquadsIDsWithFitID(fitID):
    if isinstance(fitID, int):
        with sd_lock:
            squads = saveddata_session.query(squadmembers_table.c.squadID).filter(squadmembers_table.c.memberID == fitID).all()
            squads = tuple(entry[0] for entry in squads)
            return squads
    else:
        raise TypeError("Need integer as argument")


def add(stuff):
    with sd_lock:
        saveddata_session.add(stuff)

def save(stuff):
    add(stuff)
    commit()

def remove(stuff):
    removeCachedEntry(type(stuff), stuff.ID)
    with sd_lock:
        saveddata_session.delete(stuff)
    commit()


def commit():
    with sd_lock:
        saveddata_session.commit()
        saveddata_session.flush()
