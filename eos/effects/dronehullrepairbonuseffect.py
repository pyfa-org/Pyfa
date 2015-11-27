type = "passive"
def handler(fit, src, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.group.name == "Logistic Drone", "structureDamageAmount", src.getModifiedItemAttr("droneArmorDamageAmountBonus"))