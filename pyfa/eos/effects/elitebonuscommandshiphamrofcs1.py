# eliteBonusCommandShipHAMRoFCS1
#
# Used by:
# Ship: Claymore
# Ship: Nighthawk
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Command Ships").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher Heavy Assault",
                                  "speed", ship.getModifiedItemAttr("eliteBonusCommandShips1") * level)
