# entosisLink
#
# Used by:
# Modules from group: Entosis Link (2 of 2)
type = "active"
def handler(fit, module, context):
    fit.ship.forceItemAttr("disallowAssistance", module.getModifiedItemAttr("disallowAssistance"))
