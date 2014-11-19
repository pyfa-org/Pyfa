# shipBonusFrigateSizedLightMissileExplosiveDamageMD1
#
# Used by:
# Ship: Talwar
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Minmatar Destroyer").level
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Light Missiles"),
                                    "explosiveDamage", ship.getModifiedItemAttr("shipBonusMD1") * level)
