# Used by:
# Modules from group: Projected ECCM (7 of 7)
type = "projected", "active"
def handler(fit, module, context):
    if "projected" not in context: return
    for type in ("Gravimetric", "Magnetometric", "Radar", "Ladar"):
        fit.ship.boostItemAttr("scan%sStrength" % type,
                               module.getModifiedItemAttr("scan%sStrengthPercent" % type),
                               stackingPenalties = True)
