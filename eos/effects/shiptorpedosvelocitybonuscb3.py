# shipTorpedosVelocityBonusCB3
#
# Used by:
# Ships named like: Raven (6 of 6)
# Ship: 乌鸦级YC117年特别版
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Battleship").level
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Torpedoes"),
                                    "maxVelocity", ship.getModifiedItemAttr("shipBonusCB3") * level)
