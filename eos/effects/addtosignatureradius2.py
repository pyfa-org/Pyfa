# Used by:
# Modules from group: Shield Extender (37 of 37)
type = "passive"
def handler(fit, module, context):
    fit.ship.increaseItemAttr("signatureRadius", module.getModifiedItemAttr("signatureRadiusAdd"))