# Used by:
# Modules from group: ECCM (44 of 44)
# Module: QA ECCM
type = "active"
def handler(fit, module, context):
    for type in ("Gravimetric", "Magnetometric", "Radar", "Ladar"):
        fit.ship.boostItemAttr("scan%sStrength" % type,
                               module.getModifiedItemAttr("scan%sStrengthPercent" % type),
                               stackingPenalties = True)