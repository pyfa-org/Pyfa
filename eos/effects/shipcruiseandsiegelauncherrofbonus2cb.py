# Used by:
# Ship: Widow
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Caldari Battleship").level
    affectedGroups = ("Missile Launcher Cruise", "Missile Launcher Torpedo")
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in affectedGroups,
                                  "speed", ship.getModifiedItemAttr("shipBonus2CB") * level)
