type = "passive"
def handler(fit, module, context):
    # @todo: most likely have to fix this on release
    fit.ship.boostItemAttr("agility", module.getModifiedItemAttr("modeAgilityPostDiv"),
                           stackingPenalties = True, penaltyGroup="postDiv")
