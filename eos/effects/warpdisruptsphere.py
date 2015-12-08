# warpDisruptSphere
#
# Used by:
# Modules from group: Warp Disrupt Field Generator (7 of 7)
type = "active"
runTime = "early"
def handler(fit, module, context):
    fit.ship.boostItemAttr("mass", module.getModifiedItemAttr("massBonusPercentage"))
    fit.ship.boostItemAttr("signatureRadius", module.getModifiedItemAttr("signatureRadiusBonus"))
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Propulsion Module",
                                  "speedBoostFactor", module.getModifiedItemAttr("speedBoostFactorBonus"))
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Propulsion Module",
                                  "speedFactor", module.getModifiedItemAttr("speedFactorBonus"))
    fit.ship.forceItemAttr("disallowAssistance", 1)
