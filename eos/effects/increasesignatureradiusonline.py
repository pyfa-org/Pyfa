# Used by:
# Modules from group: Inertia Stabilizer (12 of 12)
type = "passive"
def handler(fit, module, context):
    fit.ship.boostItemAttr("signatureRadius", module.getModifiedItemAttr("signatureRadiusBonus"))