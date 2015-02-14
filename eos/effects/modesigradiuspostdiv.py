# modeSigRadiusPostDiv
#
# Used by:
# Module: Amarr Tactical Destroyer Defense Mode
type = "passive"
def handler(fit, module, context):
    fit.ship.multiplyItemAttr("signatureRadius", 1/module.getModifiedItemAttr("modeSignatureRadiusPostDiv"),
                           stackingPenalties = True, penaltyGroup="postDiv")
