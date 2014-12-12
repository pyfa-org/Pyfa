# shipModeScanResPostDiv
#
# Used by:
# Module: Amarr Tactical Destroyer Sharpshooter Mode
type = "passive"
def handler(fit, module, context):
    fit.ship.multiplyItemAttr("scanResolution", 1/module.getModifiedItemAttr("modeScanResPostDiv"),
                           stackingPenalties = True, penaltyGroup="postDiv")
