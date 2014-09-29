# shipBonusEwRemoteSensorDampenerScanResolutionBonusRookie
#
# Used by:
# Ship: Velator
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Gallente Frigate").level
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Sensor Damper",
                                  "scanResolutionBonus", ship.getModifiedItemAttr("rookieDampStrengthBonus"))
