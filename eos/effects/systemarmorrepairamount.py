# Used by:
# Celestials named like: Cataclysmic Variable Effect Beacon Class (6 of 6)
runTime = "early"
type = ("projected", "offline")
def handler(fit, module, context):
    fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == "Armor Repair Unit",
                                     "armorDamageAmount", module.getModifiedItemAttr("armorDamageAmountMultiplier"),
                                     stackingPenalties = True)
