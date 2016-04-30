# shipBonusDreadnoughtG2ROFBonus
#
# Used by:
# Ship: Moros
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Hybrid Turret"), "speed", src.getModifiedItemAttr("shipBonusDreadnoughtG2"), skill="Gallente Dreadnought")
