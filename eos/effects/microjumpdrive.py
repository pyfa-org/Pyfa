# Used by:
# Module: Large Micro Jump Drive
type = "active"
def handler(fit, module, context):
    fit.ship.boostItemAttr("signatureRadius", module.getModifiedItemAttr("signatureRadiusBonusPercent"))