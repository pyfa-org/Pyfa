# Used by:
# Ship: Gnosis
# Ship: Taipan
# Ship: Velator
type = "passive"
def handler(fit, container, context):
    level = container.level if "skill" in context else 1
    fit.drones.filteredItemBoost(lambda drone: drone.item.group.name == "Mining Drone",
                                 "miningAmount", container.getModifiedItemAttr("rookieDroneBonus"))
