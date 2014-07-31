# Used by:
# Modules from group: Sensor Backup Array (72 of 72)
type = "passive"
def handler(fit, module, context):
    for type in ("Gravimetric", "Magnetometric", "Radar", "Ladar"):
        fit.ship.boostItemAttr("scan%sStrength" % type,
                               module.getModifiedItemAttr("scan%sStrengthPercent" % type),
                               stackingPenalties = True)