# Used by:
# Modules from group: Target Painter (9 of 9)
# Drone: Berserker TP-900
# Drone: Valkyrie TP-600
# Drone: Warrior TP-300
type = "projected", "active"
def handler(fit, container, context):
    if "projected" in context:
        fit.ship.boostItemAttr("signatureRadius", container.getModifiedItemAttr("signatureRadiusBonus"),
                               stackingPenalties = True)
