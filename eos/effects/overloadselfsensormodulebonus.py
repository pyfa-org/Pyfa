# overloadSelfSensorModuleBonus
#
# Used by:
# Modules from group: Remote Sensor Booster (8 of 8)
# Modules from group: Sensor Booster (16 of 16)
# Modules from group: Sensor Dampener (6 of 6)
type = "overheat"
def handler(fit, module, context):
    module.boostItemAttr("maxTargetRangeBonus", module.getModifiedItemAttr("overloadSensorModuleStrengthBonus"))
    module.boostItemAttr("scanResolutionBonus", module.getModifiedItemAttr("overloadSensorModuleStrengthBonus"),
                         stackingPenalties=True)

    for scanType in ("Gravimetric", "Magnetometric", "Radar", "Ladar"):
        module.boostItemAttr(
            "scan{}StrengthPercent".format(scanType),
            module.getModifiedItemAttr("overloadSensorModuleStrengthBonus"),
            stackingPenalties=True
        )
