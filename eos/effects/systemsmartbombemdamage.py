# systemSmartBombEmDamage
#
# Used by:
# Celestials named like: Drifter Incursion (6 of 6)
# Celestials named like: Red Giant Beacon Class (6 of 6)
runTime = "early"
type = ("projected", "offline")
def handler(fit, module, context):
    fit.modules.filteredItemMultiply(lambda mod: mod.item.group.name == "Smart Bomb",
                                     "emDamage", module.getModifiedItemAttr("smartbombDamageMultiplier"))
