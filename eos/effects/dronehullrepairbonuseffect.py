# droneHullRepairBonusEffect
#
# Used by:
# Ships from group: Logistics (6 of 7)
# Ship: Exequror
# Ship: Scythe
type = "passive"


def handler(fit, src, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.group.name == "Logistic Drone", "structureDamageAmount",
                                 src.getModifiedItemAttr("droneArmorDamageAmountBonus"))
