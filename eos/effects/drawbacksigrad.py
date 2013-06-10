# Used by:
# Modules from group: Rig Shield (72 of 72)
type = "passive"
def handler(fit, module, context):
    fit.ship.boostItemAttr("signatureRadius", module.getModifiedItemAttr("drawback"), stackingPenalties = True)
