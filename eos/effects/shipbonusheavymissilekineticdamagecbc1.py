# shipBonusHeavyMissileKineticDamageCBC1
#
# Used by:
# Ship: Drake
# Ship: Nighthawk
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"),
                                    "kineticDamage", ship.getModifiedItemAttr("shipBonusCBC1"), skill="Caldari Battlecruiser")
