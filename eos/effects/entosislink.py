# entosisLink
#
# Used by:
# Modules from group: Entosis Link (6 of 6)
type = "active"


def handler(fit, module, context):
    fit.ship.forceItemAttr("disallowAssistance", module.getModifiedItemAttr("disallowAssistance"))
    for scanType in ("Gravimetric", "Magnetometric", "Radar", "Ladar"):
        fit.ship.boostItemAttr(
            "scan{}Strength".format(scanType),
            module.getModifiedItemAttr("scan{}StrengthPercent".format(scanType)),
            stackingPenalties=True
        )
