# entosisLink
#
# Used by:
# Modules from group: Entosis Link (6 of 6)
type = "active"


def handler(fit, module, context):
    fit.ship.forceItemAttr("disallowAssistance", module.getModifiedItemAttr("disallowAssistance"))
