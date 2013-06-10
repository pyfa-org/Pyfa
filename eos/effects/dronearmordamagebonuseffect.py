# Used by:
# Ship: Exequror
# Ship: Guardian
# Ship: Oneiros
# Ship: Scythe
type = "passive"
def handler(fit, ship, context):
    # This is actually level-less bonus, anyway you have to train cruisers 5
    # and will get 100% (20%/lvl as stated by description)
    fit.drones.filteredItemBoost(lambda drone: drone.item.group.name == "Logistic Drone",
                                 "armorDamageAmount", ship.getModifiedItemAttr("droneArmorDamageAmountBonus"))
