# sensorBoosterActivePercentage
#
# Used by:
# Modules from group: Sensor Booster (16 of 16)
type = "active"


def handler(fit, module, context):
    fit.ship.boostItemAttr("maxTargetRange", module.getModifiedItemAttr("maxTargetRangeBonus"),
                           stackingPenalties=True)
    fit.ship.boostItemAttr("scanResolution", module.getModifiedItemAttr("scanResolutionBonus"),
                           stackingPenalties=True)

    for scanType in ("Gravimetric", "Magnetometric", "Radar", "Ladar"):
        fit.ship.boostItemAttr(
            "scan{}Strength".format(scanType),
            module.getModifiedItemAttr("scan{}StrengthPercent".format(scanType)),
            stackingPenalties=True
        )
