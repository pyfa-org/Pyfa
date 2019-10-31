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


ECM_BURST_DURATION = 30
DRONE_LOCK_TIME = 2


class TgtScanRes2TgtLockTimeGetter(SmoothPointGetter):

    def _getCommonData(self, miscParams, src, tgt):
        if miscParams['applyDamps']:
            tgtScanResMult = src.item.getDampMultScanRes()
        else:
            tgtScanResMult = 1
        return {
            'tgtScanResMult': tgtScanResMult,
            'sigRadius': src.item.ship.getModifiedItemAttr('signatureRadius')}

    def _calculatePoint(self, x, miscParams, src, tgt, commonData):
        scanRes = x
        time = calculateLockTime(
            srcScanRes=scanRes * commonData['tgtScanResMult'],
            tgtSigRadius=commonData['sigRadius'])
        return time


class TgtScanRes2TgtLockUptimeGetter(TgtScanRes2TgtLockTimeGetter):

    def _calculatePoint(self, *args, **kwargs):
        # Assuming you ECM burst every 30 seconds, find out how long you
        # will be locked before you burst another time
        lockTime = super()._calculatePoint(*args, **kwargs)
        lockedTime = max(0, ECM_BURST_DURATION - lockTime)
        return lockedTime


class SrcDmgBaseGetter(SmoothPointGetter):

    def _getCommonData(self, miscParams, src, tgt):
        if miscParams['applyDamps']:
            tgtScanResMult = src.item.getDampMultScanRes()
        else:
            tgtScanResMult = 1
        return {
            'tgtScanResMult': tgtScanResMult,
            'srcSigRadius': src.item.ship.getModifiedItemAttr('signatureRadius'),
            'srcEhp': sum(src.item.ehp.values()),
            'srcDpsWeapon': src.item.getWeaponDps().total,
            'srcDpsDrone': src.item.getDroneDps().total if miscParams['applyDrones'] else 0}

    @staticmethod
    def _calculateInflictedDamage(srcSigRadius, srcWeaponDps, srcDroneDps, srcEhp, tgtScanRes, tgtDps, uptimeAdjustment, uptimeAmountLimit):
        lockTime = calculateLockTime(srcScanRes=tgtScanRes, tgtSigRadius=srcSigRadius)
        lockUptime = max(0, ECM_BURST_DURATION - lockTime - uptimeAdjustment)
        lockDowntime = ECM_BURST_DURATION - lockUptime
        inflictedDmg = 0
        remainingEhp = srcEhp
        for i in range(int(uptimeAmountLimit)):
            timeAliveUnderFire = min(lockUptime, remainingEhp / tgtDps)
            timeAlive = lockDowntime + timeAliveUnderFire
            remainingEhp -= lockUptime * tgtDps
            inflictedDmg += timeAlive * srcWeaponDps
            inflictedDmg += max(0, timeAlive - DRONE_LOCK_TIME - 1) * srcDroneDps
            if remainingEhp <= 0:
                break
        return inflictedDmg


class TgtScanRes2SrcDmgGetter(SrcDmgBaseGetter):

    def _calculatePoint(self, x, miscParams, src, tgt, commonData):
        damage = self._calculateInflictedDamage(
            srcSigRadius=commonData['srcSigRadius'],
            srcWeaponDps=commonData['srcDpsWeapon'],
            srcDroneDps=commonData['srcDpsDrone'],
            srcEhp=commonData['srcEhp'],
            tgtScanRes=x * commonData['tgtScanResMult'],
            tgtDps=miscParams['tgtDps'],
            uptimeAdjustment=miscParams['uptimeAdj'],
            uptimeAmountLimit=miscParams['uptimeAmtLimit'])
        return damage


class TgtDps2SrcDmgGetter(SrcDmgBaseGetter):

    def _calculatePoint(self, x, miscParams, src, tgt, commonData):
        damage = self._calculateInflictedDamage(
            srcSigRadius=commonData['srcSigRadius'],
            srcWeaponDps=commonData['srcDpsWeapon'],
            srcDroneDps=commonData['srcDpsDrone'],
            srcEhp=commonData['srcEhp'],
            tgtScanRes=miscParams['tgtScanRes'] * commonData['tgtScanResMult'],
            tgtDps=x,
            uptimeAdjustment=miscParams['uptimeAdj'],
            uptimeAmountLimit=miscParams['uptimeAmtLimit'])
        return damage
