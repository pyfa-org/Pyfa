# Used by:
# Modules from group: Remote Sensor Booster (8 of 8)
# Modules from group: Remote Sensor Damper (9 of 9)
# Modules from group: Sensor Booster (12 of 12)
type = "overheat"
def handler(fit, module, context):
    module.boostItemAttr("maxTargetRangeBonus", module.getModifiedItemAttr("overloadSensorModuleStrengthBonus"))
    module.boostItemAttr("scanResolutionBonus", module.getModifiedItemAttr("overloadSensorModuleStrengthBonus"),
                         stackingPenalties=True)
