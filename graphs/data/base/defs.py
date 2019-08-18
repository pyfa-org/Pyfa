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


from collections import namedtuple


VectorDef = namedtuple('VectorDef', ('lengthHandle', 'lengthUnit', 'angleHandle', 'angleUnit', 'label'))
InputCheckbox = namedtuple('InputCheckbox', ('handle', 'label', 'defaultValue'))


class YDef:

    def __init__(self, handle, unit, label, selectorLabel=None):
        self.handle = handle
        self.unit = unit
        self.label = label
        self._selectorLabel = selectorLabel

    @property
    def selectorLabel(self):
        if self._selectorLabel is not None:
            return self._selectorLabel
        return self.label

    def __hash__(self):
        return hash((self.handle, self.unit, self.label, self._selectorLabel))

    def __eq__(self, other):
        if not isinstance(other, YDef):
            return False
        return all((
            self.handle == other.handle,
            self.unit == other.unit,
            self.label == other.label,
            self._selectorLabel == other._selectorLabel))


class XDef:

    def __init__(self, handle, unit, label, mainInput, selectorLabel=None):
        self.handle = handle
        self.unit = unit
        self.label = label
        self.mainInput = mainInput
        self._selectorLabel = selectorLabel

    @property
    def selectorLabel(self):
        if self._selectorLabel is not None:
            return self._selectorLabel
        return self.label

    def __hash__(self):
        return hash((self.handle, self.unit, self.label, self.mainInput, self._selectorLabel))

    def __eq__(self, other):
        if not isinstance(other, XDef):
            return False
        return all((
            self.handle == other.handle,
            self.unit == other.unit,
            self.label == other.label,
            self.mainInput == other.mainInput,
            self._selectorLabel == other._selectorLabel))


class Input:

    def __init__(self, handle, unit, label, iconID, defaultValue, defaultRange, mainOnly=False, mainTooltip=None, secondaryTooltip=None):
        self.handle = handle
        self.unit = unit
        self.label = label
        self.iconID = iconID
        self.defaultValue = defaultValue
        self.defaultRange = defaultRange
        self.mainOnly = mainOnly
        self.mainTooltip = mainTooltip
        self.secondaryTooltip = secondaryTooltip

    def __hash__(self):
        return hash((self.handle, self.unit, self.label, self.iconID, self.defaultValue, self.defaultRange, self.mainOnly, self.mainTooltip, self.secondaryTooltip))

    def __eq__(self, other):
        if not isinstance(other, Input):
            return False
        return all((
            self.handle == other.handle,
            self.unit == other.unit,
            self.label == other.label,
            self.iconID == other.iconID,
            self.defaultValue == other.defaultValue,
            self.defaultRange == other.defaultRange,
            self.mainOnly == other.mainOnly,
            self.mainTooltip == other.mainTooltip,
            self.secondaryTooltip == other.secondaryTooltip))
