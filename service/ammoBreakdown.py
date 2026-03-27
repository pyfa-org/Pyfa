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
from eos.utils.spoolSupport import SpoolOptions, SpoolType
from eos.utils.stats import DmgTypes
from service.fit import Fit


def _damage_type_string(volley):
    """
    Return primary damage type, or "Primary / Secondary" if secondary > 0.
    Returns "—" if all four damage types are 0.
    """
    ordered = [
        (volley.em, 'EM'),
        (volley.thermal, 'Thermal'),
        (volley.kinetic, 'Kinetic'),
        (volley.explosive, 'Explosive'),
    ]
    ordered.sort(key=lambda x: x[0], reverse=True)
    primary = ordered[0]
    if primary[0] <= 0:
        return "—"
    secondary = ordered[1]
    if secondary[0] <= 0:
        return primary[1]
    return "{} / {}".format(primary[1], secondary[1])


def get_ammo_in_cargo_usable_by_weapons(fit):
    """
    Return set of charge items that are in fit.cargo and can be used by at least
    one turret or launcher on the fit.
    """
    if fit is None:
        return set()
    cargo_item_ids = {c.itemID for c in fit.cargo if c.item is not None and getattr(c.item, 'isCharge', False)}
    if not cargo_item_ids:
        return set()
    usable = set()
    for mod in fit.modules:
        if not mod.canDealDamage():
            continue
        try:
            valid = mod.getValidCharges()
        except Exception:
            continue
        for charge in valid:
            if charge.ID in cargo_item_ids:
                usable.add(charge)
    return usable


def get_ammo_breakdown(fit):
    """
    For each ammo type in cargo that at least one weapon can use, compute
    aggregated DPS, Alpha (volley), Optimal, and Falloff assuming all such
    weapons are loaded with that ammo.

    Returns a list of dicts with keys: ammoName, damageType, optimal, falloff, alpha, dps.
    optimal/falloff may be strings (e.g. "12.5 – 18.2 km") or "—" for N/A.
    alpha and dps are floats (total).
    """
    if fit is None:
        return []
    default_spool = eos.config.settings['globalDefaultSpoolupPercentage'] or 1.0
    spool_opts = SpoolOptions(SpoolType.SPOOL_SCALE, default_spool, False)

    ammo_items = get_ammo_in_cargo_usable_by_weapons(fit)
    if not ammo_items:
        return []

    # Modules that can use each charge (by charge ID)
    charge_id_to_mods = {}
    for mod in fit.modules:
        if not mod.canDealDamage():
            continue
        try:
            valid = mod.getValidCharges()
        except Exception:
            continue
        for charge in valid:
            if charge in ammo_items:
                charge_id_to_mods.setdefault(charge.ID, []).append(mod)

    result = []
    for charge in ammo_items:
        mods = charge_id_to_mods.get(charge.ID, [])
        if not mods:
            continue

        # Save and restore charges
        saved_charges = [(m, m.charge) for m in mods]
        try:
            for m in mods:
                m.charge = charge
            fit.calculated = False
            fit.calculateModifiedAttributes()
            total_dps = DmgTypes.default()
            total_volley = DmgTypes.default()
            optimals = []
            falloffs = []
            for m in mods:
                total_dps += m.getDps(spoolOptions=spool_opts)
                total_volley += m.getVolley(spoolOptions=spool_opts)
                try:
                    r = m.maxRange
                    if r is not None:
                        optimals.append(r)
                except Exception:
                    pass
                try:
                    f = m.falloff
                    if f is not None:
                        falloffs.append(f)
                except Exception:
                    pass
        finally:
            for m, ch in saved_charges:
                m.charge = ch

        alpha = total_volley.total
        dps = total_dps.total
        if optimals:
            opt_min, opt_max = min(optimals), max(optimals)
            optimal_str = "{:.1f} – {:.1f} km".format(opt_min / 1000, opt_max / 1000) if opt_min != opt_max else "{:.1f} km".format(opt_min / 1000)
        else:
            optimal_str = "—"
        if falloffs:
            f_min, f_max = min(falloffs), max(falloffs)
            falloff_str = "{:.1f} – {:.1f} km".format(f_min / 1000, f_max / 1000) if f_min != f_max else "{:.1f} km".format(f_min / 1000)
        else:
            falloff_str = "—"

        result.append({
            'ammoName': charge.name,
            'damageType': _damage_type_string(total_volley),
            'optimal': optimal_str,
            'falloff': falloff_str,
            'alpha': alpha,
            'dps': dps,
        })
    # Sort by ammo name
    result.sort(key=lambda r: r['ammoName'])
    if result:
        Fit.getInstance().recalc(fit)
    return result
