# Used by:
# Ship: Typhoon
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Minmatar Battleship").level
    groups = ("Missile Launcher Torpedo", "Missile Launcher Cruise")
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name in groups,
                                  "speed", ship.getModifiedItemAttr("shipBonusMB") * level)
