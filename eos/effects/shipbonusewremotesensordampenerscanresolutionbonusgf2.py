# shipBonusEwRemoteSensorDampenerScanResolutionBonusGF2
#
# Used by:
# Ship: Keres
# Ship: Maulus
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Sensor Damper",
                                  "scanResolutionBonus", ship.getModifiedItemAttr("shipBonusGF2"), skill="Gallente Frigate")
