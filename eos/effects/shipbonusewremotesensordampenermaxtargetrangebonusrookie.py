# shipBonusEwRemoteSensorDampenerMaxTargetRangeBonusRookie
#
# Used by:
# Ship: Velator
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Sensor Dampener",
                                  "maxTargetRangeBonus", ship.getModifiedItemAttr("rookieDampStrengthBonus"))
