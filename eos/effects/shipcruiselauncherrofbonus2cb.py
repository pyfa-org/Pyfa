# shipCruiseLauncherROFBonus2CB
#
# Used by:
# Ship: Raven
# Ship: Raven State Issue
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Battleship").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher Cruise",
                                  "speed", ship.getModifiedItemAttr("shipBonus2CB") * level)
