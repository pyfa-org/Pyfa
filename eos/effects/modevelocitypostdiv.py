# modeVelocityPostDiv
#
# Used by:
# Modules named like: Propulsion Mode (3 of 4)
type = "passive"
def handler(fit, module, context):
    fit.ship.multiplyItemAttr(
        "maxVelocity",
        1 / module.getModifiedItemAttr("modeVelocityPostDiv"),
        stackingPenalties=True,
        penaltyGroup="postDiv"
    )
