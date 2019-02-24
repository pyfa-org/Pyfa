# shipBonusMiningDroneAmountPercentRookie
#
# Used by:
# Ship: Gnosis
# Ship: Praxis
# Ship: Taipan
# Ship: Velator
type = "passive"


def handler(fit, container, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Mining Drone Operation"),
                                 "miningAmount", container.getModifiedItemAttr("rookieDroneBonus"))
