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


from eos.calc import calculateLockTime
from graphs.data.base import SmoothPointGetter


class ScanRes2LockingTimeGetter(SmoothPointGetter):

    def _getCommonData(self, miscParams, src, tgt):
        if miscParams['applyDamps']:
            scanResMult = src.item.getDampMultScanRes()
        else:
            scanResMult = 1
        return {'scanResMult': scanResMult}

    def _calculatePoint(self, x, miscParams, src, tgt, commonData):
        scanRes = x
        time = calculateLockTime(
            srcScanRes=scanRes * commonData['scanResMult'],
            tgtSigRadius=src.item.ship.getModifiedItemAttr('signatureRadius'))
        return time


class ScanRes2LockedTimeGetter(ScanRes2LockingTimeGetter):

    def _calculatePoint(self, *args, **kwargs):
        # Assuming you ECM burst every 30 seconds, find out how long you
        # will be locked before you burst another time
        lockTime = super()._calculatePoint(*args, **kwargs)
        lockedTime = max(0, 30 - lockTime)
        return lockedTime
