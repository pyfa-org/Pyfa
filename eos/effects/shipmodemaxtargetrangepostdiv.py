# shipModeMaxTargetRangePostDiv
#
# Used by:
# Modules named like: Sharpshooter Mode (4 of 4)
type = "passive"
def handler(fit, module, context):
    fit.ship.multiplyItemAttr(
        "maxTargetRange",
        1 / module.getModifiedItemAttr("modeMaxTargetRangePostDiv"),
        stackingPenalties=True,
        penaltyGroup="postDiv"
    )
