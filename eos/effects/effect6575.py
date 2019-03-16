# skillBonusCapitalPulseLaserSpecialization
#
# Used by:
# Skill: Capital Pulse Laser Specialization
type = "passive"


def handler(fit, src, context):
    lvl = src.level
    fit.modules.filteredItemBoost(lambda mod: mod.item.requiresSkill("Capital Pulse Laser Specialization"),
                                  "damageMultiplier", src.getModifiedItemAttr("damageMultiplierBonus") * lvl)
