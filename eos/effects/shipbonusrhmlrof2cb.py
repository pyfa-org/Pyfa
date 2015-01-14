# shipBonusRHMLROF2CB
#
# Used by:
# Ships named like: Raven Edition (3 of 3)
# Ship: Raven
# Ship: Widow
# Ship: 乌鸦级YC117年特别版
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Battleship").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher Rapid Heavy",
                                  "speed", ship.getModifiedItemAttr("shipBonus2CB") * level)
