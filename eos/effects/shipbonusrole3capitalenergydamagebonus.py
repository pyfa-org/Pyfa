# shipBonusRole3CapitalEnergyDamageBonus
#
# Used by:
# Ship: Chemosh
# Ship: Molok
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Energy Turret"), "damageMultiplier", src.getModifiedItemAttr("shipBonusRole3"))
