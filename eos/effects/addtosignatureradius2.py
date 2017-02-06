# addToSignatureRadius2
#
# Used by:
# Modules from group: Missile Launcher Bomb (2 of 2)
# Modules from group: Shield Extender (33 of 33)
type = "passive"


def handler(fit, module, context):
    fit.ship.increaseItemAttr("signatureRadius", module.getModifiedItemAttr("signatureRadiusAdd"))
