type = "passive"
def handler(fit, module, context):
    fit.ship.multiplyItemAttr("scanRadarStrength", 1/module.getModifiedItemAttr("modeRadarStrengthPostDiv"),
                           stackingPenalties = True, penaltyGroup="postDiv")
