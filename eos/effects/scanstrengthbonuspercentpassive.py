# scanStrengthBonusPercentPassive
#
# Used by:
# Implants named like: High grade (20 of 66)
type = "passive"


def handler(fit, implant, context):
    for type in ("Gravimetric", "Magnetometric", "Radar", "Ladar"):
        sensorType = "scan{0}Strength".format(type)
        sensorBoost = "scan{0}StrengthPercent".format(type)
        if sensorBoost in implant.item.attributes:
            fit.ship.boostItemAttr(sensorType, implant.getModifiedItemAttr(sensorBoost))
