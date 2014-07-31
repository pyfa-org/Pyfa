# Used by:
# Modules from group: Target Painter (9 of 9)
# Drones named like: TP (3 of 3)
type = "projected", "active"
def handler(fit, container, context):
    if "projected" in context:
        fit.ship.boostItemAttr("signatureRadius", container.getModifiedItemAttr("signatureRadiusBonus"),
                               stackingPenalties = True)
