# shipBonusTitanM2ROFBonus
#
# Used by:
# Ship: Ragnarok
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Projectile Turret"), "speed",
                                  src.getModifiedItemAttr("shipBonusTitanM2"), skill="Minmatar Titan")
