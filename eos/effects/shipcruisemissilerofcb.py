# shipCruiseMissileROFCB
#
# Used by:
# Ship: Scorpion Navy Issue
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher Cruise",
                                  "speed", ship.getModifiedItemAttr("shipBonusCB"), skill="Caldari Battleship")
