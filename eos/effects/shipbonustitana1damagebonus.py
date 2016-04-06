# shipBonusTitanA1DamageBonus
#
# Used by:
# Ship: Avatar
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Energy Turret"), "damageMultiplier", src.getModifiedItemAttr("shipBonusTitanA1"), skill="Amarr Titan")
