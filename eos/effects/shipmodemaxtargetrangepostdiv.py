# shipModeMaxTargetRangePostDiv
#
# Used by:
# Modules named like: Sharpshooter Mode (3 of 3)
type = "passive"
def handler(fit, module, context):
    fit.ship.multiplyItemAttr(
        "maxTargetRange",
        1 / module.getModifiedItemAttr("modeMaxTargetRangePostDiv"),
        stackingPenalties=True,
        penaltyGroup="postDiv"
    )
