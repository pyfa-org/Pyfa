# shipBonusMiningDroneAmountPercentRookie
#
# Used by:
# Ship: Gnosis
# Ship: Praxis
# Ship: Taipan
# Ship: Velator
type = "passive"


def handler(fit, container, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.group.name == "Mining Drone",
                                 "miningAmount", container.getModifiedItemAttr("rookieDroneBonus"))
