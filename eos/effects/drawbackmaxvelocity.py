# Used by:
# Modules from group: Rig Armor (56 of 72)
type = "passive"
def handler(fit, module, context):
    fit.ship.boostItemAttr("maxVelocity", module.getModifiedItemAttr("drawback"),
                           stackingPenalties = True)