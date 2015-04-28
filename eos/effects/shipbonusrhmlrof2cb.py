# shipBonusRHMLROF2CB
#
# Used by:
# Ship: Raven
# Ship: Widow
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Battleship").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher Rapid Heavy",
                                  "speed", ship.getModifiedItemAttr("shipBonus2CB") * level)
