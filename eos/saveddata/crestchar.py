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

from sqlalchemy.orm import reconstructor, mapper

from eos.db.sqlAlchemy import sqlAlchemy
from eos.db.saveddata.queries import cachedQuery
from eos.db.util import processEager
from eos.db.saveddata.mapper import Crest as crest_table


class CrestChar(object):
    def __init__(self, id, name, refresh_token=None):
        self.ID = id
        self.name = name
        self.refresh_token = refresh_token

        mapper(CrestChar, crest_table)

    @reconstructor
    def init(self):
        pass

    '''
    @threads(1)
    def fetchImage(self):
        url = 'https://image.eveonline.com/character/%d_128.jpg'%self.ID
        fp = urllib.urlopen(url)
        data = fp.read()
        fp.close()
        self.img = StringIO(data)
    '''


def getCrestCharacters(eager=None):
    eager = processEager(eager)
    with sqlAlchemy.sd_lock:
        characters = sqlAlchemy.saveddata_session.query(CrestChar).options(*eager).all()
    return characters


@cachedQuery(CrestChar, 1, "lookfor")
def getCrestCharacter(lookfor, eager=None):
    if isinstance(lookfor, int):
        if eager is None:
            with sqlAlchemy.sd_lock:
                character = sqlAlchemy.saveddata_session.query(CrestChar).get(lookfor)
        else:
            eager = processEager(eager)
            with sqlAlchemy.sd_lock:
                character = sqlAlchemy.saveddata_session.query(CrestChar).options(*eager).filter(CrestChar.ID == lookfor).first()
    elif isinstance(lookfor, basestring):
        eager = processEager(eager)
        with sqlAlchemy.sd_lock:
            character = sqlAlchemy.saveddata_session.query(CrestChar).options(*eager).filter(CrestChar.name == lookfor).first()
    else:
        raise TypeError("Need integer or string as argument")
    return character
