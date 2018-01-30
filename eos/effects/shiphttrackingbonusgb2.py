# shipHTTrackingBonusGB2
#
# Used by:
# Ships named like: Megathron (3 of 3)
# Ship: Marshal
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Large Hybrid Turret"),
                                  "trackingSpeed", ship.getModifiedItemAttr("shipBonusGB2"),
                                  skill="Gallente Battleship")
