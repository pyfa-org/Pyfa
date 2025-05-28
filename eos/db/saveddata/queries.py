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

import sys

from sqlalchemy.sql import and_
from sqlalchemy import desc, select
from sqlalchemy import func

from eos.db import saveddata_session, sd_lock
from eos.db.saveddata.fit import fits_table, projectedFits_table
from eos.db.util import processEager, processWhere
from eos.saveddata.price import Price
from eos.saveddata.user import User
from eos.saveddata.ssocharacter import SsoCharacter
from eos.saveddata.damagePattern import DamagePattern
from eos.saveddata.targetProfile import TargetProfile
from eos.saveddata.character import Character
from eos.saveddata.implantSet import ImplantSet
from eos.saveddata.fit import Fit, FitLite
from eos.saveddata.module import Module
from eos.saveddata.miscData import MiscData
from eos.saveddata.override import Override

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
                        # Some uncachable data, don't cache this query
                        del localQueryCache[cacheKey]
                        break
                    localItemCache[ID] = item
                    IDs.add(ID)

                return items

            def checkAndReturn(*args, **kwargs):
                useCache = kwargs.pop("useCache", True)
                cacheKey = []
                items = None
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
                                # Fuck, some of our stuff isn't cached it seems.
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
        if type not in queryCache:
            return
        functionCache = queryCache[type]
        for _, localCache in functionCache.items():
            toDelete = set()
            for cacheKey, info in localCache.items():
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
    elif isinstance(lookfor, str):
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
    elif isinstance(lookfor, str):
        eager = processEager(eager)
        with sd_lock:
            character = saveddata_session.query(Character).options(*eager).filter(
                    Character.savedName == lookfor).first()
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
                fit = saveddata_session.query(Fit).options(*eager).filter(Fit.ID == lookfor).first()
    else:
        raise TypeError("Need integer as argument")

    if fit and fit.isInvalid:
        with sd_lock:
            removeInvalid([fit])
        return None

    return fit


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
            fits = removeInvalid(saveddata_session.query(Fit).options(*eager).filter(filter).all())
    else:
        raise TypeError("ShipID must be integer")

    return fits


def getRecentFits(ownerID=None, where=None, eager=None):
    eager = processEager(eager)
    with sd_lock:
        q = select((
            Fit.ID,
            Fit.shipID,
            Fit.name,
            Fit.modified,
            Fit.created,
            Fit.timestamp,
            Fit.notes
        )).order_by(desc(Fit.modified), desc(Fit.timestamp)).limit(50)
        fits = eos.db.saveddata_session.execute(q).fetchall()

    return fits


def getFitsWithModules(typeIDs, eager=None):
    """
    Get all the fits that have typeIDs fitted to them
    """

    if not hasattr(typeIDs, "__iter__"):
        typeIDs = (typeIDs,)

    eager = processEager(eager)
    with sd_lock:
        fits = removeInvalid(saveddata_session.query(Fit).join(Module).options(*eager).filter(Module.itemID.in_(typeIDs)).all())

    return fits


def countAllFits():
    with sd_lock:
        count = saveddata_session.query(Fit).count()
    return count


def countFitGroupedByShip():
    with sd_lock:
        count = eos.db.saveddata_session.query(Fit.shipID, func.count(Fit.shipID)).group_by(Fit.shipID).all()
    return count


def countFitsWithShip(lookfor, ownerID=None, where=None, eager=None):
    """
    Get all the fits using a certain ship.
    If no user is passed, do this for all users.
    """
    if ownerID is not None and not isinstance(ownerID, int):
        raise TypeError("OwnerID must be integer")

    if isinstance(lookfor, int):
        filter = Fit.shipID == lookfor
    elif isinstance(lookfor, list):
        if len(lookfor) == 0:
            return 0
        filter = Fit.shipID.in_(lookfor)
    else:
        raise TypeError("You must supply either an integer or ShipID must be integer")

    if ownerID is not None:
        filter = and_(filter, Fit.ownerID == ownerID)

    filter = processWhere(filter, where)
    eager = processEager(eager)
    with sd_lock:
        count = saveddata_session.query(Fit).options(*eager).filter(filter).count()

    return count


def getFitList(eager=None):
    eager = processEager(eager)
    with sd_lock:
        fits = removeInvalid(saveddata_session.query(Fit).options(*eager).all())

    return fits


def getFitListLite():
    with sd_lock:
        stmt = select([fits_table.c.ID, fits_table.c.name, fits_table.c.shipID])
        data = eos.db.saveddata_session.execute(stmt).fetchall()
    fits = []
    for fitID, fitName, shipID in data:
        fit = FitLite(id=fitID, name=fitName, shipID=shipID)
        fits.append(fit)
    return fits


@cachedQuery(Price, 1, "typeID")
def getPrice(typeID):
    if isinstance(typeID, int):
        with sd_lock:
            price = saveddata_session.query(Price).get(typeID)
    else:
        raise TypeError("Need integer as argument")
    return price


def clearPrices():
    with sd_lock:
        deleted_rows = saveddata_session.query(Price).delete()
    commit()
    return deleted_rows


def getMiscData(field):
    if isinstance(field, str):
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


def clearDamagePatterns():
    with sd_lock:
        deleted_rows = saveddata_session.query(DamagePattern).filter(DamagePattern.name != 'Uniform').delete()
    commit()
    return deleted_rows


def getTargetProfileList(eager=None):
    eager = processEager(eager)
    with sd_lock:
        patterns = saveddata_session.query(TargetProfile).options(*eager).all()
    return patterns


def clearTargetProfiles():
    with sd_lock:
        deleted_rows = saveddata_session.query(TargetProfile).delete()
    commit()
    return deleted_rows


def getImplantSetList(eager=None):
    eager = processEager(eager)
    with sd_lock:
        sets = saveddata_session.query(ImplantSet).options(*eager).all()
    return sets


@cachedQuery(DamagePattern, 1, "lookfor")
def getDamagePattern(lookfor, eager=None):
    if isinstance(lookfor, int):
        if eager is None:
            with sd_lock:
                pattern = saveddata_session.query(DamagePattern).get(lookfor)
        else:
            eager = processEager(eager)
            with sd_lock:
                pattern = saveddata_session.query(DamagePattern).options(*eager).filter(
                        DamagePattern.ID == lookfor).first()
    elif isinstance(lookfor, str):
        eager = processEager(eager)
        with sd_lock:
            pattern = saveddata_session.query(DamagePattern).options(*eager).filter(
                    DamagePattern.rawName == lookfor).first()
    else:
        raise TypeError("Need integer or string as argument")
    return pattern


@cachedQuery(TargetProfile, 1, "lookfor")
def getTargetProfile(lookfor, eager=None):
    if isinstance(lookfor, int):
        if eager is None:
            with sd_lock:
                pattern = saveddata_session.query(TargetProfile).get(lookfor)
        else:
            eager = processEager(eager)
            with sd_lock:
                pattern = saveddata_session.query(TargetProfile).options(*eager).filter(
                    TargetProfile.ID == lookfor).first()
    elif isinstance(lookfor, str):
        eager = processEager(eager)
        with sd_lock:
            pattern = saveddata_session.query(TargetProfile).options(*eager).filter(
                TargetProfile.rawName == lookfor).first()
    else:
        raise TypeError("Need integer or string as argument")
    return pattern


@cachedQuery(ImplantSet, 1, "lookfor")
def getImplantSet(lookfor, eager=None):
    if isinstance(lookfor, int):
        if eager is None:
            with sd_lock:
                pattern = saveddata_session.query(ImplantSet).get(lookfor)
        else:
            eager = processEager(eager)
            with sd_lock:
                pattern = saveddata_session.query(ImplantSet).options(*eager).filter(
                    TargetProfile.ID == lookfor).first()
    elif isinstance(lookfor, str):
        eager = processEager(eager)
        with sd_lock:
            pattern = saveddata_session.query(ImplantSet).options(*eager).filter(TargetProfile.name == lookfor).first()
    else:
        raise TypeError("Improper argument")
    return pattern


def searchFits(nameLike, where=None, eager=None):
    if not isinstance(nameLike, str):
        raise TypeError("Need string as argument")
    # Prepare our string for request
    nameLike = "%{0}%".format(sqlizeString(nameLike))

    # Add any extra components to the search to our where clause
    filter = processWhere(Fit.name.like(nameLike, escape="\\"), where)
    eager = processEager(eager)
    with sd_lock:
        fits = removeInvalid(saveddata_session.query(Fit).options(*eager).filter(filter).limit(100).all())

    return fits


def getProjectedFits(fitID):
    if isinstance(fitID, int):
        with sd_lock:
            filter = and_(projectedFits_table.c.sourceID == fitID, Fit.ID == projectedFits_table.c.victimID)
            fits = saveddata_session.query(Fit).filter(filter).all()
            return fits
    else:
        raise TypeError("Need integer as argument")


def getSsoCharacters(clientHash, eager=None):
    eager = processEager(eager)
    with sd_lock:
        characters = saveddata_session.query(SsoCharacter).filter(SsoCharacter.client == clientHash).options(*eager).all()
    return characters


@cachedQuery(SsoCharacter, 1, "lookfor", "clientHash")
def getSsoCharacter(lookfor, clientHash, server=None, eager=None):
    filter = SsoCharacter.client == clientHash

    if server is not None:
        filter = and_(filter, SsoCharacter.server == server)

    if isinstance(lookfor, int):
        filter = and_(filter, SsoCharacter.ID == lookfor)
    elif isinstance(lookfor, str):
        filter = and_(filter, SsoCharacter.characterName == lookfor)
    else:
        raise TypeError("Need integer or string as argument")

    eager = processEager(eager)
    with sd_lock:
        character = saveddata_session.query(SsoCharacter).options(*eager).filter(filter).first()

    return character


def getOverrides(itemID, eager=None):
    if isinstance(itemID, int):
        return saveddata_session.query(Override).filter(Override.itemID == itemID).all()
    else:
        raise TypeError("Need integer as argument")


def clearOverrides():
    with sd_lock:
        deleted_rows = saveddata_session.query(Override).delete()
    commit()
    return deleted_rows


def getAllOverrides(eager=None):
    return saveddata_session.query(Override).all()


def removeInvalid(fits):
    invalids = [f for f in fits if f.isInvalid]

    if invalids:
        list(map(fits.remove, invalids))
        list(map(saveddata_session.delete, invalids))
        saveddata_session.commit()

    return fits


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
        try:
            saveddata_session.commit()
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception:
            saveddata_session.rollback()
            exc_info = sys.exc_info()
            raise exc_info[0](exc_info[1]).with_traceback(exc_info[2])


def flush():
    with sd_lock:
        try:
            saveddata_session.flush()
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception:
            saveddata_session.rollback()
            exc_info = sys.exc_info()
            raise exc_info[0](exc_info[1]).with_traceback(exc_info[2])
