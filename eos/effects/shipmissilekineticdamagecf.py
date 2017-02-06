# shipMissileKineticDamageCF
#
# Used by:
# Ship: Buzzard
# Ship: Condor
# Ship: Hawk
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                    "kineticDamage", ship.getModifiedItemAttr("shipBonusCF"), skill="Caldari Frigate")
