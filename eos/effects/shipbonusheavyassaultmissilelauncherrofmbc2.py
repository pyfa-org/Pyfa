# Used by:
# Variations of ship: Cyclone (2 of 2)
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Minmatar Battlecruiser").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher Heavy Assault",
                                  "speed", ship.getModifiedItemAttr("shipBonusMBC2") * level)
