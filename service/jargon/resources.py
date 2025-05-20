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

from importlib.resources import files

PACKAGE_NAME = __name__.rsplit(".", maxsplit=1)[0]

DEFAULT_DATA = files(PACKAGE_NAME).joinpath('defaults.yaml').open('r', encoding='utf8').read()
DEFAULT_HEADER = files(PACKAGE_NAME).joinpath('header.yaml').open('r', encoding='utf8').read()
