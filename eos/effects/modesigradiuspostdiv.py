type = "passive"
def handler(fit, module, context):
    level = fit.character.getSkill("Minmatar Destroyer").level
    fit.ship.multiplyItemAttr("signatureRadius", 1/module.getModifiedItemAttr("modeSignatureRadiusPostDiv"),
                           stackingPenalties = True, penaltyGroup="postDiv")
