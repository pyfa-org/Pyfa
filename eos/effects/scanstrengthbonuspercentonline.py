# scanStrengthBonusPercentOnline
#
# Used by:
# Modules from group: Signal Amplifier (7 of 7)
type = "passive"


def handler(fit, module, context):
    for type in ("Gravimetric", "Magnetometric", "Radar", "Ladar"):
        fit.ship.boostItemAttr("scan%sStrength" % type,
                               module.getModifiedItemAttr("scan%sStrengthPercent" % type),
                               stackingPenalties=True)
