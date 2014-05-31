# Used by:
# Variations of ship: Cyclone (2 of 2)
# Ship: Cyclone Thukker Tribe Edition
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Minmatar Battlecruiser").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher Heavy",
                                  "speed", ship.getModifiedItemAttr("shipBonusMBC2") * level)
