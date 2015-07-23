# shipRocketExplosiveDmgMD1
#
# Used by:
# Ship: Talwar
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Rockets"),
                                    "explosiveDamage", ship.getModifiedItemAttr("shipBonusMD1"), skill="Minmatar Destroyer")
