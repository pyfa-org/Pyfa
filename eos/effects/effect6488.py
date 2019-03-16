# scriptSensorBoosterSensorStrengthBonusBonus
#
# Used by:
# Charges from group: Sensor Booster Script (3 of 3)
type = "active"


def handler(fit, module, context):
    for scanType in ("Gravimetric", "Magnetometric", "Radar", "Ladar"):
        module.boostItemAttr("scan{}StrengthPercent".format(scanType),
                             module.getModifiedChargeAttr("sensorStrengthBonusBonus"))
