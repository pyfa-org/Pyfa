# =============================================================================
# Copyright (C) 2010 Diego Duclos
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


# One BIG HACK to resolve circular imports the easy way
_LAZY = {
    'GraphFrame': ('.gui.frame', 'GraphFrame'),
    'graphFrame_enabled': ('.gui.canvasPanel', 'graphFrame_enabled')}


def __getattr__(name):
    try:
        moduleName, attrName = _LAZY[name]
    except KeyError:
        raise AttributeError('module {!r} has no attribute {!r}'.format(__name__, name)) from None
    from importlib import import_module
    value = getattr(import_module(moduleName, __name__), attrName)
    globals()[name] = value  # cache so __getattr__ runs once per name
    return value


def __dir__():
    return sorted(set(globals()) | set(_LAZY))
