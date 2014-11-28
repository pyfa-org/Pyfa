type = "passive"
def handler(fit, module, context):
    # @todo: most likely have to fix this on release
    fit.ship.boostItemAttr("maxVelocity", module.getModifiedItemAttr("modeVelocityPostDiv"),
                           stackingPenalties = True, penaltyGroup="postDiv")
