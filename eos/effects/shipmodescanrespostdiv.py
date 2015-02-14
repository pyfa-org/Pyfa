# shipModeScanResPostDiv
#
# Used by:
# Modules named like: Sharpshooter Mode (2 of 2)
type = "passive"
def handler(fit, module, context):
    fit.ship.multiplyItemAttr("scanResolution", 1/module.getModifiedItemAttr("modeScanResPostDiv"),
                           stackingPenalties = True, penaltyGroup="postDiv")
