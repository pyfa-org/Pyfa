# addToSignatureRadius2
#
# Used by:
# Modules from group: Missile Launcher Bomb (2 of 2)
# Modules from group: Shield Extender (36 of 36)
type = "passive"


def handler(fit, module, context):
    fit.ship.increaseItemAttr("signatureRadius", module.getModifiedItemAttr("signatureRadiusAdd"))
