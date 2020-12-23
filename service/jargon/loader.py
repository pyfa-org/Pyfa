# =============================================================================
# Copyright (C) 2018 Filip Sufitchi
#
# This file is part of pyfa.
#
# pyfa is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyfa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfa.  If not, see <http://www.gnu.org/licenses/>.
# =============================================================================

import os
import config
import yaml

from .jargon import Jargon
from .resources import DEFAULT_DATA, DEFAULT_HEADER

USER_JARGON_PATH = os.path.join(config.savePath, 'user_jargon.yaml') if config.savePath is not None else None


class JargonLoader:

    def __init__(self):
        self._user_jargon_mtime = 0  # type: int
        self._jargon = None  # type: Jargon

    def get_jargon(self) -> Jargon:
        if self._is_stale():
            self._load_jargon()
        return self._jargon

    def _is_stale(self):
        return (not self._jargon or not self._user_jargon_mtime or
                self.jargon_mtime != self._get_user_jargon_mtime())

    def _load_jargon(self):
        jargondata = yaml.load(DEFAULT_DATA, Loader=yaml.SafeLoader)
        if USER_JARGON_PATH is not None and os.path.isfile(USER_JARGON_PATH):
            with open(USER_JARGON_PATH) as f:
                userdata = yaml.load(f, Loader=yaml.SafeLoader)
            if userdata:
                jargondata.update(userdata)
        self.jargon_mtime = self._get_user_jargon_mtime()
        self._jargon = Jargon(jargondata)

    def _get_user_jargon_mtime(self) -> int:
        if USER_JARGON_PATH is None or not os.path.isfile(USER_JARGON_PATH):
            return 0
        return os.stat(USER_JARGON_PATH).st_mtime

    @staticmethod
    def init_user_jargon(jargon_path):
        if not os.path.exists(jargon_path):
            with open(jargon_path, 'w') as f:
                f.write(DEFAULT_HEADER)
                f.write('\n\n')

    _instance = None

    @staticmethod
    def instance():
        if not JargonLoader._instance:
            JargonLoader._instance = JargonLoader()
        return JargonLoader._instance


if USER_JARGON_PATH is not None:
    JargonLoader.init_user_jargon(USER_JARGON_PATH)
