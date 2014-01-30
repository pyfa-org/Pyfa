# Used by:
# Modules named like: Energy Adjuster (8 of 8)
type = "passive"
def handler(fit, module, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Energy Weapon",
                                  "trackingSpeed", module.getModifiedItemAttr("trackingSpeedBonus"),
                                  stackingPenalties = True)
