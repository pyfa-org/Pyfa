# Used by:
# Modules named like: Durability Enhancer (8 of 8)
type = "passive"
def handler(fit, module, context):
    fit.drones.filteredItemBoost(lambda drone: drone.item.requiresSkill("Drones"),
                                  "armorHP", module.getModifiedItemAttr("hullHpBonus"))
