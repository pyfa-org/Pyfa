# Used by:
# Implants named like: Exile Booster (4 of 4)
type = "passive"
def handler(fit, booster, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Repair Systems"),
                                  "armorDamageAmount", booster.getModifiedItemAttr("armorDamageAmountBonus"))
