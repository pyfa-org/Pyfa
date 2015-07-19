# shipBonusCruiseROFMB
#
# Used by:
# Ship: Typhoon
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher Cruise",
                                  "speed", ship.getModifiedItemAttr("shipBonusMB"), skill="Minmatar Battleship")
