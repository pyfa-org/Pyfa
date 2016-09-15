# shipBonusTitanG2ROFBonus
#
# Used by:
# Ship: Erebus
# Ship: Vanquisher
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Hybrid Turret"), "speed", src.getModifiedItemAttr("shipBonusTitanG2"), skill="Gallente Titan")
