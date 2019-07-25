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


from eos.saveddata.fit import Fit
from eos.saveddata.targetProfile import TargetProfile


def getTgtMaxVelocity(tgt, extraMultipliers=None):
    if isinstance(tgt, Fit):
        if extraMultipliers:
            return tgt.ship.getModifiedItemAttrWithExtraMods('maxVelocity', extraMultipliers=extraMultipliers)
        else:
            return tgt.ship.getModifiedItemAttr('maxVelocity')
    elif isinstance(tgt, TargetProfile):
        return tgt.maxVelocity
    return None


def getTgtSigRadius(tgt, extraMultipliers=None):
    if isinstance(tgt, Fit):
        if extraMultipliers:
            return tgt.ship.getModifiedItemAttrWithExtraMods('signatureRadius', extraMultipliers=extraMultipliers)
        else:
            return tgt.ship.getModifiedItemAttr('signatureRadius')
    elif isinstance(tgt, TargetProfile):
        return tgt.signatureRadius
    return None


def getTgtRadius(tgt):
    if isinstance(tgt, Fit):
        return tgt.ship.getModifiedItemAttr('radius')
    elif isinstance(tgt, TargetProfile):
        return tgt.radius
    return None
