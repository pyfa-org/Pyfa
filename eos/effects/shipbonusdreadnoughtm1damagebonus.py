# shipBonusDreadnoughtM1DamageBonus
#
# Used by:
# Ship: Naglfar
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Projectile Turret"), "damageMultiplier",
                                  src.getModifiedItemAttr("shipBonusDreadnoughtM1"), skill="Minmatar Dreadnought")
