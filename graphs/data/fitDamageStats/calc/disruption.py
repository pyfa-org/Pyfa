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

from eos.calc import calculateMultiplier, calculateRangeFactor


# Weapon disruption attributes which affect the attacker's damage output.
# Guidance disruptors modify missiles, tracking disruptors modify turrets.
DISRUPTION_ATTRS = (
    'aoeCloudSizeBonus',
    'aoeVelocityBonus',
    'missileVelocityBonus',
    'explosionDelayBonus',
    'trackingSpeedBonus',
    'maxRangeBonus',
    'falloffBonus')

DisruptionProjData = namedtuple('DisruptionProjData', ('boosts', 'optimal', 'falloff', 'stackingGroup'))

# Maps disruptor bonus attributes to the attributes they modify on the victim
DISRUPTION_ATTR_MAP = {
    'aoeCloudSizeBonus': 'aoeCloudSize',
    'aoeVelocityBonus': 'aoeVelocity',
    'missileVelocityBonus': 'maxVelocity',
    'explosionDelayBonus': 'explosionDelay',
    'trackingSpeedBonus': 'trackingSpeed',
    'maxRangeBonus': 'maxRange',
    'falloffBonus': 'falloff'}

_DISRUPTION_EFFECTS = (
    'shipModuleGuidanceDisruptor',
    'shipModuleTrackingDisruptor',
    'structureModuleEffectWeaponDisruption')


def getDisruptionModules(tgt):
    """Weapon disruptors active on ``tgt``, ready to be projected onto ``src``."""
    modules = []
    if not tgt.isFit:
        return modules
    for mod in tgt.item.activeModulesIter():
        if not mod.item:
            continue
        boosts = {}
        for effectName in _DISRUPTION_EFFECTS:
            if effectName not in mod.item.effects:
                continue
            for attrName in DISRUPTION_ATTRS:
                boost = mod.getModifiedItemAttr(attrName)
                if boost:
                    boosts[attrName] = boosts.get(attrName, 0) + boost
        if not boosts:
            continue
        modules.append(DisruptionProjData(
            boosts,
            mod.maxRange or 0,
            mod.falloff or 0,
            'default'))
    return modules


def getDisruptionMultipliers(disruptionData, distance):
    """Multipliers for the attributes modified by the target's disruptors."""
    if not disruptionData:
        return {}
    applied = {}
    for data in disruptionData:
        rangeFactor = calculateRangeFactor(
            srcOptimalRange=data.optimal,
            srcFalloffRange=data.falloff,
            distance=distance)
        if not rangeFactor:
            continue
        for attrName, boost in data.boosts.items():
            appliedAttr = DISRUPTION_ATTR_MAP[attrName]
            appliedBoost = boost * rangeFactor
            applied.setdefault(appliedAttr, {}).setdefault(data.stackingGroup, []).append((1 + appliedBoost / 100, None))
    return {attrName: calculateMultiplier(groups) for attrName, groups in applied.items()}
