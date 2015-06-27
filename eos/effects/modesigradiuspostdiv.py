# modeSigRadiusPostDiv
#
# Used by:
# Module: Confessor Defense Mode
# Module: Jackdaw Defense Mode
type = "passive"
def handler(fit, module, context):
    fit.ship.multiplyItemAttr("signatureRadius", 1 / module.getModifiedItemAttr("modeSignatureRadiusPostDiv"),
                              stackingPenalties=True, penaltyGroup="postDiv")
