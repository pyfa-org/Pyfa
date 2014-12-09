# shipModeMaxTargetRangePostDiv
#
# Used by:
# Module: Amarr Tactical Destroyer Sharpshooter Mode
type = "passive"
def handler(fit, module, context):
    fit.ship.multiplyItemAttr("maxTargetRange", 1/module.getModifiedItemAttr("modeMaxTargetRangePostDiv"),
                           stackingPenalties = True, penaltyGroup="postDiv")
