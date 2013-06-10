# Used by:
# Modules from group: Rig Hybrid Weapon (56 of 56)
type = "passive"
def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Hybrid Weapon",
                                  "power", module.getModifiedItemAttr("drawback"))