# drawbackSigRad
#
# Used by:
# Modules from group: Rig Shield (72 of 72)
# Modules named like: Optimizer (16 of 16)
type = "passive"
def handler(fit, module, context):
    fit.ship.boostItemAttr("signatureRadius", module.getModifiedItemAttr("drawback"), stackingPenalties = True)
