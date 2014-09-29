# shipMissileKineticDamageCF
#
# Used by:
# Ship: Buzzard
# Ship: Caldari Navy Hookbill
# Ship: Condor
# Ship: Hawk
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Frigate").level
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                    "kineticDamage", ship.getModifiedItemAttr("shipBonusCF") * level)
