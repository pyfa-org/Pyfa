# shipBonusDreadnoughtM2ROFBonus
#
# Used by:
# Ship: Naglfar
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Projectile Turret"), "speed",
                                  src.getModifiedItemAttr("shipBonusDreadnoughtM2"), skill="Minmatar Dreadnought")
