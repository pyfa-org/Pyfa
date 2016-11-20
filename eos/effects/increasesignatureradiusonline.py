# increaseSignatureRadiusOnline
#
# Used by:
# Modules from group: Inertial Stabilizer (7 of 7)
type = "passive"


def handler(fit, module, context):
    fit.ship.boostItemAttr("signatureRadius", module.getModifiedItemAttr("signatureRadiusBonus"))
