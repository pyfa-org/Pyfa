# passiveMassAdd
#
# Used by:
# Modules from group: Entosis Link (2 of 2)
type = "offline"
def handler(fit, module, context):
    fit.ship.increaseItemAttr("mass", module.getModifiedItemAttr("massAddition"))
