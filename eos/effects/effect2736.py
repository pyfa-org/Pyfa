# boosterArmorRepairAmountPenalty
#
# Used by:
# Implants named like: Drop Booster (3 of 4)
# Implants named like: Mindflood Booster (3 of 4)
# Implants named like: Sooth Sayer Booster (3 of 4)
type = "boosterSideEffect"

# User-friendly name for the side effect
displayName = "Armor Repair Amount"

# Attribute that this effect targets
attr = "boosterArmorRepairAmountPenalty"


def handler(fit, booster, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Armor Repair Unit",
                                  "armorDamageAmount", booster.getModifiedItemAttr(attr))
