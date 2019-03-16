# shipBonusTitanG1DamageBonus
#
# Used by:
# Ship: Erebus
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Hybrid Turret"), "damageMultiplier",
                                  src.getModifiedItemAttr("shipBonusTitanG1"), skill="Gallente Titan")
