# shipBonusEwRemoteSensorDampenerScanResolutionBonusRookie
#
# Used by:
# Ship: Velator
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Sensor Damper",
                                  "scanResolutionBonus", ship.getModifiedItemAttr("rookieDampStrengthBonus"))
