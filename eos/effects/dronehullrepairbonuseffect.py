# droneHullRepairBonusEffect
#
# Used by:
# Ships from group: Logistics (5 of 6)
# Ship: Exequror
# Ship: Scythe
type = "passive"


def handler(fit, src, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.group.name == "Logistic Drone", "structureDamageAmount",
                                 src.getModifiedItemAttr("droneArmorDamageAmountBonus"))
