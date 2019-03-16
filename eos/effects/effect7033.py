# shipBonusHeavyMissileEMDamageCBC2
#
# Used by:
# Ship: Drake Navy Issue
type = "passive"


def handler(fit, src, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"),
                                    "emDamage", src.getModifiedItemAttr("shipBonusCBC2"), skill="Caldari Battlecruiser")
