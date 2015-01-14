# shipBonusKineticMissileDamageGB2
#
# Used by:
# Ships named like: Rattlesnake (2 of 2)
# Ship: 响尾蛇级YC117年特别版
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Battleship").level
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Missile Launcher Operation"),
                                    "kineticDamage", ship.getModifiedItemAttr("shipBonusGB2") * level)
