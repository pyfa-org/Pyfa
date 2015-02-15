# modeVelocityPostDiv
#
# Used by:
# Modules named like: Propulsion Mode (2 of 2)
type = "passive"
def handler(fit, module, context):
    fit.ship.multiplyItemAttr(
        "maxVelocity",
        1 / module.getModifiedItemAttr("modeVelocityPostDiv"),
        stackingPenalties=True,
        penaltyGroup="postDiv"
    )
