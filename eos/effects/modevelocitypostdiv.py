# modeVelocityPostDiv
#
# Used by:
# Module: Amarr Tactical Destroyer Propulsion Mode
type = "passive"
def handler(fit, module, context):
    fit.ship.multiplyItemAttr("maxVelocity", 1/module.getModifiedItemAttr("modeVelocityPostDiv"),
                           stackingPenalties = True, penaltyGroup="postDiv")
