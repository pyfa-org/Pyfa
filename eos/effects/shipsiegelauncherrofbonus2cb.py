# shipSiegeLauncherROFBonus2CB
#
# Used by:
# Ship: Raven
# Ship: Raven State Issue
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher Torpedo",
                                  "speed", ship.getModifiedItemAttr("shipBonus2CB"), skill="Caldari Battleship")
