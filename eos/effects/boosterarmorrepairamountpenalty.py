# Used by:
# Implant: Improved Drop Booster
# Implant: Improved Mindflood Booster
# Implant: Improved Sooth Sayer Booster
# Implant: Standard Drop Booster
# Implant: Standard Mindflood Booster
# Implant: Standard Sooth Sayer Booster
# Implant: Strong Drop Booster
# Implant: Strong Mindflood Booster
# Implant: Strong Sooth Sayer Booster
type = "boosterSideEffect"
def handler(fit, booster, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Armor Repair Unit",
                                  "armorDamageAmount", booster.getModifiedItemAttr("boosterArmorRepairAmountPenalty"))
