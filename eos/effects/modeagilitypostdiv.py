type = "passive"
def handler(fit, module, context):
    fit.ship.multiplyItemAttr("agility", 1/module.getModifiedItemAttr("modeAgilityPostDiv"),
                           stackingPenalties = True, penaltyGroup="postDiv")
