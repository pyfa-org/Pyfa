# shipBonusEwRemoteSensorDampenerMaxTargetRangeBonusGF2
#
# Used by:
# Variations of ship: Maulus (2 of 2)
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Sensor Damper",
                                  "maxTargetRangeBonus", ship.getModifiedItemAttr("shipBonusGF2"), skill="Gallente Frigate")
