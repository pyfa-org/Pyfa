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

from sqlalchemy.orm import validates


class User(object):
    def __init__(self, username, password=None, admin=False):
        self.username = username
        if password is not None:
            self.encodeAndSetPassword(password)
        self.admin = admin

    def encodeAndSetPassword(self, pw):
        h = hashlib.new("sha256")
        salt = "".join([random.choice(string.letters) for _ in range(32)])
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
        return self.password == ("%s%s" % (h.hexdigest(), salt))

    @validates("ID", "username", "password", "admin")
    def validator(self, key, val):
        map = {
            "ID"      : lambda _val: isinstance(_val, int),
            "username": lambda _val: isinstance(_val, str),
            "password": lambda _val: isinstance(_val, str) and len(_val) == 96,
            "admin"   : lambda _val: isinstance(_val, bool)
        }

        if not map[key](val):
            raise ValueError(str(val) + " is not a valid value for " + key)
        else:
            return val
