# Used by:
# Modules named like: Engine Thermal Shielding (8 of 8)
type = "passive"
def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Propulsion Module",
                                  "duration", module.getModifiedItemAttr("durationBonus"))
