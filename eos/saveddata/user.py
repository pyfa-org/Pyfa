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

import hashlib
import random
import string
from sqlalchemy.orm import mapper

from sqlalchemy.orm import validates

from eos.db.sqlAlchemy import sqlAlchemy
from eos.db.saveddata.queries import cachedQuery
from eos.db.util import processEager
from eos.db.saveddata.mapper import Users as users_table


class User(object):
    def __init__(self, username, password=None, admin=False):
        self.username = username
        if password is not None:
            self.encodeAndSetPassword(password)
        self.admin = admin

        mapper(User, users_table)

    def encodeAndSetPassword(self, pw):
        h = hashlib.new("sha256")
        salt = "".join([random.choice(string.letters) for _ in xrange(32)])
        h.update(pw)
        h.update(salt)
        self.password = ("%s%s" % (h.hexdigest(), salt))

    def isPasswordValid(self, pw):
        if self.password is None:
            return False
        salt = self.password[-32:]
        h = hashlib.new("sha256")
        h.update(pw)
        h.update(salt)
        return self.password == (u"%s%s" % (h.hexdigest(), salt))

    @validates("ID", "username", "password", "admin")
    def validator(self, key, val):
        map = {"ID": lambda val: isinstance(val, int),
               "username": lambda val: isinstance(val, basestring),
               "password": lambda val: isinstance(val, basestring) and len(val) == 96,
               "admin": lambda val: isinstance(val, bool)}

        if not map[key](val):
            raise ValueError(str(val) + " is not a valid value for " + key)
        else:
            return val


@cachedQuery(User, 1, "lookfor")
def getUser(lookfor, eager=None):
    if isinstance(lookfor, int):
        if eager is None:
            with sqlAlchemy.sd_lock:
                user = sqlAlchemy.saveddata_session.query(User).get(lookfor)
        else:
            eager = processEager(eager)
            with sqlAlchemy.sd_lock:
                user = sqlAlchemy.saveddata_session.query(User).options(*eager).filter(User.ID == lookfor).first()
    elif isinstance(lookfor, basestring):
        eager = processEager(eager)
        with sqlAlchemy.sd_lock:
            user = sqlAlchemy.saveddata_session.query(User).options(*eager).filter(User.username == lookfor).first()
    else:
        raise TypeError("Need integer or string as argument")
    return user
