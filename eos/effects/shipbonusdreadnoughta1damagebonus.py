# shipBonusDreadnoughtA1DamageBonus
#
# Used by:
# Ship: Revelation
type = "passive"
def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Energy Turret"), "damageMultiplier", src.getModifiedItemAttr("shipBonusDreadnoughtA1"), skill="Amarr Dreadnought")
