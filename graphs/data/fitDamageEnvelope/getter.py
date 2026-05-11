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


import eos.config
from eos.const import FittingHardpoint
from eos.saveddata.targetProfile import TargetProfile
from eos.utils.spoolSupport import SpoolOptions, SpoolType
from graphs.calc import checkLockRange
from graphs.data.base import SmoothPointGetter
from graphs.data.fitDamageStats.calc.application import (_calcMissileFactor, _calcTurretChanceToHit, _calcTurretMult,
                                                         getApplicationPerKey, )
from service.settings import GraphSettings


def _buildResistProfile(tgtResists, tgtFullHp):
    if not GraphSettings.getInstance().get('ignoreResists'):
        emRes, thermRes, kinRes, exploRes = tgtResists
    else:
        emRes = thermRes = kinRes = exploRes = 0
    return TargetProfile(emAmount=emRes, thermalAmount=thermRes, kineticAmount=kinRes, explosiveAmount=exploRes,
        hp=tgtFullHp)


def _typedDmgScalar(dmgTyped, applicationMult, profile):
    """Apply application multiplier and resist profile, return scalar EHP/s."""
    if applicationMult == 0:
        return 0
    scaled = dmgTyped * applicationMult
    scaled.profile = profile
    return scaled.total


def _turretApplication(snapshot, src, tgt, atkSpeed, atkAngle, distance, tgtSpeed, tgtAngle, tgtSigRadius):
    cth = _calcTurretChanceToHit(atkSpeed=atkSpeed, atkAngle=atkAngle, atkRadius=src.getRadius(),
        atkOptimalRange=snapshot['maxRange'] or 0, atkFalloffRange=snapshot['falloff'] or 0,
        atkTracking=snapshot['tracking'], atkOptimalSigRadius=snapshot['optimalSigRadius'], distance=distance,
        tgtSpeed=tgtSpeed, tgtAngle=tgtAngle, tgtRadius=tgt.getRadius(), tgtSigRadius=tgtSigRadius)
    return _calcTurretMult(cth)


def _missileApplication(snapshot, distance, tgtSpeed, tgtSigRadius):
    rangeData = snapshot['missileMaxRangeData']
    if rangeData is None:
        return 0
    lowerRange, higherRange, higherChance = rangeData
    if distance is None or distance <= lowerRange:
        distanceFactor = 1
    elif lowerRange < distance <= higherRange:
        distanceFactor = higherChance
    else:
        distanceFactor = 0
    if distanceFactor == 0:
        return 0
    applicationFactor = _calcMissileFactor(atkEr=snapshot['aoeCloudSize'], atkEv=snapshot['aoeVelocity'],
        atkDrf=snapshot['aoeDamageReductionFactor'], tgtSpeed=tgtSpeed, tgtSigRadius=tgtSigRadius)
    return distanceFactor * applicationFactor


def _snapshotTurret(mod, dmgTyped, charge):
    return {'kind': 'turret', 'charge': charge, 'dmg': dmgTyped, 'maxRange': mod.maxRange, 'falloff': mod.falloff,
        'tracking': mod.getModifiedItemAttr('trackingSpeed'),
        'optimalSigRadius': mod.getModifiedItemAttr('optimalSigRadius')}


def _snapshotMissile(mod, dmgTyped, charge):
    return {'kind': 'missile', 'charge': charge, 'dmg': dmgTyped, 'missileMaxRangeData': mod.missileMaxRangeData,
        'aoeCloudSize': mod.getModifiedChargeAttr('aoeCloudSize'),
        'aoeVelocity': mod.getModifiedChargeAttr('aoeVelocity'),
        'aoeDamageReductionFactor': mod.getModifiedChargeAttr('aoeDamageReductionFactor'),
        'isFoF': 'fofMissileLaunching' in (charge.effects if charge else {})}


def _isAmmoEnvelopeWeapon(mod):
    """Turret or standard missile launcher with valid charges."""
    if mod.hardpoint not in (FittingHardpoint.TURRET, FittingHardpoint.MISSILE):
        return False
    # Skip exotic weapon groups handled separately by stock app logic
    if mod.item.group.name in ('Missile Launcher Bomb', 'Structure Guided Bomb Launcher'):
        return False
    if 'ChainLightning' in mod.item.effects:
        return False
    if mod.isBreacher:
        return False
    return bool(mod.getValidCharges())


def _snapshotForCurrentCharge(mod):
    """Build a snapshot dict for whatever charge is currently loaded on mod."""
    spoolOptions = SpoolOptions(SpoolType.SPOOL_SCALE, eos.config.settings['globalDefaultSpoolupPercentage'], False)
    dmgTyped = mod.getDps(spoolOptions=spoolOptions)
    if mod.hardpoint == FittingHardpoint.TURRET:
        return _snapshotTurret(mod, dmgTyped, mod.charge)
    return _snapshotMissile(mod, dmgTyped, mod.charge)


def _collectWeaponCandidates(src):
    """For each ammo-bearing weapon, return list of per-charge snapshots.

    Charge-dependent attributes (optimal/falloff/tracking/missile range/AoE) are
    only applied to the module's modified attributes by a full fit recalc.
    Since ammo effects are gun-local in EVE (a crystal in laser-1 does not
    affect laser-2's attributes), we load up to N different ammos onto N
    different weapons of the same group, recalc the fit once, and snapshot
    all N (weapon, ammo) pairs from that single recalc. For a group of size
    K weapons and M ammos this needs ceil(M / K) recalcs instead of M.
    Originals are always restored via try/finally even if a calc raises.
    """
    fit = src.item
    weapon_mods = [mod for mod in fit.activeModulesIter() if _isAmmoEnvelopeWeapon(mod)]
    if not weapon_mods:
        return []

    # Group by (item ID, state) — within such a group, snapshots can be shared
    # across mods, and DPS reads need consistent per-mod state.
    groups = {}
    for mod in weapon_mods:
        groups.setdefault((mod.item.ID, mod.state), []).append(mod)

    originals = {id(mod): mod.charge for mod in weapon_mods}
    snapshots_by_mod = {id(mod): [] for mod in weapon_mods}
    spoolOptions = SpoolOptions(SpoolType.SPOOL_SCALE, eos.config.settings['globalDefaultSpoolupPercentage'], False)

    try:
        for group_mods in groups.values():
            valid_charges = sorted(group_mods[0].getValidCharges(), key=lambda c: c.name)
            if not valid_charges:
                continue
            chunk_size = len(group_mods)
            for chunk_start in range(0, len(valid_charges), chunk_size):
                chunk = valid_charges[chunk_start:chunk_start + chunk_size]
                # Assign one chunk-ammo per group mod (extras stay on their previous charge)
                for i, charge in enumerate(chunk):
                    group_mods[i].charge = charge
                fit.clear()
                fit.calculateModifiedAttributes()
                # Snapshot per (assignee mod, charge); copy to all group mods since
                # within an (item ID, state) group attributes for a given ammo match.
                for i, charge in enumerate(chunk):
                    assignee = group_mods[i]
                    dmgTyped = assignee.getDps(spoolOptions=spoolOptions)
                    if dmgTyped.total <= 0:
                        continue
                    if assignee.hardpoint == FittingHardpoint.TURRET:
                        snap = _snapshotTurret(assignee, dmgTyped, charge)
                    else:
                        snap = _snapshotMissile(assignee, dmgTyped, charge)
                    for target_mod in group_mods:
                        snapshots_by_mod[id(target_mod)].append(snap)
    finally:
        for mod in weapon_mods:
            mod.charge = originals[id(mod)]
        fit.clear()
        fit.calculateModifiedAttributes()

    weapons = [{'mod': mod, 'candidates': snapshots_by_mod[id(mod)]} for mod in weapon_mods if
               snapshots_by_mod[id(mod)]]
    for weapon in weapons:
        weapon['candidates'] = _pruneDominated(weapon['candidates'], src)
    return weapons


def _pruneDominated(candidates, src):
    """Drop candidates whose effective-DPS curve is dominated everywhere.

    Sample each candidate's application-only multiplier (ignoring resists,
    which are mod-independent and uniformly scale all candidates) over a
    coarse distance grid. A candidate X is dominated if there exists Y such
    that Y's raw_damage * multiplier(distance) >= X's at every sample.
    """
    if len(candidates) <= 1:
        return candidates
    # Sample multipliers under a neutral mid-range scenario; this captures
    # the shape of each ammo's range envelope without depending on misc inputs.
    sampleDistances = [0, 1000, 5000, 10000, 20000, 40000, 80000, 160000, 320000]
    tgtSpeed = 0
    atkSpeed = 0
    tgtSigRadius = 125
    sigRefMod = src.getSigRadius()  # not directly used, kept for clarity
    del sigRefMod
    # For each candidate, build a scalar score vector across samples.
    scores = []
    for snap in candidates:
        rawTotal = snap['dmg'].total
        vec = []
        for d in sampleDistances:
            if snap['kind'] == 'turret':
                # Use only the range factor (drop tracking — angular speed is 0 here)
                # by passing 0 atkSpeed/tgtSpeed/tgtAngle.
                mult = _turretApplication(snap, src, src, atkSpeed, 0, d, tgtSpeed, 0, tgtSigRadius)
            else:
                mult = _missileApplication(snap, d, tgtSpeed, tgtSigRadius)
            vec.append(rawTotal * mult)
        scores.append(vec)
    # Mark dominated
    n = len(candidates)
    eps = 1e-9
    keep = [True] * n
    for i in range(n):
        if not keep[i]:
            continue
        for j in range(n):
            if i == j or not keep[j]:
                continue
            # j dominates i if scores[j][k] >= scores[i][k] - eps for all k
            # and scores[j][k] > scores[i][k] + eps for at least one k
            dominates = True
            strict = False
            for k in range(len(sampleDistances)):
                if scores[j][k] + eps < scores[i][k]:
                    dominates = False
                    break
                if scores[j][k] > scores[i][k] + eps:
                    strict = True
            if dominates and strict:
                keep[i] = False
                break
    return [c for c, k in zip(candidates, keep) if k]


def _bestWeaponDpsAtDistance(weapon, src, tgt, atkSpeed, atkAngle, distance, tgtSpeed, tgtAngle, tgtSigRadius, profile,
                             inLockRange):
    if not inLockRange:
        # Special case: FoF missiles ignore lock range
        candidates = [c for c in weapon['candidates'] if c.get('isFoF')]
        if not candidates:
            return 0
    else:
        candidates = weapon['candidates']
    best = 0
    for snap in candidates:
        if snap['kind'] == 'turret':
            mult = _turretApplication(snap, src, tgt, atkSpeed, atkAngle, distance, tgtSpeed, tgtAngle, tgtSigRadius)
        else:
            mult = _missileApplication(snap, distance, tgtSpeed, tgtSigRadius)
        scalar = _typedDmgScalar(snap['dmg'], mult, profile)
        if scalar > best:
            best = scalar
    return best


class Distance2EnvelopeDpsGetter(SmoothPointGetter):
    _baseResolution = 50
    _extraDepth = 2

    def _getCommonData(self, miscParams, src, tgt):
        # Snapshot per-weapon ammo candidates once. _calculatePoint reuses these
        # for every distance step so we avoid repeated charge swaps.
        weapons = _collectWeaponCandidates(src)
        # Track ammo-envelope weapon IDs so we can subtract their stock contribution
        # from the common application map below.
        envelopeMods = {id(w['mod']) for w in weapons}
        # Standard application path covers everything else (drones, fighters,
        # smartbombs, doomsdays, modules without valid charges, etc.).
        defaultSpool = eos.config.settings['globalDefaultSpoolupPercentage']
        spoolOptions = SpoolOptions(SpoolType.SPOOL_SCALE, defaultSpool, False)
        nonEnvelopeDmg = {}
        for mod in src.item.activeModulesIter():
            if id(mod) in envelopeMods:
                continue
            if not mod.isDealingDamage():
                continue
            nonEnvelopeDmg[mod] = mod.getDps(spoolOptions=spoolOptions)
        for drone in src.item.activeDronesIter():
            if not drone.isDealingDamage():
                continue
            nonEnvelopeDmg[drone] = drone.getDps()
        for fighter in src.item.activeFightersIter():
            if not fighter.isDealingDamage():
                continue
            for effectID, effectDps in fighter.getDpsPerEffect().items():
                nonEnvelopeDmg[(fighter, effectID)] = effectDps
        return {'weapons': weapons, 'nonEnvelopeDmg': nonEnvelopeDmg, 'tgtResists': tgt.getResists(),
            'tgtFullHp': tgt.getFullHp()}

    def _calculatePoint(self, x, miscParams, src, tgt, commonData):
        distance = x
        tgtSpeed = miscParams['tgtSpeed']
        tgtSigRadius = miscParams.get('tgtSigRad', tgt.getSigRadius())
        atkSpeed = miscParams.get('atkSpeed', 0) or 0
        atkAngle = miscParams.get('atkAngle', 0) or 0
        tgtAngle = miscParams.get('tgtAngle', 0) or 0
        profile = _buildResistProfile(commonData['tgtResists'], commonData['tgtFullHp'])
        inLockRange = checkLockRange(src=src, distance=distance)

        total = 0
        # Sum optimum-ammo contribution for each ammo-bearing weapon
        for weapon in commonData['weapons']:
            total += _bestWeaponDpsAtDistance(weapon=weapon, src=src, tgt=tgt, atkSpeed=atkSpeed, atkAngle=atkAngle,
                distance=distance, tgtSpeed=tgtSpeed, tgtAngle=tgtAngle, tgtSigRadius=tgtSigRadius, profile=profile,
                inLockRange=inLockRange)

        # Add fixed-ammo contributors (drones, fighters, smartbombs, etc.) using
        # the standard application math from fitDamageStats.
        if commonData['nonEnvelopeDmg']:
            applicationMap = getApplicationPerKey(src=src, tgt=tgt, atkSpeed=atkSpeed, atkAngle=atkAngle,
                distance=distance, tgtSpeed=tgtSpeed, tgtAngle=tgtAngle, tgtSigRadius=tgtSigRadius)
            for key, dmgTyped in commonData['nonEnvelopeDmg'].items():
                mult = applicationMap.get(key, 0)
                total += _typedDmgScalar(dmgTyped, mult, profile)
        return total
