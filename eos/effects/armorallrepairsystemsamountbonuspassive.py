# Used by:
# Implant: Improved Exile Booster
# Implant: Standard Exile Booster
# Implant: Strong Exile Booster
# Implant: Synth Exile Booster
type = "passive"
def handler(fit, booster, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems") or mod.item.requiresSkill("Capital Repair Systems"),
                                  "armorDamageAmount", booster.getModifiedItemAttr("armorDamageAmountBonus"))
