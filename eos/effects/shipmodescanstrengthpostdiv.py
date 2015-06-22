# shipModeScanStrengthPostDiv
#
# Used by:
# Modules named like: Sharpshooter Mode (4 of 4)
type = "passive"
def handler(fit, module, context):
    for scanType in ("Gravimetric", "Magnetometric", "Radar", "Ladar"):
        fit.ship.multiplyItemAttr(
            "scan{}Strength".format(scanType),
            1 / (module.getModifiedItemAttr("mode{}StrengthPostDiv".format(scanType)) or 1),
            stackingPenalties=True,
            penaltyGroup="postDiv"
        )
