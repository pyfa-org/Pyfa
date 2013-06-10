# Used by:
# Modules from group: Reinforced Bulkhead (12 of 12)
type = "passive"
def handler(fit, module, context):
    fit.ship.multiplyItemAttr("maxVelocity", module.getModifiedItemAttr("maxVelocityBonus"),
                              stackingPenalties = True)