# shipBonusEwRemoteSensorDampenerOptimalBonusGC1
#
# Used by:
# Ship: Celestis
type = "passive"


def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Sensor Dampener",
                                  "maxRange", ship.getModifiedItemAttr("shipBonusGC"), skill="Gallente Cruiser")
