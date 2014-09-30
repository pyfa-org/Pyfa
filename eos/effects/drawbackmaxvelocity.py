# drawbackMaxVelocity
#
# Used by:
# Modules from group: Rig Armor (48 of 72)
# Modules from group: Rig Resource Processing (8 of 10)
type = "passive"
def handler(fit, module, context):
    fit.ship.boostItemAttr("maxVelocity", module.getModifiedItemAttr("drawback"),
                           stackingPenalties = True)