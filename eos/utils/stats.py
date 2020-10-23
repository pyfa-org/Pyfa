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


from eos.utils.float import floatUnerr
from utils.repr import makeReprStr


def _t(x):
    return x


class DmgTypes:
    """Container for damage data stats."""

    def __init__(self, em, thermal, kinetic, explosive):
        self.em = em
        self.thermal = thermal
        self.kinetic = kinetic
        self.explosive = explosive
        self._calcTotal()

    # Iterator is needed to support tuple-style unpacking
    def __iter__(self):
        yield self.em
        yield self.thermal
        yield self.kinetic
        yield self.explosive
        yield self.total

    def __eq__(self, other):
        if not isinstance(other, DmgTypes):
            return NotImplemented
        # Round for comparison's sake because often damage profiles are
        # generated from data which includes float errors
        return (
                floatUnerr(self.em) == floatUnerr(other.em) and
                floatUnerr(self.thermal) == floatUnerr(other.thermal) and
                floatUnerr(self.kinetic) == floatUnerr(other.kinetic) and
                floatUnerr(self.explosive) == floatUnerr(other.explosive) and
                floatUnerr(self.total) == floatUnerr(other.total))

    def __bool__(self):
        return any((
            self.em, self.thermal, self.kinetic,
            self.explosive, self.total))

    def _calcTotal(self):
        self.total = self.em + self.thermal + self.kinetic + self.explosive

    def __add__(self, other):
        return type(self)(
            em=self.em + other.em,
            thermal=self.thermal + other.thermal,
            kinetic=self.kinetic + other.kinetic,
            explosive=self.explosive + other.explosive)

    def __iadd__(self, other):
        self.em += other.em
        self.thermal += other.thermal
        self.kinetic += other.kinetic
        self.explosive += other.explosive
        self._calcTotal()
        return self

    def __mul__(self, mul):
        return type(self)(
            em=self.em * mul,
            thermal=self.thermal * mul,
            kinetic=self.kinetic * mul,
            explosive=self.explosive * mul)

    def __imul__(self, mul):
        if mul == 1:
            return
        self.em *= mul
        self.thermal *= mul
        self.kinetic *= mul
        self.explosive *= mul
        self._calcTotal()
        return self

    def __truediv__(self, div):
        return type(self)(
            em=self.em / div,
            thermal=self.thermal / div,
            kinetic=self.kinetic / div,
            explosive=self.explosive / div)

    def __itruediv__(self, div):
        if div == 1:
            return
        self.em /= div
        self.thermal /= div
        self.kinetic /= div
        self.explosive /= div
        self._calcTotal()
        return self

    def __repr__(self):
        spec = DmgTypes.names()
        spec.append('total')
        return makeReprStr(self, spec)

    @staticmethod
    def names(short=None, postProcessor=None):
        value = [_t('em'), _t('th'), _t('kin'), _t('exp')] if short else [_t('em'), _t('thermal'), _t('kinetic'), _t('explosive')]

        if postProcessor:
            value = [postProcessor(x) for x in value]

        return value


class RRTypes:
    """Container for tank data stats."""

    def __init__(self, shield, armor, hull, capacitor):
        self.shield = shield
        self.armor = armor
        self.hull = hull
        self.capacitor = capacitor

    # Iterator is needed to support tuple-style unpacking
    def __iter__(self):
        yield self.shield
        yield self.armor
        yield self.hull
        yield self.capacitor

    def __eq__(self, other):
        if not isinstance(other, RRTypes):
            return NotImplemented
        # Round for comparison's sake because often tanking numbers are
        # generated from data which includes float errors
        return (
                floatUnerr(self.shield) == floatUnerr(other.shield) and
                floatUnerr(self.armor) == floatUnerr(other.armor) and
                floatUnerr(self.hull) == floatUnerr(other.hull) and
                floatUnerr(self.capacitor) == floatUnerr(other.capacitor))

    def __bool__(self):
        return any((self.shield, self.armor, self.hull, self.capacitor))

    def __add__(self, other):
        return type(self)(
            shield=self.shield + other.shield,
            armor=self.armor + other.armor,
            hull=self.hull + other.hull,
            capacitor=self.capacitor + other.capacitor)

    def __iadd__(self, other):
        self.shield += other.shield
        self.armor += other.armor
        self.hull += other.hull
        self.capacitor += other.capacitor
        return self

    def __mul__(self, mul):
        return type(self)(
            shield=self.shield * mul,
            armor=self.armor * mul,
            hull=self.hull * mul,
            capacitor=self.capacitor * mul)

    def __imul__(self, mul):
        if mul == 1:
            return
        self.shield *= mul
        self.armor *= mul
        self.hull *= mul
        self.capacitor *= mul
        return self

    def __truediv__(self, div):
        return type(self)(
            shield=self.shield / div,
            armor=self.armor / div,
            hull=self.hull / div,
            capacitor=self.capacitor / div)

    def __itruediv__(self, div):
        if div == 1:
            return self
        self.shield /= div
        self.armor /= div
        self.hull /= div
        self.capacitor /= div
        return self

    def __repr__(self):
        spec = RRTypes.names(False)
        return makeReprStr(self, spec)

    @staticmethod
    def names(ehpOnly=True, postProcessor=None):
        value = ['shield', 'armor', 'hull']

        if not ehpOnly:
            value.append('capacitor')

        if postProcessor:
            value = [postProcessor(x) for x in value]

        return value
