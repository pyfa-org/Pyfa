# Used by:
# Modules from group: Expanded Cargohold (13 of 13)
type = "passive"
def handler(fit, module, context):
    fit.ship.multiplyItemAttr("maxVelocity", module.getModifiedItemAttr("maxVelocityBonus"),
                              stackingPenalties = True)