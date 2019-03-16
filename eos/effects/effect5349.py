# shipBonusHeavyMissileLauncherRofMBC2
#
# Used by:
# Variations of ship: Cyclone (2 of 2)
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher Heavy",
                                  "speed", ship.getModifiedItemAttr("shipBonusMBC2"), skill="Minmatar Battlecruiser")
