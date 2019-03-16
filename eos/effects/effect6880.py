# shipBonusLauncherRoF2CB
#
# Used by:
# Ship: Marshal
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher Cruise", "speed",
                                  src.getModifiedItemAttr("shipBonus2CB"), skill="Caldari Battleship")
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher Torpedo", "speed",
                                  src.getModifiedItemAttr("shipBonus2CB"), skill="Caldari Battleship")
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher Rapid Heavy", "speed",
                                  src.getModifiedItemAttr("shipBonus2CB"), skill="Caldari Battleship")
