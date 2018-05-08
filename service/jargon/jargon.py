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

import config
import pkg_resources

class Jargon(object):
    def __init__(self, rawdata: dict):
        self._rawdata = rawdata

        # copy the data to lowercase keys, ignore blank keys
        self._data = {str(k).lower():v for k,v in rawdata.items() if k}

    def get(self, term: str) -> str:
        return self._data.get(term.lower())

    def get_rawdata() -> dict:
        return self._rawdata

    def apply(self, query):
        query_words = query.split()
        parts = []

        for word in query_words:
            replacement = self.get(word)
            if replacement:
                parts.append(replacement)
            else:
                parts.append(word)

        return ' '.join(parts)
