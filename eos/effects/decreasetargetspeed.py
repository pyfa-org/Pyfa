# Used by:
# Drones from group: Stasis Webifying Drone (3 of 3)
# Modules from group: Stasis Web (19 of 19)
type = "active", "projected"
def handler(fit, module, context):
    if "projected" not in context:
        return
    fit.ship.boostItemAttr("maxVelocity", module.getModifiedItemAttr("speedFactor"),
                           stackingPenalties = True)
