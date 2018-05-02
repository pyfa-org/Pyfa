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

JARGON_PATH = os.path.join(config.savePath, 'jargon.yaml')

class JargonLoader(object):
    def __init__(self, jargon_path: str):
        self.jargon_path = jargon_path
        self._jargon_mtime = 0 # type: int
        self._jargon = None # type: Jargon

    def get_jargon(self) -> Jargon:
        if self._is_stale():
            self._load_jargon()
        return self._jargon

    def _is_stale(self):
        return (not self._jargon or not self._jargon_mtime or
                self.jargon_mtime != self._get_jargon_file_mtime())

    def _load_jargon(self):
        jargondata = yaml.load(DEFAULT_DATA)
        with open(JARGON_PATH) as f:
            userdata = yaml.load(f)
        jargondata.update(userdata)
        self.jargon_mtime = self._get_jargon_file_mtime()
        self._jargon = Jargon(jargondata)

    def _get_jargon_file_mtime(self) -> int:
        if not os.path.exists(self.jargon_path):
            return 0
        return os.stat(self.jargon_path).st_mtime

    @staticmethod
    def init_user_jargon(jargon_path):
        values = yaml.load(DEFAULT_DATA)

        ## Disabled for issue/1533; do not overwrite existing user config
        # if os.path.exists(jargon_path):
        #     with open(jargon_path) as f:
        #         custom_values = yaml.load(f)
        #     if custom_values:
        #         values.update(custom_values)

        if not os.path.exists(jargon_path):
            with open(jargon_path, 'w') as f:
                f.write(DEFAULT_HEADER)
                f.write('\n\n')
                yaml.dump(values, stream=f, default_flow_style=False)

    _instance = None
    @staticmethod
    def instance(jargon_path=None):
        if not JargonLoader._instance:
            jargon_path = jargon_path or JARGON_PATH
            JargonLoader._instance = JargonLoader(jargon_path)
        return JargonLoader._instance

JargonLoader.init_user_jargon(JARGON_PATH)
