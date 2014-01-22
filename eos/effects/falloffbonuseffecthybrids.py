# Used by:
# Modules named like: Hybrid Ambit (8 of 8)
type = "passive"
def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Hybrid Weapon",
                                  "falloff", module.getModifiedItemAttr("falloffBonus"),
                                  stackingPenalties = True)